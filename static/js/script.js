document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('start-webcam');
    const stopButton = document.getElementById('stop-webcam');
    
    startButton.addEventListener('click', function() {
        document.getElementById('video').src = '/video_feed';
    });
    
    stopButton.addEventListener('click', function() {
        fetch('/stop_video', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'stopped') {
                    document.getElementById('video').src = '';
                }
            });
    });
});
