document.addEventListener('DOMContentLoaded', function () {
    var stopButton = document.getElementById('stopButton');
    var elementsToStop = document.querySelectorAll('.hero *');
    var isAnimationPaused = false;

    function updateButton() {
        if (isAnimationPaused) {
            elementsToStop.forEach(function (element) {
                element.style.animationPlayState = 'running';
            });
            stopButton.textContent = 'car on';
        } else {
            elementsToStop.forEach(function (element) {
                element.style.animationPlayState = 'paused';
            });
            stopButton.textContent = 'car off';
        }
    }

    function updateButtonStyle() {
        if (isAnimationPaused) {
            stopButton.style.backgroundColor = 'green';
            stopButton.style.color = 'white';
        } else {
            stopButton.style.backgroundColor = 'red';
            stopButton.style.color = 'white';
        }
    }

    stopButton.addEventListener('click', function () {
        isAnimationPaused = !isAnimationPaused;
        updateButton();
        updateButtonStyle();
    });

    updateButtonStyle();
    updateButton();
});
