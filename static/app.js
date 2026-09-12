// =====================================================
// SKILLBRIDGE - APP.JS
// =====================================================


// =====================================================
// REQUIRED SKILLS
// =====================================================

const requiredSkills = {

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Data Visualization",
        "Statistics"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "Data Visualization"
    ],

    "Business Intelligence": [
        "SQL",
        "Excel",
        "Power BI",
        "Data Visualization",
        "Data Modeling",
        "DAX"
    ],

    "Software Engineer": [
        "Python",
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "DSA",
        "SQL"
    ]
};


// =====================================================
// SHOW REQUIRED SKILLS
// =====================================================

function showRequiredSkills() {

    const field =
        document.getElementById("field");

    const box =
        document.getElementById("requiredSkills");

    if (!field || !box) {
        return;
    }

    const selectedField =
        field.value;

    const skills =
        requiredSkills[selectedField] || [];

    if (skills.length === 0) {

        box.innerHTML =
            "<b>📌 Required Skills:</b> Select a career field";

        return;
    }

    box.innerHTML =
        "<b>📌 Required Skills:</b> " +
        skills.join(", ");
}


// =====================================================
// ANALYZE STUDENT
// =====================================================

async function analyzeStudent() {

    const nameElement =
        document.getElementById("name");

    const fieldElement =
        document.getElementById("field");

    const skillsElement =
        document.getElementById("skills");


    if (
        !nameElement ||
        !fieldElement ||
        !skillsElement
    ) {

        alert(
            "Required input fields are missing."
        );

        return;
    }


    const name =
        nameElement.value.trim();

    const targetField =
        fieldElement.value;

    const skillsInput =
        skillsElement.value.trim();


    const skills =
        skillsInput
            .split(",")
            .map(skill => skill.trim())
            .filter(skill => skill.length > 0);


    // =================================================
    // VALIDATION
    // =================================================

    if (name === "") {

        alert(
            "Please enter your name."
        );

        nameElement.focus();

        return;
    }


    if (targetField === "") {

        alert(
            "Please select a career field."
        );

        fieldElement.focus();

        return;
    }


    if (skills.length === 0) {

        alert(
            "Please enter at least one skill."
        );

        skillsElement.focus();

        return;
    }


    // Show required skills

    showRequiredSkills();


    // =================================================
    // SEND TO FLASK
    // =================================================

    try {

        const response =
            await fetch(
                "/api/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name: name,

                        skills: skills,

                        target_field:
                            targetField

                    })
                }
            );


        const data =
            await response.json();


        // =================================================
        // ERROR
        // =================================================

        if (!response.ok) {

            alert(
                data.error ||
                "Analysis failed."
            );

            return;
        }


        // =================================================
        // HELLO
        // =================================================

        const hello =
            document.getElementById("hello");

        if (hello) {

            hello.textContent =
                data.name;
        }


        // =================================================
        // TARGET CAREER
        // =================================================

        const target =
            document.getElementById("target");

        if (target) {

            target.textContent =
                data.target_field;
        }


        // =================================================
        // MATCHED COUNT
        // =================================================

        const matchedCount =
            document.getElementById(
                "matchedCount"
            );

        if (matchedCount) {

            matchedCount.textContent =
                data.matched_skills.length;
        }


        // =================================================
        // MISSING COUNT
        // =================================================

        const missingCount =
            document.getElementById(
                "missingCount"
            );

        if (missingCount) {

            missingCount.textContent =
                data.missing_skills.length;
        }


        // =================================================
        // READINESS
        // =================================================

        const readiness =
            document.getElementById(
                "readiness"
            );

        if (readiness) {

            readiness.textContent =
                data.readiness + "%";
        }


        // =================================================
        // MATCHED SKILLS
        // =================================================

        const matched =
            document.getElementById(
                "matched"
            );

        if (matched) {

            if (
                data.matched_skills &&
                data.matched_skills.length > 0
            ) {

                matched.innerHTML =

                    data.matched_skills

                        .map(
                            skill =>
                                `<li>✓ ${skill}</li>`
                        )

                        .join("");

            } else {

                matched.innerHTML =
                    "<li>No matching skills yet.</li>";
            }
        }


        // =================================================
        // MISSING SKILLS
        // =================================================

        const missing =
            document.getElementById(
                "missing"
            );

        if (missing) {

            if (
                data.missing_skills &&
                data.missing_skills.length > 0
            ) {

                missing.innerHTML =

                    data.missing_skills

                        .map(
                            skill =>
                                `<li>✗ ${skill}</li>`
                        )

                        .join("");

            } else {

                missing.innerHTML =
                    "<li>No major skill gaps 🎉</li>";
            }
        }


        // =================================================
        // ROADMAP
        // =================================================

        const roadmap =
            document.getElementById(
                "roadmap"
            );

        if (roadmap) {

            if (
                data.roadmap &&
                data.roadmap.length > 0
            ) {

                roadmap.innerHTML =

                    data.roadmap

                        .map(
                            step =>
                                `<li>${step}</li>`
                        )

                        .join("");

            } else {

                roadmap.innerHTML =
                    "<li>No roadmap available.</li>";
            }
        }


        // =================================================
        // JOBS
        // =================================================

        loadJobs(
            data.target_field
        );


        // =================================================
        // COLLEGE REPORT
        // =================================================

        loadCollegeGaps();


    } catch (error) {

        console.error(
            "Analyze Error:",
            error
        );

        alert(
            "Something went wrong while analyzing your skills."
        );
    }
}


// =====================================================
// LOAD JOBS / INTERNSHIPS
// =====================================================

async function loadJobs(field) {

    try {

        const response =
            await fetch(
                "/api/opportunities?field=" +
                encodeURIComponent(field)
            );


        const jobs =
            await response.json();


        const jobsElement =
            document.getElementById("jobs");


        if (!jobsElement) {
            return;
        }


        if (
            !jobs ||
            jobs.length === 0
        ) {

            jobsElement.innerHTML =
                "<p>No opportunities found.</p>";

            return;
        }


        jobsElement.innerHTML =

            jobs.map(job => `

                <div class="job">

                    <div>

                        <strong>
                            ${job.role}
                        </strong>

                        <br>

                        ${job.company}

                        <br>

                        <small>
                            Required Skills:
                            ${job.skills}
                        </small>

                    </div>

                    <span class="badge">
                        Recommended
                    </span>

                </div>

            `).join("");


    } catch (error) {

        console.error(
            "Jobs Error:",
            error
        );
    }
}


// =====================================================
// COLLEGE SKILL GAP REPORT
// =====================================================

async function loadCollegeGaps() {

    try {

        const response =
            await fetch(
                "/api/college/skill-gaps"
            );


        const gaps =
            await response.json();


        const element =
            document.getElementById(
                "collegeGaps"
            );


        if (!element) {
            return;
        }


        if (
            !gaps ||
            gaps.length === 0
        ) {

            element.innerHTML = `
                <p>
                    No student assessment data yet.
                </p>
            `;

            return;
        }


        element.innerHTML =

            gaps.map(gap => `

                <span class="gap">

                    ${gap.skill_gap}

                    →

                    ${gap.students}
                    student(s)

                </span>

            `).join("");


    } catch (error) {

        console.error(
            "College Gap Error:",
            error
        );
    }
}