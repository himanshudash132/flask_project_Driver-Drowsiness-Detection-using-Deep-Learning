document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-webcam');
    const stopBtn = document.getElementById('stop-webcam');
    const videoFeed = document.getElementById('video');
    const loader = document.getElementById('loader');
    
    let streaming = false;

    startBtn.addEventListener('click', () => {
        if (!streaming) {
            loader.style.display = 'block';
            videoFeed.src = '/video_feed';
            videoFeed.onload = () => {
                loader.style.display = 'none';
                videoFeed.style.display = 'block';
            };
            streaming = true;
            fetchAnalyticsData();
        }
    });

    stopBtn.addEventListener('click', () => {
        if (streaming) {
            videoFeed.src = '';
            videoFeed.style.display = 'none';
            streaming = false;
        }
    });

    function fetchAnalyticsData() {
        if (streaming) {
            fetch('/analytics_data')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('uptime').textContent = `${data.uptime.toFixed(2)} seconds`;
                    document.getElementById('alert-count').textContent = data.alert_count;
                    document.getElementById('average-score').textContent = data.average_score.toFixed(2);
                });
            setTimeout(fetchAnalyticsData, 1000);  // Refresh data every second
        }
    }
});


