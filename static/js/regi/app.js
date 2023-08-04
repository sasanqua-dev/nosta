window.SQR = window.SQR || {};

SQR.reader = (() => {
    /**
     * getUserMedia()に非対応の場合は非対応の表示をする
     */
    const showUnsuportedScreen = () => {
        document.querySelector('#js-unsupported').classList.add('is-show');
    };
    //if (navigator.mediaDevices == null) {
    //    showUnsuportedScreen();
    //    return;
    //} else {
    //    MediaDevices.getUserMedia({ video: true });
    //}
    const video = document.querySelector('#js-video');

    /**
     * videoの出力をCanvasに描画して画像化 jsQRを使用してQR解析
     */
    const checkQRUseLibrary = () => {
        const canvas = document.querySelector('#js-canvas');
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, canvas.width, canvas.height);

        if (code) {
            SQR.modal.open(code.data);
        } else {
            setTimeout(checkQRUseLibrary, 200);
        }
    };

    /**
     * videoの出力をBarcodeDetectorを使用してQR解析
     */
    const checkQRUseBarcodeDetector = () => {
        const barcodeDetector = new BarcodeDetector();
        barcodeDetector
            .detect(video)
            .then((barcodes) => {
                if (barcodes.length > 0) {
                    for (let barcode of barcodes) {
                        SQR.modal.open(barcode.rawValue);
                    }
                } else {
                    setTimeout(checkQRUseBarcodeDetector, 200);
                }
            })
            .catch(() => {
                console.error('Barcode Detection failed, boo.');
            });
    };

    /**
     * BarcodeDetector APIを使えるかどうかで処理を分岐
     */
    const findQR = () => {
        window.BarcodeDetector ? checkQRUseBarcodeDetector() : checkQRUseLibrary();
    };

    /**
     * デバイスのカメラを起動
     */
    const initCamera = () => {
        navigator.mediaDevices
            .getUserMedia({
                audio: false,
                video: { facingMode: 'environment', width: { min: 1280, ideal: 1980, max: 3000 }, height: { min: 720, ideal: 1080, max: 3000 }, aspectRatio: 1 },
            })
            .then((stream) => {
                video.srcObject = stream;
                video.onloadedmetadata = () => {
                    video.play();
                    findQR();
                };
            })
            .catch((e) => {
                console.log(e);
                showUnsuportedScreen();
            });
    };

    return {
        initCamera,
        findQR,
    };
})();

SQR.modal = (() => {
    const content = document.querySelector('#modal-content-body');
    const modal = document.querySelector('#js-modal');
    const code_input = document.querySelector('#code');

    /**
     * 取得した文字列を入れ込んでモーダルを開く
     */
    const open = (code) => {
        code_input.value = code;
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === name + '=') {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
        }
        var csrf_token = getCookie('csrftoken');
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
                }
            },
            type: 'POST',
            url: path,
            data: {
                type: 'get_code',
                code: code,
            },
            dataType: 'html',
        })
            .done(function (data) {
                content.innerHTML = data;
            })
            .fail(function (data) {
                // error
                console.log(data);
                content.innerHTML = "<div class='hero hero-body is-size-4 has-text-centered'>通信エラーが発生しました</div>";
            });
        modal.classList.add('is-active');
    };

    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
        });
    });

    // Add a keyboard event to close all modals
    document.addEventListener('keydown', (event) => {
        if (event.code === 'Escape') {
            closeAllModals();
        }
    });

    const closeModal = ($el) => {
        code_input.value = '';
        $el.classList.remove('is-active');
        SQR.reader.findQR();
    };

    const closeAllModals = () => {
        (document.querySelectorAll('.modal') || []).forEach(($modal) => {
            closeModal($modal);
        });
    };

    return {
        open,
    };
})();

if (SQR.reader) SQR.reader.initCamera();

let currentSlide = 0;
const tabs = document.getElementsByClassName('tab-item');
const slides = document.getElementsByClassName('content');
function showSlide(index) {
    if (index >= 0 && index < slides.length) {
        for (let i = 0; i < slides.length; i++) {
            slides[i].classList.remove('active');
            tabs[i].classList.remove('is-active');
        }
        slides[index].classList.add('active');
        tabs[index].classList.add('is-active');
        currentSlide = index;
    }
}
showSlide(0);

function changestate(type, id) {
    var csrf_token = getCookie('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        },
        type: 'POST',
        url: path,
        data: {
            type: 'change_state',
            state: type,
            id: id,
        },
        dataType: 'html',
    })
        .done(function (data) {
            window.alert('伝票ステータスを変更しました');
        })
        .fail(function (data) {
            // error
            console.log(data);
            window.alert('エラーが発生しました');
        });
    modal.classList.add('is-active');
}
