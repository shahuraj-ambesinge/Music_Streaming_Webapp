$(document).ready(function() {
    var audio = document.getElementById('audioPlayer');
    var playPauseBtn = document.getElementById('playPauseBtn');
    var stopBtn = document.getElementById('stopBtn');

    playPauseBtn.addEventListener('click', function() {
        if (audio.paused || audio.ended) {
            audio.play();
            playPauseBtn.innerHTML = 'Pause';
        } else {
            audio.pause();
            playPauseBtn.innerHTML = 'Play';
        }
    });

    stopBtn.addEventListener('click', function() {
        audio.pause();
        audio.currentTime = 0;
        playPauseBtn.innerHTML = 'Play';
    });
});

