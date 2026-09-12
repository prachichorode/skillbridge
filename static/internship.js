document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("internshipContainer");
    const studentData = document.getElementById("studentData");

    if (!container) {
        return;
    }

    if (!studentData) {

        container.innerHTML = `
            <div class="empty-box">
                Please create your profile first.
            </div>
        `;

        return;
    }

    const targetField = studentData.dataset.targetField;

    fetch(
        "/api/opportunities?field=" +
        encodeURIComponent(targetField)
    )

    .then(response => {

        if (!response.ok) {
            throw new Error("Failed to load internships");
        }

        return response.json();

    })

    .then(data => {

        container.innerHTML = "";

        if (!data || data.length === 0) {

            container.innerHTML = `
                <div class="empty-box">
                    No internships found for ${targetField}.
                </div>
            `;

            return;
        }

        data.forEach(internship => {

            const card = document.createElement("div");

            card.className = "internship-card";

            const skills = Array.isArray(internship.skills)
                ? internship.skills
                : String(internship.skills || "")
                    .split(",")
                    .map(skill => skill.trim())
                    .filter(Boolean);

            card.innerHTML = `

                <div class="company-name">
                    ${internship.company || "Company"}
                </div>

                <h2>
                    ${internship.role || "Internship"}
                </h2>

                <span class="internship-field">
                    ${internship.field || targetField}
                </span>

                <div class="required-skills">

                    <h3>
                        Required Skills
                    </h3>

                    <div class="profile-skills">

                        ${skills.map(skill => `
                            <span class="skill-tag">
                                ${skill}
                            </span>
                        `).join("")}

                    </div>

                </div>

                <div class="internship-action">

                    <a
                        href="/internship/${internship.id}"
                        class="apply-btn">

                        Apply Now →

                    </a>

                </div>
            `;

            container.appendChild(card);

        });

    })

    .catch(error => {

        console.error(error);

        container.innerHTML = `

            <div class="empty-box">

                Unable to load internships.

                <br><br>

                Please try again.

            </div>

        `;

    });

});