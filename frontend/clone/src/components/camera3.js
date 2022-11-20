const camera = function () {
    let width = 1080;
    let height = 1080;
    
    const createObjects = function () {
    
    
        const video = document.createElement('video');
        video.id = 'video';
        video.width = width;
        video.width = height;
        video.autoplay = true;
        document.body.appendChild(video);
    
        const canvas = document.createElement('canvas');
        canvas.id = 'canvas';
        canvas.width = width;
        canvas.width = height;
        document.body.appendChild(canvas);
    }
    
    
    return {
        video: null,
        context: null,
        canvas: null,
        
        startCamera: function (w = 1080, h = 1080) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                width = w;
                height = h;
    
                createObjects();
    
                this.video = document.getElementById('video');
                this.canvas = document.getElementById('canvas');
                this.context = this.canvas.getContext('2d');
    
    
                (function (video) {
                    navigator.mediaDevices.getUserMedia({video: true}).then(function (stream) {
                        video.srcObject = stream;
                        video.play();
                    });
                })(this.video)
    
            }
        },
    
    
        takeSnapshot: function () {
            console.log(width,height)
            this.context.drawImage(this.video,0,0);
            var data = canvas.toDataURL('image/png');
            photo.setAttribute('src', data);
        }
    
    }
    }();
    
    export default camera;