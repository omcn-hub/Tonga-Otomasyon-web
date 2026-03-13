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
}
