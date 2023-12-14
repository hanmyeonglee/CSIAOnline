let wave = document.getElementById("gradientWave");
let interv = undefined;

setTimeout(() => {
    interv = setInterval(() => {
        wave.style.transition = "all 2.5s ease-in-out 0s";
        wave.style.transform = "scale(1.55)";
        wave.style.opacity = 0;
        setTimeout(() => {
            wave.style.transition = "all 0s linear 0s";
            wave.style.transform = "scale(1)";
            wave.style.opacity = 1;
        }, 2700);
    }, 3000);
}, 300);