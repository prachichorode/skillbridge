document.addEventListener("DOMContentLoaded", function () {

    const steps = document.querySelectorAll(".roadmap-step");

    const progressFill =
        document.getElementById("progressFill");

    const progressText =
        document.getElementById("progressText");


    // If roadmap doesn't exist
    if (!steps.length) {
        return;
    }


    /*
        Each roadmap step represents
        equal learning progress.
    */

    const progress =
        Math.round(100 / steps.length);


    // Update progress bar
    if (progressFill) {
        progressFill.style.width = progress + "%";
    }


    // Update progress percentage
    if (progressText) {
        progressText.innerText = progress + "%";
    }


    // Small animation for roadmap cards
    steps.forEach(function (step, index) {

        step.style.opacity = "0";
        step.style.transform = "translateY(20px)";


        setTimeout(function () {

            step.style.transition =
                "opacity 0.5s ease, transform 0.5s ease";

            step.style.opacity = "1";
            step.style.transform = "translateY(0)";

        }, index * 120);

    });

});