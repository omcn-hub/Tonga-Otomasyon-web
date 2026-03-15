@extends($masterpage ?? 'panel.master')

@section('breadcrumb')
<ol class="breadcrumb page-breadcrumb">
    <li class="breadcrumb-item"><a href="{{ route('panel.index') }}">Ana Sayfa</a></li>
    @foreach($container->view->breadcrumb as $title => $href)
    <li class="breadcrumb-item"><a href="{{ $href }}" href="javascript:void(0)">{{ $title }}</a></li>
    @endforeach
    <li class="breadcrumb-item active">Liste</li>

    <li class="position-absolute pos-top pos-right d-none d-sm-block">
        <a href="javascript:void(0);" excel-export class="btn btn-info btn-icon waves-effect waves-themed mr-2" style="margin-top: -8px;">
            <i class="fal fa-file-excel"></i>
        </a>
        <a href="{{ route('panel.' . $container->page . '_form') }}" class="btn btn-success btn-icon waves-effect waves-themed" style="margin-top: -8px;">
            <i class="fal fa-plus"></i>
        </a>
    </li>
</ol>
@endsection

@section('content')
<div class="row">
    <div class="col-xl-12">
        <div id="panel-1" class="panel">
            <div class="panel-hdr">
                <h2>{{ $container->title }} Listesi</h2>
            </div>
            <div class="panel-container show">
                <div class="panel-content">

                    <table datatable class="table table-bordered table-hover table-striped w-100">
                        <thead>
                            <tr>
                                <th class="text-center"># ID</th>
                                <th class="text-center">YouTube Başlığı (AI)</th>
                                <th class="text-center">Ses Dosyası</th>
                                <th class="text-center">Video (Çıktı)</th>
                                <th class="text-center wd-100">Yapay Zeka Durumu</th>
                                <th class="text-center wd-100">Eklenme Tarihi</th>
                                <th class="text-center wd-80">İşlemler</th>
                            </tr>
                        </thead>
                        <tbody>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

