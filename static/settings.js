document.addEventListener("DOMContentLoaded", function () {

    // =========================================
    // DARK MODE
    // =========================================

    const darkMode = document.getElementById("darkMode");

    if (darkMode) {

        const savedTheme =
            localStorage.getItem("skillbridge-theme");

        // Load saved theme
        if (savedTheme === "dark") {

            document.body.classList.add("dark-mode");

            darkMode.checked = true;

        } else {

            document.body.classList.remove("dark-mode");

            darkMode.checked = false;

        }


        // Dark mode click
        darkMode.addEventListener("change", function () {

            if (this.checked) {

                document.body.classList.add("dark-mode");

                localStorage.setItem(
                    "skillbridge-theme",
                    "dark"
                );

            } else {

                document.body.classList.remove("dark-mode");

                localStorage.setItem(
                    "skillbridge-theme",
                    "light"
                );

            }

        });

    }


    // =========================================
    // LEARNING REMINDER
    // =========================================

    const learningReminder =
        document.getElementById("learningReminder");

    if (learningReminder) {

        const saved =
            localStorage.getItem("learningReminder");

        if (saved === "false") {

            learningReminder.checked = false;

        }

        learningReminder.addEventListener(
            "change",
            function () {

                localStorage.setItem(
                    "learningReminder",
                    this.checked
                );

            }
        );

    }


    // =========================================
    // PLACEMENT NOTIFICATION
    // =========================================

    const placementNotification =
        document.getElementById(
            "placementNotification"
        );

    if (placementNotification) {

        const saved =
            localStorage.getItem(
                "placementNotification"
            );

        if (saved === "false") {

            placementNotification.checked = false;

        }

        placementNotification.addEventListener(
            "change",
            function () {

                localStorage.setItem(
                    "placementNotification",
                    this.checked
                );

            }
        );

    }


    // =========================================
    // ASSESSMENT REMINDER
    // =========================================

    const assessmentReminder =
        document.getElementById(
            "assessmentReminder"
        );

    if (assessmentReminder) {

        const saved =
            localStorage.getItem(
                "assessmentReminder"
            );

        if (saved === "false") {

            assessmentReminder.checked = false;

        }

        assessmentReminder.addEventListener(
            "change",
            function () {

                localStorage.setItem(
                    "assessmentReminder",
                    this.checked
                );

            }
        );

    }

});