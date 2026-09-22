document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // GET STUDENT DATA
    // =====================================================

    const studentData = document.getElementById("studentData");

    if (!studentData) {
        return;
    }

    const targetField =
        studentData.dataset.targetField || "";

    const readiness =
        Number(studentData.dataset.readiness || 0);

    const skillsText =
        studentData.dataset.skills || "";

    const currentSkills =
        skillsText
            .split(",")
            .map(skill => skill.trim())
            .filter(skill => skill.length > 0);


    // =====================================================
    // ELEMENTS
    // =====================================================

    const placementContainer =
        document.getElementById("placementContainer");

    const skillGapBox =
        document.getElementById("skillGapBox");

    const improveMatchButton =
        document.getElementById("improveMatchButton");

    const improvementResult =
        document.getElementById("improvementResult");

    const eligibilityContainer =
        document.getElementById("eligibilityContainer");

    const advisorButton =
        document.getElementById("advisorButton");

    const advisorResult =
        document.getElementById("advisorResult");


    // =====================================================
    // NORMALIZE SKILL
    // =====================================================

    function normalizeSkill(skill) {

        return String(skill)
            .trim()
            .toLowerCase();

    }


    // =====================================================
    // GET APPLICATIONS
    // =====================================================

    function getApplications() {

        try {

            const data =
                localStorage.getItem(
                    "skillbridgeApplications"
                );

            if (!data) {
                return [];
            }

            return JSON.parse(data);

        } catch (error) {

            console.error(
                "Application storage error:",
                error
            );

            return [];

        }

    }


    // =====================================================
    // SAVE APPLICATIONS
    // =====================================================

    function saveApplications(applications) {

        localStorage.setItem(
            "skillbridgeApplications",
            JSON.stringify(applications)
        );

    }


    // =====================================================
    // SHOW READINESS BAR
    // =====================================================

    const readinessProgress =
        document.getElementById(
            "readinessProgress"
        );

    if (readinessProgress) {

        setTimeout(function () {

            readinessProgress.style.width =
                readiness + "%";

        }, 200);

    }


    // =====================================================
    // LOAD SMART JOB MATCH
    // =====================================================

    async function loadPlacements() {

        if (!placementContainer) {
            return;
        }

        placementContainer.innerHTML = `
            <div class="loading-card">
                ⏳ Analyzing your skills...
            </div>
        `;


        try {

            const response =
                await fetch(
                    "/api/placements?field=" +
                    encodeURIComponent(targetField)
                );


            if (!response.ok) {

                throw new Error(
                    "Unable to load placements"
                );

            }


            const placements =
                await response.json();


            if (!placements.length) {

                placementContainer.innerHTML = `
                    <div class="empty-card">

                        <h3>
                            No placement opportunities found
                        </h3>

                        <p>
                            Try selecting another career
                            field from your profile.
                        </p>

                    </div>
                `;

                if (skillGapBox) {

                    skillGapBox.innerHTML = `
                        <div class="empty-card">
                            No skill gap data available.
                        </div>
                    `;

                }

                return;

            }


            const studentSkillSet =
                currentSkills.map(
                    normalizeSkill
                );


            const processed =
                placements.map(
                    placement => {

                        const requiredSkills =
                            placement.skills || [];


                        const matchedSkills =
                            requiredSkills.filter(
                                skill =>
                                    studentSkillSet.includes(
                                        normalizeSkill(skill)
                                    )
                            );


                        const missingSkills =
                            requiredSkills.filter(
                                skill =>
                                    !studentSkillSet.includes(
                                        normalizeSkill(skill)
                                    )
                            );


                        let matchPercentage = 0;


                        if (requiredSkills.length > 0) {

                            matchPercentage =
                                Math.round(
                                    matchedSkills.length /
                                    requiredSkills.length *
                                    100
                                );

                        }


                        return {

                            ...placement,

                            matchedSkills,

                            missingSkills,

                            matchPercentage

                        };

                    }
                );


            processed.sort(
                (a, b) =>
                    b.matchPercentage -
                    a.matchPercentage
            );


            // =================================================
            // DISPLAY PLACEMENTS
            // =================================================

            placementContainer.innerHTML =
                processed.map(
                    (placement, index) => {

                        let matchClass =
                            "low-match";

                        if (
                            placement.matchPercentage >= 70
                        ) {

                            matchClass =
                                "high-match";

                        } else if (
                            placement.matchPercentage >= 40
                        ) {

                            matchClass =
                                "medium-match";

                        }


                        const skillsHTML =
                            placement.skills
                                .map(
                                    skill =>
                                        `<span class="skill-tag">
                                            ${skill}
                                         </span>`
                                )
                                .join("");


                        const missingHTML =
                            placement.missingSkills.length
                                ? placement.missingSkills
                                    .map(
                                        skill =>
                                            `<span class="missing-skill">
                                                ${skill}
                                             </span>`
                                    )
                                    .join("")
                                : `
                                    <span class="matched-all">
                                        ✅ All required skills matched
                                    </span>
                                `;


                        return `

                            <div
                                class="placement-card"
                                data-placement-index="${index}"
                            >

                                <div class="placement-card-top">

                                    <div>

                                        <h3>
                                            🏢 ${placement.company}
                                        </h3>

                                        <h4>
                                            ${placement.role}
                                        </h4>

                                    </div>

                                    <div
                                        class="match-score ${matchClass}"
                                    >

                                        ${placement.matchPercentage}%

                                        <small>
                                            Match
                                        </small>

                                    </div>

                                </div>


                                <div class="placement-info">

                                    <p>
                                        📍 ${placement.location}
                                    </p>

                                    <p>
                                        💰 ${placement.package}
                                    </p>

                                    <p>
                                        🎓 ${placement.experience}
                                    </p>

                                    <p>
                                        📋 ${placement.eligibility}
                                    </p>

                                </div>


                                <div class="placement-skills">

                                    <strong>
                                        Required Skills
                                    </strong>

                                    <div>
                                        ${skillsHTML}
                                    </div>

                                </div>


                                <div class="placement-match-details">

                                    <strong>
                                        Skill Analysis
                                    </strong>

                                    <p>
                                        ✅ Matched:
                                        ${
                                            placement.matchedSkills.length
                                        }
                                        /
                                        ${
                                            placement.skills.length
                                        }
                                    </p>

                                    <div>
                                        ${missingHTML}
                                    </div>

                                </div>


                                <div class="placement-actions">

                                    <button
                                        type="button"
                                        class="apply-placement-button"
                                        data-company="${placement.company}"
                                        data-role="${placement.role}"
                                    >

                                        📤 Apply

                                    </button>


                                    <button
                                        type="button"
                                        class="eligibility-button"
                                        data-placement-index="${index}"
                                    >

                                        ✅ Check Eligibility

                                    </button>

                                </div>

                            </div>

                        `;

                    }
                )
                .join("");


            // =================================================
            // STORE PROCESSED DATA
            // =================================================

            window.skillBridgePlacements =
                processed;


            // =================================================
            // APPLICATION BUTTONS
            // =================================================

            document
                .querySelectorAll(
                    ".apply-placement-button"
                )
                .forEach(
                    button => {

                        button.addEventListener(
                            "click",
                            function () {

                                const company =
                                    this.dataset.company;

                                const role =
                                    this.dataset.role;


                                addApplication(
                                    company,
                                    role
                                );

                            }
                        );

                    }
                );


            // =================================================
            // ELIGIBILITY BUTTONS
            // =================================================

            document
                .querySelectorAll(
                    ".eligibility-button"
                )
                .forEach(
                    button => {

                        button.addEventListener(
                            "click",
                            function () {

                                const index =
                                    Number(
                                        this.dataset
                                            .placementIndex
                                    );


                                checkEligibility(
                                    processed[index]
                                );

                            }
                        );

                    }
                );


            // =================================================
            // SKILL GAP
            // =================================================

            showSkillGap(processed);


            // =================================================
            // ELIGIBILITY SUMMARY
            // =================================================

            showEligibilitySummary(processed);

        } catch (error) {

            console.error(error);

            placementContainer.innerHTML = `

                <div class="empty-card">

                    <h3>
                        ⚠️ Could not load placements
                    </h3>

                    <p>
                        Please refresh the page and try again.
                    </p>

                </div>

            `;

        }

    }


    // =====================================================
    // SHOW SKILL GAP
    // =====================================================

    function showSkillGap(placements) {

        if (!skillGapBox) {
            return;
        }


        const gapMap = {};


        placements.forEach(
            placement => {

                placement.missingSkills
                    .forEach(
                        skill => {

                            const key =
                                normalizeSkill(skill);


                            if (!gapMap[key]) {

                                gapMap[key] = {

                                    name: skill,

                                    count: 0

                                };

                            }


                            gapMap[key].count++;

                        }
                    );

            }
        );


        const gaps =
            Object.values(gapMap)
                .sort(
                    (a, b) =>
                        b.count - a.count
                );


        if (!gaps.length) {

            skillGapBox.innerHTML = `

                <div class="success-card">

                    <h3>
                        🎉 No Major Skill Gaps
                    </h3>

                    <p>
                        Your current skills match
                        the available placement requirements.
                    </p>

                </div>

            `;

            return;

        }


        skillGapBox.innerHTML = `

            <div class="skill-gap-list">

                ${

                    gaps.map(
                        gap => `

                            <div class="skill-gap-item">

                                <div>

                                    <strong>
                                        ${gap.name}
                                    </strong>

                                    <p>
                                        Missing for
                                        ${gap.count}
                                        placement(s)
                                    </p>

                                </div>

                                <span>
                                    ❌
                                </span>

                            </div>

                        `
                    ).join("")

                }

            </div>

        `;

    }


    // =====================================================
    // IMPROVE MY MATCH
    // =====================================================

    if (improveMatchButton) {

        improveMatchButton.addEventListener(
            "click",
            function () {

                improveMatchButton.disabled =
                    true;

                improveMatchButton.textContent =
                    "⏳ Creating Improvement Plan...";


                setTimeout(
                    function () {

                        const placements =
                            window.skillBridgePlacements ||
                            [];


                        const missing = {};


                        placements.forEach(
                            placement => {

                                placement.missingSkills
                                    .forEach(
                                        skill => {

                                            const key =
                                                normalizeSkill(
                                                    skill
                                                );


                                            if (!missing[key]) {

                                                missing[key] = {

                                                    name: skill,

                                                    count: 0

                                                };

                                            }


                                            missing[key].count++;

                                        }
                                    );

                            }
                        );


                        const sortedSkills =
                            Object.values(missing)
                                .sort(
                                    (a, b) =>
                                        b.count -
                                        a.count
                                );


                        if (!sortedSkills.length) {

                            improvementResult.innerHTML = `

                                <div class="success-card">

                                    <h3>
                                        🎉 You are already well matched!
                                    </h3>

                                    <p>
                                        Focus now on aptitude,
                                        interviews and resume preparation.
                                    </p>

                                </div>

                            `;

                        } else {

                            improvementResult.innerHTML = `

                                <div class="improvement-plan">

                                    <h3>
                                        🚀 Your Recommended Plan
                                    </h3>

                                    <p>
                                        Learn these skills in
                                        priority order:
                                    </p>

                                    <ol>

                                        ${
                                            sortedSkills
                                                .slice(0, 6)
                                                .map(
                                                    (skill, index) => `

                                                        <li>

                                                            <strong>
                                                                ${skill.name}
                                                            </strong>

                                                            <span>
                                                                Important for
                                                                ${skill.count}
                                                                placement(s)
                                                            </span>

                                                        </li>

                                                    `
                                                )
                                                .join("")
                                        }

                                    </ol>


                                    <div class="plan-tip">

                                        💡
                                        Start with the skill
                                        appearing in the most
                                        placement requirements.

                                    </div>

                                </div>

                            `;

                        }


                        improveMatchButton.disabled =
                            false;

                        improveMatchButton.textContent =
                            "🚀 Improve My Match";


                        improvementResult.scrollIntoView(
                            {
                                behavior: "smooth",
                                block: "center"
                            }
                        );

                    },
                    500
                );

            }
        );

    }


    // =====================================================
    // PLACEMENT DRIVE COUNTDOWN
    // =====================================================

    function startCountdown() {

        const companyElement =
            document.getElementById(
                "countdownCompany"
            );


        const daysElement =
            document.getElementById(
                "countDays"
            );

        const hoursElement =
            document.getElementById(
                "countHours"
            );

        const minutesElement =
            document.getElementById(
                "countMinutes"
            );

        const secondsElement =
            document.getElementById(
                "countSeconds"
            );


        if (
            !daysElement ||
            !hoursElement ||
            !minutesElement ||
            !secondsElement
        ) {

            return;

        }


        // Demo upcoming drive.
        // Automatically changes to next occurrence.

        const now =
            new Date();


        const drive =
            new Date();

        drive.setDate(
            drive.getDate() + 12
        );

        drive.setHours(
            10,
            0,
            0,
            0
        );


        if (companyElement) {

            companyElement.textContent =
                "TCS Campus Placement Drive • Upcoming";

        }


        function updateCountdown() {

            const current =
                new Date();

            const difference =
                drive - current;


            if (difference <= 0) {

                daysElement.textContent = "0";

                hoursElement.textContent = "0";

                minutesElement.textContent = "0";

                secondsElement.textContent = "0";

                return;

            }


            const days =
                Math.floor(
                    difference /
                    (1000 * 60 * 60 * 24)
                );


            const hours =
                Math.floor(
                    (
                        difference %
                        (1000 * 60 * 60 * 24)
                    ) /
                    (1000 * 60 * 60)
                );


            const minutes =
                Math.floor(
                    (
                        difference %
                        (1000 * 60 * 60)
                    ) /
                    (1000 * 60)
                );


            const seconds =
                Math.floor(
                    (
                        difference %
                        (1000 * 60)
                    ) /
                    1000
                );


            daysElement.textContent =
                String(days).padStart(2, "0");

            hoursElement.textContent =
                String(hours).padStart(2, "0");

            minutesElement.textContent =
                String(minutes).padStart(2, "0");

            secondsElement.textContent =
                String(seconds).padStart(2, "0");

        }


        updateCountdown();


        setInterval(
            updateCountdown,
            1000
        );

    }


    // =====================================================
    // ELIGIBILITY SUMMARY
    // =====================================================

    function showEligibilitySummary(placements) {

        if (!eligibilityContainer) {
            return;
        }


        const html =
            placements
                .map(
                    placement => {

                        const eligible =
                            placement.missingSkills.length === 0;


                        return `

                            <div class="eligibility-card">

                                <div>

                                    <h3>
                                        🏢 ${placement.company}
                                    </h3>

                                    <p>
                                        ${placement.role}
                                    </p>

                                </div>


                                <div>

                                    ${
                                        eligible

                                        ?

                                        `<span class="eligible">
                                            ✅ Eligible
                                         </span>`

                                        :

                                        `<span class="not-eligible">
                                            ❌ ${placement.missingSkills.length}
                                            skill(s) missing
                                         </span>`
                                    }

                                </div>

                            </div>

                        `;

                    }
                )
                .join("");


        eligibilityContainer.innerHTML =
            html;

    }


    // =====================================================
    // CHECK ONE ELIGIBILITY
    // =====================================================

    function checkEligibility(placement) {

        if (!eligibilityContainer) {
            return;
        }


        const eligible =
            placement.missingSkills.length === 0;


        let message;


        if (eligible) {

            message = `

                <div class="success-card">

                    <h3>
                        🎉 You are eligible for
                        ${placement.company}
                    </h3>

                    <p>
                        Your current skills match all
                        listed technical requirements
                        for ${placement.role}.
                    </p>

                </div>

            `;

        } else {

            message = `

                <div class="warning-card">

                    <h3>
                        ⚠️ Not fully eligible yet
                    </h3>

                    <p>
                        Improve these skills:
                    </p>

                    <div>

                        ${
                            placement.missingSkills
                                .map(
                                    skill =>
                                        `<span class="missing-skill">
                                            ${skill}
                                         </span>`
                                )
                                .join("")
                        }

                    </div>

                </div>

            `;

        }


        eligibilityContainer.innerHTML =
            message;


        eligibilityContainer.scrollIntoView(
            {
                behavior: "smooth",
                block: "center"
            }
        );

    }


    // =====================================================
    // ADD APPLICATION
    // =====================================================

    function addApplication(
        company,
        role
    ) {

        const applications =
            getApplications();


        const alreadyApplied =
            applications.some(
                app =>
                    app.company === company &&
                    app.role === role
            );


        if (alreadyApplied) {

            alert(
                "You have already applied for this placement."
            );

            return;

        }


        const application = {

            id:
                Date.now(),

            company:
                company,

            role:
                role,

            appliedAt:
                new Date().toLocaleString(),

            status:
                "Applied"

        };


        applications.push(
            application
        );


        saveApplications(
            applications
        );


        renderApplications();


        alert(
            "Application submitted successfully!"
        );

    }


    // =====================================================
    // RENDER APPLICATIONS
    // =====================================================

    function renderApplications() {

        const applications =
            getApplications();


        const appliedCount =
            document.getElementById(
                "appliedCount"
            );

        const shortlistedCount =
            document.getElementById(
                "shortlistedCount"
            );

        const interviewCount =
            document.getElementById(
                "interviewCount"
            );

        const selectedCount =
            document.getElementById(
                "selectedCount"
            );

        const applicationList =
            document.getElementById(
                "applicationList"
            );


        if (!applicationList) {
            return;
        }


        // COUNTS

        if (appliedCount) {

            appliedCount.textContent =
                applications.length;

        }


        if (shortlistedCount) {

            shortlistedCount.textContent =
                applications.filter(
                    app =>
                        app.status === "Shortlisted"
                ).length;

        }


        if (interviewCount) {

            interviewCount.textContent =
                applications.filter(
                    app =>
                        app.status === "Interview"
                ).length;

        }


        if (selectedCount) {

            selectedCount.textContent =
                applications.filter(
                    app =>
                        app.status === "Selected"
                ).length;

        }


        // EMPTY

        if (!applications.length) {

            applicationList.innerHTML = `

                <div class="no-applications">

                    <h3>
                        No Applications Yet
                    </h3>

                    <p>
                        Apply to a placement opportunity
                        above and your application will
                        appear here.
                    </p>

                </div>

            `;

            return;

        }


        // APPLICATIONS

        applicationList.innerHTML =
            applications
                .map(
                    app => `

                        <div
                            class="application-card"
                            data-id="${app.id}"
                        >

                            <div>

                                <h3>
                                    🏢 ${app.company}
                                </h3>

                                <p>
                                    ${app.role}
                                </p>

                                <small>
                                    Applied:
                                    ${app.appliedAt}
                                </small>

                            </div>


                            <div class="application-status">

                                <select
                                    class="status-select"
                                    data-id="${app.id}"
                                >

                                    <option
                                        value="Applied"
                                        ${
                                            app.status ===
                                            "Applied"
                                                ? "selected"
                                                : ""
                                        }
                                    >
                                        Applied
                                    </option>


                                    <option
                                        value="Shortlisted"
                                        ${
                                            app.status ===
                                            "Shortlisted"
                                                ? "selected"
                                                : ""
                                        }
                                    >
                                        Shortlisted
                                    </option>


                                    <option
                                        value="Interview"
                                        ${
                                            app.status ===
                                            "Interview"
                                                ? "selected"
                                                : ""
                                        }
                                    >
                                        Interview
                                    </option>


                                    <option
                                        value="Selected"
                                        ${
                                            app.status ===
                                            "Selected"
                                                ? "selected"
                                                : ""
                                        }
                                    >
                                        Selected
                                    </option>

                                </select>


                                <button
                                    type="button"
                                    class="delete-application"
                                    data-id="${app.id}"
                                >
                                    🗑️ Remove
                                </button>

                            </div>

                        </div>

                    `
                )
                .join("");


        // STATUS CHANGE

        document
            .querySelectorAll(
                ".status-select"
            )
            .forEach(
                select => {

                    select.addEventListener(
                        "change",
                        function () {

                            const id =
                                Number(
                                    this.dataset.id
                                );


                            const applications =
                                getApplications();


                            const application =
                                applications.find(
                                    app =>
                                        app.id === id
                                );


                            if (application) {

                                application.status =
                                    this.value;

                            }


                            saveApplications(
                                applications
                            );


                            renderApplications();

                        }
                    );

                }
            );


        // DELETE

        document
            .querySelectorAll(
                ".delete-application"
            )
            .forEach(
                button => {

                    button.addEventListener(
                        "click",
                        function () {

                            const id =
                                Number(
                                    this.dataset.id
                                );


                            const applications =
                                getApplications()
                                    .filter(
                                        app =>
                                            app.id !== id
                                    );


                            saveApplications(
                                applications
                            );


                            renderApplications();

                        }
                    );

                }
            );

    }


    // =====================================================
    // PLACEMENT AI ADVISOR
    // =====================================================

    if (advisorButton) {

        advisorButton.addEventListener(
            "click",
            function () {

                advisorButton.disabled =
                    true;

                advisorButton.textContent =
                    "⏳ Preparing Advice...";


                setTimeout(
                    function () {

                        let advice = "";


                        // LOW READINESS

                        if (readiness < 40) {

                            advice = `

                                <div class="advisor-message">

                                    <h3>
                                        🔴 Your placement preparation needs improvement
                                    </h3>

                                    <p>
                                        Your current technical readiness is
                                        <strong>
                                            ${readiness}%
                                        </strong>.
                                    </p>

                                    <h4>
                                        Recommended Plan
                                    </h4>

                                    <ol>

                                        <li>
                                            Focus on your missing technical skills first.
                                        </li>

                                        <li>
                                            Practice aptitude questions every day.
                                        </li>

                                        <li>
                                            Prepare common HR interview questions.
                                        </li>

                                        <li>
                                            Improve your resume with projects and skills.
                                        </li>

                                        <li>
                                            Build at least one strong
                                            ${targetField} project.
                                        </li>

                                        <li>
                                            Apply actively after improving your skill match.
                                        </li>

                                    </ol>

                                </div>

                            `;

                        }


                        // MEDIUM READINESS

                        else if (readiness < 70) {

                            advice = `

                                <div class="advisor-message">

                                    <h3>
                                        🟡 You are progressing well
                                    </h3>

                                    <p>
                                        Your readiness is
                                        <strong>
                                            ${readiness}%
                                        </strong>.
                                    </p>

                                    <h4>
                                        Recommended Plan
                                    </h4>

                                    <ol>

                                        <li>
                                            Complete your remaining skill gaps.
                                        </li>

                                        <li>
                                            Build at least one strong
                                            ${targetField} project.
                                        </li>

                                        <li>
                                            Practice aptitude and coding regularly.
                                        </li>

                                        <li>
                                            Start preparing for technical interviews.
                                        </li>

                                        <li>
                                            Improve your resume and LinkedIn profile.
                                        </li>

                                    </ol>

                                </div>

                            `;

                        }


                        // HIGH READINESS

                        else {

                            advice = `

                                <div class="advisor-message">

                                    <h3>
                                        🟢 You are placement ready!
                                    </h3>

                                    <p>
                                        Your readiness is
                                        <strong>
                                            ${readiness}%
                                        </strong>.
                                    </p>

                                    <h4>
                                        Recommended Plan
                                    </h4>

                                    <ol>

                                        <li>
                                            Start applying actively.
                                        </li>

                                        <li>
                                            Practice technical interview questions.
                                        </li>

                                        <li>
                                            Prepare your project explanation.
                                        </li>

                                        <li>
                                            Practice HR interviews.
                                        </li>

                                        <li>
                                            Track every application through SkillBridge.
                                        </li>

                                    </ol>

                                </div>

                            `;

                        }


                        advisorResult.innerHTML =
                            advice;


                        advisorButton.disabled =
                            false;

                        advisorButton.textContent =
                            "🧠 Get My Advice";


                        advisorResult.scrollIntoView(
                            {
                                behavior: "smooth",
                                block: "center"
                            }
                        );


                    },
                    700
                );

            }
        );

    }


    // =====================================================
    // START
    // =====================================================

    loadPlacements();

    startCountdown();

    renderApplications();

});