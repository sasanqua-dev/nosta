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
                video: { facingMode: 'environment', width: { min: 800, ideal: 1280, max: 2000 }, height: { min: 600, ideal: 720, max: 2000 }, aspectRatio: 1 },
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
    const result = document.querySelector('#js-result');
    const modal = document.querySelector('#js-modal');
    const modalClose = document.querySelector('#js-modal-close');

    /**
     * 取得した文字列を入れ込んでモーダルを開く
     */
    const open = (url) => {
        result.value = url;
        modal.classList.add('is-active');
    };

    /**
     * モーダルを閉じてQR読み込みを再開
     */
    const close = () => {
        modal.classList.remove('is-show');
        SQR.reader.findQR();
    };

    modalClose.addEventListener('click', () => close());

    return {
        open,
    };
})();
(document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');
    $close.addEventListener('click', () => {
        closeModal($target);
    });
});

if (SQR.reader) SQR.reader.initCamera();
