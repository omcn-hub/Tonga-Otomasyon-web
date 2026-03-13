@extends($masterpage ?? 'panel.master')

@section('breadcrumb')
    <ol class="breadcrumb page-breadcrumb">
        <li class="breadcrumb-item"><a href="{{ route('panel.index') }}">Ana Sayfa</a></li>
        @foreach ($container->view->breadcrumb as $title => $href)
            <li class="breadcrumb-item"><a href="{{ $href }}">{{ $title }}</a></li>
        @endforeach
        <li class="breadcrumb-item active">{{ is_null($item->id) ? 'Yeni Video Yükle' : 'Videoyu Düzenle' }}</li>
    </ol>
@endsection

@section('content')
    <div class="row">
        <div class="col-xl-12">

            <ul class="nav nav-tabs nav-fill" role="tablist">
                <li class="nav-item">
                    <a class="nav-link fs-lg px-4 active" data-toggle="tab" href="#tab_set1" role="tab">Yapay Zeka Görev Formu</a>
                </li>
            </ul>

            <div id="panel-1" class="panel" style="border-top: none;">
                <form ajax-form method="POST"
                    action="{{ route('panel.' . $container->page . '_save', ['unique' => $item->id]) }}"
                    enctype="multipart/form-data">
                    @csrf

                    <div class="panel-container show">
                        <div class="panel-content">

                            <div class="tab-content p-1">

                                <div class="tab-pane fade show active" id="tab_set1" role="tabpanel">
                                    <div class="row mt-3">

                                        <div class="col-md-12">
                                            <div class="form-group mb-3">
                                                <label class="form-label">Video Başlığı (İsteğe Bağlı)</label>
                                                <input type="text" class="form-control" name="title"
                                                    value="{{ old('title') ? old('title') : $item->title }}"
                                                    placeholder="Boş bırakırsanız yapay zeka sesten dinleyip efsane bir başlık bulacaktır...">
                                                @error('title')
                                                    <span class="badge badge-danger">{{ $message }}</span>
                                                @enderror
                                            </div>
                                        </div>

                                        <div class="col-md-12">
                                            <div class="form-group mb-3">
                                                <label class="form-label">Ses Dosyası (MP3, M4A, WAV) <span class="text-danger">*</span></label>
                                                <input type="file" class="form-control form-control-file" name="audio" accept=".mp3, .m4a, .wav" {{ is_null($item->id) ? 'required' : '' }}>
                                                @error('audio')
                                                    <span class="badge badge-danger">{{ $message }}</span>
                                                @enderror

                                                @if(!is_null($item->audio_path))
                                                    <small class="text-info mt-2 d-block"><i class="fal fa-check"></i> Sisteme daha önce bir ses dosyası yüklenmiş.</small>
                                                @endif
                                            </div>
                                        </div>

                                    </div>
                                </div>
                            </div>

                            <div class="panel-content border-faded border-left-0 border-right-0 border-bottom-0 mt-4">
                                <button class="btn btn-primary ml-auto waves-effect waves-themed wd-100" type="submit">
                                    <i class="fal fa-robot"></i> Yapay Zekaya Gönder
                                </button>
                                <a class="btn btn-warning ml-auto waves-effect waves-themed wd-100 color-white" href="{{ route('panel.' . $container->page . '_list') }}">İptal</a>
                            </div>
                        </div>
                    </div>
                </form>
            </div>

        </div>
    </div>
@endsection
