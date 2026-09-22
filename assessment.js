document.addEventListener("DOMContentLoaded", function () {

    const quizContainer = document.getElementById("quizContainer");
    const submitButton = document.getElementById("submitQuiz");
    const resultBox = document.getElementById("resultBox");

    // =====================================================
    // CHECK HTML ELEMENTS
    // =====================================================

    if (!quizContainer || !submitButton || !resultBox) {
        console.error("Assessment HTML elements are missing.");
        return;
    }


    // =====================================================
    // QUESTIONS
    // =====================================================

    const questions = [

        {
            question: "Which language is commonly used for Data Analysis?",
            options: ["Python", "HTML", "CSS", "XML"],
            answer: "Python"
        },

        {
            question: "Which language is mainly used to query databases?",
            options: ["SQL", "HTML", "CSS", "Java"],
            answer: "SQL"
        },

        {
            question: "Which tool is commonly used for Business Intelligence?",
            options: ["Power BI", "Notepad", "Paint", "Calculator"],
            answer: "Power BI"
        },

        {
            question: "Which Python library is commonly used for data manipulation?",
            options: ["Pandas", "Flask", "Tkinter", "Requests"],
            answer: "Pandas"
        },

        {
            question: "What does DSA stand for?",
            options: [
                "Data Structures and Algorithms",
                "Data Software Application",
                "Database System Analysis",
                "Digital Software Architecture"
            ],
            answer: "Data Structures and Algorithms"
        },

        {
            question: "Which technology is used to create the structure of a webpage?",
            options: ["HTML", "Python", "SQL", "Power BI"],
            answer: "HTML"
        },

        {
            question: "Which technology is mainly used to style webpages?",
            options: ["CSS", "SQL", "Python", "Git"],
            answer: "CSS"
        },

        {
            question: "Which tool is commonly used for version control?",
            options: ["Git", "Excel", "Power BI", "NumPy"],
            answer: "Git"
        },

        {
            question: "Which library is mainly used for numerical computing in Python?",
            options: ["NumPy", "Flask", "HTML", "Git"],
            answer: "NumPy"
        },

        {
            question: "Machine Learning is a part of which field?",
            options: [
                "Artificial Intelligence",
                "Web Design",
                "Database Management",
                "Networking"
            ],
            answer: "Artificial Intelligence"
        }

    ];


    // =====================================================
    // DISPLAY QUESTIONS
    // =====================================================

    questions.forEach(function (item, index) {

        const questionBox = document.createElement("div");

        questionBox.className = "assessment-question";

        let optionsHTML = "";

        item.options.forEach(function (option) {

            optionsHTML += `
                <label class="assessment-option">

                    <input
                        type="radio"
                        name="question${index}"
                        value="${option}"
                    >

                    <span>${option}</span>

                </label>
            `;

        });


        questionBox.innerHTML = `
            <h3>
                ${index + 1}. ${item.question}
            </h3>

            <div class="assessment-options">
                ${optionsHTML}
            </div>
        `;


        quizContainer.appendChild(questionBox);

    });


    // =====================================================
    // SUBMIT ASSESSMENT
    // =====================================================

    submitButton.addEventListener("click", function () {

        let score = 0;
        let answered = 0;


        // =================================================
        // CHECK ANSWERS
        // =================================================

        questions.forEach(function (item, index) {

            const selected = document.querySelector(
                `input[name="question${index}"]:checked`
            );


            if (selected) {

                answered++;

                if (selected.value === item.answer) {
                    score++;
                }

            }

        });


        // =================================================
        // CHECK ALL QUESTIONS
        // =================================================

        if (answered < questions.length) {

            alert(
                "Please answer all 10 questions before submitting."
            );

            return;
        }


        // =================================================
        // CALCULATE RESULT
        // =================================================

        const total = questions.length;

        const percentage = Math.round(
            (score / total) * 100
        );


        let performance = "";
        let message = "";


        if (percentage >= 80) {

            performance = "Excellent";

            message =
                "Excellent performance! You have a strong foundation for your selected career.";

        }

        else if (percentage >= 60) {

            performance = "Good";

            message =
                "Good performance! Continue improving your technical skills and practice regularly.";

        }

        else if (percentage >= 40) {

            performance = "Average";

            message =
                "You are making progress. Focus on weak areas and follow your learning roadmap.";

        }

        else {

            performance = "Needs Improvement";

            message =
                "You need more preparation. Follow your roadmap and practice regularly.";

        }


        // =================================================
        // SAVE RESULT IN LOCAL STORAGE
        // =================================================

        localStorage.setItem(
            "skillbridge_score",
            score
        );

        localStorage.setItem(
            "skillbridge_total",
            total
        );

        localStorage.setItem(
            "skillbridge_percentage",
            percentage
        );

        localStorage.setItem(
            "skillbridge_performance",
            performance
        );

        localStorage.setItem(
            "skillbridge_message",
            message
        );


        // =================================================
        // SHOW RESULT
        // =================================================

        resultBox.style.display = "block";


        resultBox.innerHTML = `

            <div class="assessment-result-content">

                <h2>🎉 Assessment Completed</h2>

                <div class="assessment-score">
                    ${score} / ${total}
                </div>


                <h3>
                    Score:
                    <strong>${percentage}%</strong>
                </h3>


                <h3>
                    Performance:
                    <strong>${performance}</strong>
                </h3>


                <p>
                    ${message}
                </p>


                <div class="roadmap-action">

                    <button
                        type="button"
                        class="assessment-retry-btn"
                        id="retryAssessment">

                        🔄 Retake Assessment

                    </button>


                    <a
                        href="/report"
                        class="btn">

                        📋 View Full Report

                    </a>

                </div>

            </div>

        `;


        // =================================================
        // RETAKE BUTTON
        // =================================================

        const retryButton =
            document.getElementById("retryAssessment");


        if (retryButton) {

            retryButton.addEventListener(
                "click",
                function () {

                    location.reload();

                }
            );

        }


        // =================================================
        // DISABLE SUBMIT BUTTON
        // =================================================

        submitButton.disabled = true;

        submitButton.innerText =
            "Assessment Submitted";


        // =================================================
        // SCROLL TO RESULT
        // =================================================

        resultBox.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    });

});