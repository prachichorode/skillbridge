document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // CAREER READINESS PROGRESS
    // ==========================================

    const progressFill =
        document.querySelector(".progress-fill");

    if (progressFill) {

        let readiness =
            Number(progressFill.dataset.readiness);

        // If readiness is not a valid number
        if (isNaN(readiness)) {
            readiness = 0;
        }

        // Keep value between 0 and 100
        readiness =
            Math.max(0, Math.min(100, readiness));

        // Set progress bar width
        progressFill.style.width =
            readiness + "%";

        // Optional: show percentage in console
        console.log(
            "Career Readiness:",
            readiness + "%"
        );
    }

});