@section('extra_script')
<script>
    $(document).ready(function()
    {
        BaseCRUD.selector = "[datatable]";
        BaseCRUD.ajaxtable({
            ajax: {
                url: "{{ route('panel.' . $container->page . '_list') }}?datatable=true",
                type: 'GET'
            },
            columns: [
                { data: 'id', name: 'id', className: 'text-center' },
                {
                    data: 'title',
                    name: 'title',
                    className: 'text-center',
                    render: function(data) {
                        return data ? '<b>'+data+'</b>' : '<i class="text-muted">Yapay Zeka Bekleniyor...</i>';
                    }
                },
                {
                    data: 'audio_path',
                    name: 'audio_path',
                    className: 'text-center',
                    render: function(data) {
                        return '<span class="text-info"><i class="fal fa-music"></i> Yüklendi</span>';
                    }
                },
                {
                    data: 'video_path',
                    name: 'video_path',
                    className: 'text-center',
                    render: function(data) {
                        // Eğer Python videoyu bitirmişse izle butonu çıkar
                        return data ? '<a href="javascript:void(0);" class="btn btn-xs btn-primary"><i class="fal fa-play"></i> Hazır</a>' : '-';
                    }
                },
                {
                    data: 'status',
                    name: 'status',
                    className: 'text-center ai-status-cell',
                    render: function(data, type, row) {
                        // Hücreyi bulabilmek için id'yi html attribute olarak ekliyoruz
                        var html = '<div class="ai-status-container" data-id="' + row.id + '" data-status="' + data + '">';
                        
                        // YAPAY ZEKA STATÜ RENKLENDİRMESİ VE CANLI LOG EKRANI
                        if(data == 'bekliyor') {
                            html += '<span class="badge badge-secondary" style="font-size:12px;">Bekliyor <i class="fal fa-clock"></i></span>';
                        }
                        else if(data == 'isleniyor') {
                            var lastLog = row.error_log ? row.error_log.split('\n').filter(Boolean).pop() : 'Başlatılıyor...';
                            html += '<span class="badge badge-warning mb-1" style="font-size:12px;">İşleniyor <i class="fal fa-spinner fa-spin"></i></span><br>';
                            // Canlı Log alanı
                            html += '<small class="text-muted d-block mt-1 font-italic live-log-text" style="max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="'+lastLog+'">'+lastLog+'</small>';
                        }
                        else if(data == 'tamamlandı') {
                            html += '<span class="badge badge-success" style="font-size:12px;">Tamamlandı <i class="fal fa-check"></i></span>';
                        }
                        else if(data == 'hata') {
                            html += '<span class="badge badge-danger" style="font-size:12px;">Hata! <i class="fal fa-times"></i></span>';
                        }
                        else {
                            html += data;
                        }
                        
                        html += '</div>';
                        return html;
                    }
                },
                { data: 'created_at', name: 'created_at', className: 'text-center' },
                {
                    render : function (data, type, row)
                    {
                        var html = '';
                        html += '<a href="{{ route("panel." . $container->page . "_form") }}/' + row.id + '" class="btn btn-info btn-sm btn-icon waves-effect waves-themed mr-1" data-toggle="tooltip" data-placement="auto" data-original-title="Düzenle">';
                        html += '   <i class="fal fa-edit"></i>';
                        html += '</a>';
                        html += '<a href="javascript:void(0);" row-delete="' + row.id + '" class="btn btn-danger btn-sm btn-icon waves-effect waves-themed" data-toggle="tooltip" data-placement="auto" data-original-title="Sil">';
                        html += '   <i class="fal fa-trash"></i>';
                        html += '</a>';
                        return html;
                    },
                    data: null, orderable: false, searchable: false, className: 'text-center act-col',
                },
            ],
            dom: "<'row mb-3'<'col-sm-12 col-md-6 d-flex align-items-center justify-content-start'f><'col-sm-12 col-md-6 d-flex align-items-center justify-content-end'l>><'row'<'col-sm-12'tr>><'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>><'disabled-none'B>",
            buttons: [
                {
                   extend: 'csv',
                   charset: 'UTF-8',
                   fieldSeparator: ';',
                   bom: true,
                   filename: 'TongaAi_Videolari',
                   title: 'Tonga AI Video Listesi'
                },
                'pdfHtml5'
            ],
            order: [[0, 'DESC']], // Son yüklenen en üstte çıksın diye ID'ye göre tersten sıraladık
            pageLength: 50,
        });

        $('[excel-export]').click(function(){
            $('.dt-buttons .buttons-csv').trigger('click');
        });

        BaseCRUD.delete("{{ route('panel.' . $container->page . '_delete') }}");
        
        // --- CANLI LOG TAKİBİ (AJAX) ---
        setInterval(function() {
            var activeIds = [];
            // Sadece "isleniyor" (veya bekliyor) olan satırların id'lerini topla
            $('.ai-status-container').each(function() {
                var status = $(this).attr('data-status');
                if (status === 'isleniyor' || status === 'bekliyor') {
                    activeIds.push($(this).attr('data-id'));
                }
            });

            if (activeIds.length > 0) {
                $.ajax({
                    url: "{{ route('panel.video_live_logs') }}",
                    type: "GET",
                    data: { ids: activeIds },
                    success: function(response) {
                        $.each(response, function(id, data) {
                            var container = $('.ai-status-container[data-id="' + id + '"]');
                            var oldStatus = container.attr('data-status');
                            
                            // Eğer durum "tamamlandı" veya "hata" olarak değiştiyse, DataTables sayfasını yenileyebiliriz 
                            // ya da doğrudan DOM'u güncelleyebiliriz. DOM'u güncellemek sayfayı sarsmaz.
                            if (data.status !== oldStatus) {
                                // Status değiştiyse tabloyu ufaktan yenileyelim ki video butonu vb. gelsin
                                // Ama sayfa başa sıçramasın diye paging false yapabiliriz veya sadece o satırı DataTables API ile güncelleyebiliriz.
                                // Şimdilik topyekun tablo yenilemesi en temizi (kullanıcıyı rahatsız etmeden arka planda):
                                $(BaseCRUD.selector).DataTable().ajax.reload(null, false); 
                            } else if (data.status === 'isleniyor') {
                                // Sadece log değiştiyse log metnini güncelle
                                var logEl = container.find('.live-log-text');
                                if (logEl.length) {
                                    logEl.text(data.last_log);
                                    logEl.attr('title', data.last_log);
                                }
                            }
                        });
                    }
                });
            }
        }, 5000); // 5 saniyede bir kontrol et
    });
</script>
@endsection
