<?php

namespace App\Http\Controllers\Panel;

use App\Http\Controllers\Controller;
use App\Models\Video;
use Illuminate\Http\Request;

class VideoController extends BaseController
{
    use BasePattern;

    public function __construct()
    {
        // Temel Ayarlar
        $this->title = 'Tonga AI Videoları';
        $this->page = 'video';
        $this->model = Video::class;
        $this->upload = 'sesler';

        // Üst Kısım Menüsü (Breadcrumb)
        $this->view = (object) [
            'breadcrumb' => [
                'Tonga AI Videoları' => 'javascript:void(0)',
            ],
        ];

        // Form Doğrulama (Validasyon) Kuralları
        $this->validation = [
            [
                'title' => 'nullable|string|max:255',
                'audio' => 'nullable|file|max:51200', // mimes uçuruldu, dosya kontrolü hook'ta!
            ],
            [
                'title' => 'Video Başlığı',
                'audio' => 'Ses Dosyası',
            ],
        ];

        parent::__construct();
    }

    /**
     * Dosya formdan geldiğinde araya giren gizli ajan (Hook)
     */
    public function saveHook(Request $request)
    {
        $params = $request->all();

        // Eğer formdan ses dosyası yüklenmişse bu bloğa girer
        if ($request->hasFile('audio')) {
            $file = $request->file('audio');
            $uzanti = strtolower($file->getClientOriginalExtension());

            // 1. KESİN KONTROL: Bizim izin verdiğimiz uzantılar mı?
            if (!in_array($uzanti, ['mp3', 'm4a', 'wav'])) {
                abort(403, 'Hata: Sadece MP3, M4A ve WAV formatları yüklenebilir!');
            }

            // Güvenlik: Zararlı yazılım engeli
            if (in_array($uzanti, ['php', 'js', 'py'])) {
                abort(403, 'Geçersiz dosya türü!');
            }

            // Dosyaya efsanevi ve benzersiz bir isim ver (Örn: a8f4d9...m4a)
            $audioName = md5(rand(1, 999999) . date('ymdhis')) . '.' . $uzanti;

            // Dosyayı sunucuya (public/upload/sesler) kaydet
            $file->move(public_path('upload/' . $this->upload), $audioName);

            // PYTHON İÇİN: Dosyanın işletim sistemindeki TAM adresini veritabanına yaz
            $params['audio_path'] = public_path('upload/' . $this->upload . '/' . $audioName);

            // Veritabanında audio diye bir sütun olmadığı için onu devreden çıkar
            unset($params['audio']);
        }
        if (isset($params['_token'])) {
            unset($params['_token']);
        }

        // Eğer yeni kayıt oluşturuluyorsa (güncelleme değilse) statüyü bekliyor yap
        if (!isset($params['id']) || empty($params['id'])) {
            $params['status'] = 'bekliyor';
        }

        return $params;
    }

    /**
     * Veritabanına kayıt atıldıktan SONRA (veya güncellendikten sonra) çalışan kanca.
     * Bu sayede yeni oluşturulan ID'ye erişebilir ve Python'a gönderebiliriz.
     */
    public function saveBack($obj)
    {
        // Yalnızca yeni yüklenen ve statüsü "bekliyor" olanlar için tetikle.
        if ($obj->status === 'bekliyor') {
            // Python projesinin bulunduğu klasör (Laravel projesinin içindeki Engine klasörü)
            $enginePath = base_path('Engine');
            
            // Python sanal ortam (venv) içindeki python.exe yolu
            $pythonExe = $enginePath . DIRECTORY_SEPARATOR . 'venv' . DIRECTORY_SEPARATOR . 'Scripts' . DIRECTORY_SEPARATOR . 'python.exe';
            
            // Çalıştırılacak yeni wrapper script
            $scriptPath = $enginePath . DIRECTORY_SEPARATOR . 'run_task.py';
            
            // Komutu oluştur. Laragon/Windows için arkaplanda çalıştırma:
            // start /B: Arka planda yeni pencere açmadan çalıştır
            // cmd /S /C: Komutu çalıştırıp kapanacak
            // "" ile python exe veya script yollarında boşluk varsa hata vermesini önlüyoruz
            // Not: Python'un doğru kütüphaneleri (genai vb.) bulabilmesi ve local dizinleri görebilmesi için
            // cd ile Engine dizinine geçip ondan sonra python'u çalıştırıyoruz.
            $command = "start /B cmd /S /C \"cd \"$enginePath\" && \"$pythonExe\" \"$scriptPath\" {$obj->id}\"";

            // Asenkron olarak cmd başlat
            pclose(popen($command, "r"));
        }

        // BaseController'daki default yönlendirmeyi manuel yapıyoruz çünkü saveBack return'ü controller'dan döner.
        return redirect()->route("panel." . $this->page . "_list")->with('success', 'Video başarıyla yüklendi, yapay zeka arka planda işleme başladı!');
    }

    /**
     * list.blade.php tarafından 5 saniyede bir çağrılarak Python güncellemelerini alır.
     */
    public function getLiveLogs(Request $request)
    {
        $ids = $request->input('ids', []);
        
        if (empty($ids)) {
            return response()->json([]);
        }

        $videos = Video::whereIn('id', $ids)->get(['id', 'status', 'error_log', 'video_path']);
        
        $data = [];
        foreach ($videos as $video) {
            // Logların son satırını al (veya tümünü array olarak döndür)
            $logLines = array_filter(explode("\n", $video->error_log ?? ''));
            $lastLog = end($logLines) ?: 'Bağlantı kuruluyor...';

            $data[$video->id] = [
                'status' => $video->status,
                'last_log' => $lastLog,
                'video_path' => $video->video_path
            ];
        }

        return response()->json($data);
    }
}
