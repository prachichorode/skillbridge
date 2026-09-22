from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3
import os
import uuid

import psycopg
from psycopg.rows import dict_row


# =====================================================
# APP CONFIGURATION
# =====================================================

app = Flask(__name__)

app.secret_key = "skillbridge-secret-key"

DB = "skillbridge.db"

UPLOAD_FOLDER = "/tmp/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =====================================================
# 1. INDUSTRY REQUIRED SKILLS
# =====================================================

FIELD_SKILLS = {

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
}


# =====================================================
# 2. PERSONALIZED ROADMAP
# =====================================================

ROADMAP = {

    "Data Analyst": [
        "Learn SQL",
        "Learn Excel",
        "Learn Statistics",
        "Learn Power BI",
        "Learn Data Visualization",
        "Build Data Analysis Project"
    ],

    "Data Scientist": [
        "Learn Python for Data Science",
        "Learn NumPy and Pandas",
        "Learn Statistics",
        "Learn Machine Learning",
        "Learn Model Evaluation",
        "Build ML Project"
    ],

    "Business Intelligence": [
        "Learn SQL",
        "Learn Excel",
        "Learn Power BI",
        "Learn DAX",
        "Learn Data Modeling",
        "Build BI Dashboard"
    ],

    "Software Engineer": [
        "Learn HTML and CSS",
        "Learn JavaScript",
        "Learn Git and GitHub",
        "Learn DSA",
        "Learn Backend/API",
        "Build Full Stack Project"
    ]
}


# =====================================================
# 3. INTERNSHIP DATA
# =====================================================

OPPORTUNITIES = [

    {
        "company": "TCS",
        "role": "Data Analyst Intern",
        "field": "Data Analyst",
        "location": "Pune, India",
        "duration": "8 weeks",
        "stipend": "Not publicly specified",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current TCS opening",

        "skills": [
            "SQL",
            "Excel",
            "Power BI"
        ],

        "responsibilities": [
            "Analyze and clean datasets",
            "Prepare reports and dashboards",
            "Support data-driven business decisions"
        ],

        "learn": [
            "SQL",
            "Excel",
            "Power BI",
            "Data Analysis"
        ]
    },

    {
        "company": "Infosys",
        "role": "Software Developer Intern",
        "field": "Software Engineer",
        "location": "Bengaluru, India",
        "duration": "8 weeks",
        "stipend": "Not publicly specified",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current Infosys opening",

        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python"
        ],

        "responsibilities": [
            "Develop and maintain software applications",
            "Write and test application code",
            "Work with development teams",
            "Debug and improve software functionality"
        ],

        "learn": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "Software Development"
        ]
    },

    {
        "company": "Wipro",
        "role": "AI/ML Intern",
        "field": "Data Scientist",
        "location": "Bengaluru, India",
        "duration": "8 weeks",
        "stipend": "Not publicly specified",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current Wipro opening",

        "skills": [
            "Python",
            "Machine Learning",
            "Pandas"
        ],

        "responsibilities": [
            "Prepare and analyze datasets",
            "Build basic machine learning models",
            "Support AI and ML experiments"
        ],

        "learn": [
            "Python",
            "Pandas",
            "Machine Learning",
            "Data Analysis"
        ]
    },

    {
        "company": "Accenture",
        "role": "BI Intern",
        "field": "Business Intelligence",
        "location": "Mumbai, India",
        "duration": "8 weeks",
        "stipend": "Not publicly specified",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current Accenture opening",

        "skills": [
            "SQL",
            "Power BI",
            "DAX"
        ],

        "responsibilities": [
            "Create business intelligence reports",
            "Build dashboards",
            "Analyze business data",
            "Support reporting activities"
        ],

        "learn": [
            "SQL",
            "Power BI",
            "DAX",
            "Business Intelligence"
        ]
    }
]


# =====================================================
# 4. INTERNSHIP EXTRA DETAILS
# =====================================================

INTERNSHIP_DETAILS = {

    "Infosys": {
        "location": "Bengaluru, India",
        "duration": "8 weeks",
        "stipend": "Not publicly specified",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current Infosys opening",

        "responsibilities": [
            "Assist in software development and coding tasks.",
            "Work with HTML, CSS, JavaScript and Python.",
            "Support the development and testing of applications.",
            "Collaborate with team members on assigned projects."
        ],

        "learning": [
            "Practical software development",
            "Frontend development using HTML and CSS",
            "JavaScript programming",
            "Python programming",
            "Team collaboration and project development"
        ]
    },

    "TCS": {
        "location": "India",
        "duration": "8 weeks",
        "stipend": "As per current opening",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current TCS opening",

        "responsibilities": [
            "Work on data analysis tasks.",
            "Prepare and analyze datasets.",
            "Create reports and dashboards."
        ],

        "learning": [
            "SQL",
            "Excel",
            "Power BI",
            "Data analysis"
        ]
    },

    "Wipro": {
        "location": "India",
        "duration": "8 weeks",
        "stipend": "As per current opening",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current Wipro opening",

        "responsibilities": [
            "Assist with AI and machine learning projects.",
            "Work with Python and data processing.",
            "Support model development and testing."
        ],

        "learning": [
            "Python",
            "Pandas",
            "Machine Learning",
            "AI project development"
        ]
    },

    "Accenture": {
        "location": "India",
        "duration": "8 weeks",
        "stipend": "As per current opening",
        "eligibility": "Students / eligible university candidates",
        "deadline": "Check current Accenture opening",

        "responsibilities": [
            "Work with business intelligence data.",
            "Prepare dashboards and reports.",
            "Support data-driven business analysis."
        ],

        "learning": [
            "SQL",
            "Power BI",
            "DAX",
            "Business Intelligence"
        ]
    }
}


# =====================================================
# 5. PLACEMENT DATA
# =====================================================

PLACEMENTS = [

    {
        "company": "TCS",
        "role": "Data Analyst",
        "field": "Data Analyst",
        "location": "Mumbai / Pune",
        "package": "4.5 - 7 LPA",
        "experience": "Freshers",
        "skills": [
            "SQL",
            "Excel",
            "Power BI"
        ],
        "eligibility": "B.Tech / B.E / B.Sc"
    },

    {
        "company": "Infosys",
        "role": "Data Analyst",
        "field": "Data Analyst",
        "location": "Pune / Bengaluru",
        "package": "5 - 8 LPA",
        "experience": "Freshers",
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Statistics"
        ],
        "eligibility": "B.Tech / B.E"
    },

    {
        "company": "Accenture",
        "role": "Business Intelligence Analyst",
        "field": "Business Intelligence",
        "location": "Pune / Bengaluru",
        "package": "5 - 9 LPA",
        "experience": "Freshers",
        "skills": [
            "SQL",
            "Power BI",
            "DAX",
            "Data Modeling"
        ],
        "eligibility": "B.Tech / B.E / MCA"
    },

    {
        "company": "Wipro",
        "role": "BI Developer",
        "field": "Business Intelligence",
        "location": "Pune / Hyderabad",
        "package": "4.5 - 7.5 LPA",
        "experience": "Freshers",
        "skills": [
            "SQL",
            "Power BI",
            "DAX"
        ],
        "eligibility": "B.Tech / B.E"
    },

    {
        "company": "Deloitte",
        "role": "Business Intelligence Analyst",
        "field": "Business Intelligence",
        "location": "Mumbai / Pune",
        "package": "6 - 10 LPA",
        "experience": "Freshers",
        "skills": [
            "SQL",
            "Power BI",
            "Excel",
            "Data Visualization"
        ],
        "eligibility": "B.Tech / B.E / MCA"
    },

    {
        "company": "TCS",
        "role": "Software Engineer",
        "field": "Software Engineer",
        "location": "Pune / Bengaluru",
        "package": "4 - 8 LPA",
        "experience": "Freshers",
        "skills": [
            "Python",
            "JavaScript",
            "SQL",
            "DSA",
            "Git"
        ],
        "eligibility": "B.Tech / B.E"
    },

    {
        "company": "Infosys",
        "role": "Software Developer",
        "field": "Software Engineer",
        "location": "Bengaluru / Hyderabad",
        "package": "5 - 8 LPA",
        "experience": "Freshers",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "Git"
        ],
        "eligibility": "B.Tech / B.E / MCA"
    },

    {
        "company": "Wipro",
        "role": "Machine Learning Engineer",
        "field": "Data Scientist",
        "location": "Bengaluru / Hyderabad",
        "package": "5 - 9 LPA",
        "experience": "Freshers",
        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy"
        ],
        "eligibility": "B.Tech / B.E"
    },

    {
        "company": "Accenture",
        "role": "Data Scientist",
        "field": "Data Scientist",
        "location": "Pune / Bengaluru",
        "package": "6 - 10 LPA",
        "experience": "Freshers",
        "skills": [
            "Python",
            "Machine Learning",
            "SQL",
            "Statistics"
        ],
        "eligibility": "B.Tech / B.E / MCA"
    }
]


# =====================================================
# 6. DATABASE CONNECTION
# =====================================================
def get_db():
    conn = psycopg.connect(
        os.environ["DATABASE_URL"],
        row_factory=dict_row
    )
    return conn


# =====================================================
# 7. INITIALIZE DATABASE
# =====================================================

def init_db():

    conn = get_db()

    # -------------------------------------------------
    # STUDENTS
    # -------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name TEXT NOT NULL,
            skills TEXT NOT NULL,
            target_field TEXT NOT NULL
        )
    """)

    # -------------------------------------------------
    # OPPORTUNITIES
    # -------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            company TEXT,
            role TEXT,
            field TEXT,
            skills TEXT
        )
    """)

    # -------------------------------------------------
    # USERS
    # -------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # -------------------------------------------------
    # APPLICATIONS
    # -------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS internship_applications (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            internship_id INTEGER,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            college TEXT NOT NULL,
            branch TEXT,
            year TEXT,
            skills TEXT,
            resume TEXT,
            cover_message TEXT,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -------------------------------------------------
    # INSERT INTERNSHIPS ONLY IF TABLE IS EMPTY
    # -------------------------------------------------

    count = conn.execute(
        "SELECT COUNT(*) AS count FROM opportunities"
    ).fetchone()["count"]

    if count == 0:

        for opportunity in OPPORTUNITIES:

            conn.execute(
                """
                INSERT INTO opportunities
                (company, role, field, skills)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    opportunity["company"],
                    opportunity["role"],
                    opportunity["field"],
                    ", ".join(opportunity["skills"])
                )
            )

    # -------------------------------------------------
    # DEMO LOGIN
    # -------------------------------------------------

    existing_user = conn.execute(
        """
        SELECT id
        FROM users
        WHERE email = %s
        """,
        ("prachi@skillbridge.com",)
    ).fetchone()

    if existing_user is None:

        conn.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (
                "Prachi",
                "prachi@skillbridge.com",
                generate_password_hash("123456")
            )
        )

    conn.commit()
    conn.close()

# =====================================================
# 8. NORMALIZE SKILLS
# =====================================================

def normalize_skills(skills):

    if isinstance(skills, str):

        skills = skills.split(",")

    result = {}

    for skill in skills:

        skill = str(skill).strip()

        if skill:

            result[skill.lower()] = skill

    return result


# =====================================================
# 9. ANALYZE SKILLS
# =====================================================

def analyze(skills, target_field):

    student_skills = normalize_skills(skills)

    required_skills = FIELD_SKILLS.get(
        target_field,
        []
    )

    matched = []

    missing = []

    for skill in required_skills:

        if skill.lower() in student_skills:

            matched.append(skill)

        else:

            missing.append(skill)

    if required_skills:

        readiness = round(
            len(matched) /
            len(required_skills) *
            100
        )

    else:

        readiness = 0

    return matched, missing, readiness


# =====================================================
# 10. LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        conn = get_db()

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session["user_id"] = user["id"]

            session["name"] = user["name"]

            session["email"] = user["email"]

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


# =====================================================
# 11. REGISTER
# =====================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not password:

            return render_template(
                "register.html",
                error="Please fill all fields."
            )

        if len(password) < 6:

            return render_template(
                "register.html",
                error="Password must be at least 6 characters."
            )

        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        conn = get_db()

        existing_user = conn.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if existing_user:

            conn.close()

            return render_template(
                "register.html",
                error="An account with this email already exists."
            )

        conn.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                generate_password_hash(password)
            )
        )

        conn.commit()

        conn.close()

        return redirect(
            url_for("login")
        )

    return render_template("register.html")


# =====================================================
# 12. LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =====================================================
# 13. DASHBOARD
# =====================================================

@app.route("/")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard.html",
        fields=list(FIELD_SKILLS.keys())
    )


# =====================================================
# 14. PROFILE
# =====================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    if student is None:

        return render_template(
            "profile.html",
            student=None,
            matched=[],
            missing=[],
            readiness=0
        )

    skills = [
        skill.strip()
        for skill in student["skills"].split(",")
        if skill.strip()
    ]

    matched, missing, readiness = analyze(
        skills,
        student["target_field"]
    )

    return render_template(
        "profile.html",
        student=student,
        matched=matched,
        missing=missing,
        readiness=readiness
    )


# =====================================================
# 15. ANALYZE API
# =====================================================

@app.route("/api/analyze", methods=["POST"])
def api_analyze():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "No data received."
        }), 400

    name = str(
        data.get(
            "name",
            "Student"
        )
    ).strip()

    skills = data.get(
        "skills",
        []
    )

    if isinstance(skills, str):

        skills = skills.split(",")

    skills = [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]

    target_field = data.get(
        "target_field"
    )

    if target_field not in FIELD_SKILLS:

        return jsonify({
            "error": "Please select a valid career field."
        }), 400

    if not skills:

        return jsonify({
            "error": "Please enter at least one skill."
        }), 400

    matched, missing, readiness = analyze(
        skills,
        target_field
    )

    conn = get_db()

    conn.execute(
        """
        INSERT INTO students
        (name, skills, target_field)
        VALUES (?, ?, ?)
        """,
        (
            name,
            ", ".join(skills),
            target_field
        )
    )

    conn.commit()

    conn.close()

    return jsonify({

        "name": name,

        "target_field": target_field,

        "matched_skills": matched,

        "missing_skills": missing,

        "readiness": readiness,

        "roadmap": ROADMAP.get(
            target_field,
            []
        )
    })


# =====================================================
# 16. INTERNSHIP API
# =====================================================

@app.route("/api/opportunities")
def opportunities():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    field = request.args.get(
        "field",
        ""
    ).strip()

    conn = get_db()

    if field:

        rows = conn.execute(
            """
            SELECT
                id,
                company,
                role,
                field,
                skills
            FROM opportunities
            WHERE field = ?
            """,
            (field,)
        ).fetchall()

    else:

        rows = conn.execute(
            """
            SELECT
                id,
                company,
                role,
                field,
                skills
            FROM opportunities
            """
        ).fetchall()

    conn.close()

    result = []

    for row in rows:

        result.append({

            "id": row["id"],

            "company": row["company"],

            "role": row["role"],

            "field": row["field"],

            "skills": [
                skill.strip()
                for skill in row["skills"].split(",")
                if skill.strip()
            ]
        })

    return jsonify(result)


# =====================================================
# 17. COLLEGE SKILL GAP
# =====================================================

@app.route("/api/college/skill-gaps")
def college_skill_gaps():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    conn = get_db()

    students = conn.execute(
        """
        SELECT skills, target_field
        FROM students
        """
    ).fetchall()

    conn.close()

    skill_gap_count = {}

    for student in students:

        field = student["target_field"]

        student_skills = [
            skill.strip().lower()
            for skill in student["skills"].split(",")
            if skill.strip()
        ]

        required_skills = FIELD_SKILLS.get(
            field,
            []
        )

        for required_skill in required_skills:

            if required_skill.lower() not in student_skills:

                key = (
                    f"{field} | {required_skill}"
                )

                skill_gap_count[key] = (
                    skill_gap_count.get(key, 0) + 1
                )

    result = []

    for skill_gap, students_count in sorted(
        skill_gap_count.items(),
        key=lambda x: -x[1]
    ):

        result.append({

            "skill_gap": skill_gap,

            "students": students_count
        })

    return jsonify(result)


# =====================================================
# 18. SKILL MAPPING
# =====================================================

@app.route("/skill-mapping")
def skill_mapping():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    if student is None:

        return render_template(
            "skill_mapping.html",
            student=None,
            current_skills=[],
            required_skills=[],
            matched_skills=[],
            missing_skills=[],
            readiness=0
        )

    current_skills = [
        skill.strip()
        for skill in student["skills"].split(",")
        if skill.strip()
    ]

    matched_skills, missing_skills, readiness = analyze(
        current_skills,
        student["target_field"]
    )

    required_skills = FIELD_SKILLS.get(
        student["target_field"],
        []
    )

    return render_template(
        "skill_mapping.html",
        student=student,
        current_skills=current_skills,
        required_skills=required_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        readiness=readiness
    )


# =====================================================
# 19. ROADMAP
# =====================================================

@app.route("/roadmap")
def roadmap():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    if student is None:

        return render_template(
            "roadmap.html",
            student=None,
            roadmap=[]
        )

    roadmap_steps = ROADMAP.get(
        student["target_field"],
        []
    )

    return render_template(
        "roadmap.html",
        student=student,
        roadmap=roadmap_steps
    )


# =====================================================
# 20. INTERNSHIP LIST PAGE
# =====================================================

@app.route("/internship")
def internship():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    return render_template(
        "internship.html",
        student=student
    )


# =====================================================
# 21. INTERNSHIP DETAIL PAGE
# =====================================================

@app.route("/internship/<int:company_id>")
def internship_detail(company_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    internship = conn.execute(
        """
        SELECT
            id,
            company,
            role,
            field,
            skills
        FROM opportunities
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    conn.close()

    if internship is None:

        return render_template(
            "internship_detail.html",
            internship=None,
            details=None,
            error="This internship does not exist."
        ), 404

    details = INTERNSHIP_DETAILS.get(
        internship["company"],
        {
            "location": "Not specified",
            "duration": "Not specified",
            "stipend": "Not publicly specified",
            "eligibility": "Students / eligible candidates",
            "deadline": "Check current company opening",
            "responsibilities": [],
            "learning": []
        }
    )

    return render_template(
        "internship_detail.html",
        internship=internship,
        details=details
    )


# =====================================================
# 22. HELPER - GET INTERNSHIP
# =====================================================

def get_internship(company_id):

    conn = get_db()

    internship = conn.execute(
        """
        SELECT
            id,
            company,
            role,
            field,
            skills
        FROM opportunities
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    conn.close()

    return internship


# =====================================================
# 23. APPLY FOR INTERNSHIP
# =====================================================

@app.route(
    "/apply-internship/<int:company_id>",
    methods=["POST"]
)
def apply_internship(company_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    internship = get_internship(
        company_id
    )

    if internship is None:

        return "Internship not found", 404

    # -------------------------------------------------
    # FORM DATA
    # -------------------------------------------------

    full_name = request.form.get(
        "full_name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    college = request.form.get(
        "college",
        ""
    ).strip()

    branch = request.form.get(
        "branch",
        ""
    ).strip()

    year = request.form.get(
        "year",
        ""
    ).strip()

    skills = request.form.get(
        "skills",
        ""
    ).strip()

    cover_message = request.form.get(
        "cover_message",
        ""
    ).strip()

    resume = request.files.get(
        "resume"
    )

    # -------------------------------------------------
    # REQUIRED FIELDS
    # -------------------------------------------------

    if (
        not full_name
        or not email
        or not phone
        or not college
    ):

        return render_template(
            "internship_detail.html",
            internship=internship,
            details=INTERNSHIP_DETAILS.get(
                internship["company"],
                {}
            ),
            error="Please fill all required fields."
        )

    # -------------------------------------------------
    # RESUME
    # -------------------------------------------------

    if not resume or resume.filename == "":

        return render_template(
            "internship_detail.html",
            internship=internship,
            details=INTERNSHIP_DETAILS.get(
                internship["company"],
                {}
            ),
            error="Please upload your resume."
        )

    # -------------------------------------------------
    # PDF CHECK
    # -------------------------------------------------

    original_name = secure_filename(
        resume.filename
    )

    if not original_name.lower().endswith(".pdf"):

        return render_template(
            "internship_detail.html",
            internship=internship,
            details=INTERNSHIP_DETAILS.get(
                internship["company"],
                {}
            ),
            error="Please upload a PDF resume."
        )

    # -------------------------------------------------
    # UNIQUE RESUME NAME
    # -------------------------------------------------

    filename = (
        str(uuid.uuid4())
        + "_"
        + original_name
    )

    resume_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    resume.save(resume_path)

    # -------------------------------------------------
    # SAVE APPLICATION
    # -------------------------------------------------

    conn = get_db()

    conn.execute(
        """
        INSERT INTO internship_applications
        (
            internship_id,
            full_name,
            email,
            phone,
            college,
            branch,
            year,
            skills,
            resume,
            cover_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company_id,
            full_name,
            email,
            phone,
            college,
            branch,
            year,
            skills,
            filename,
            cover_message
        )
    )

    conn.commit()

    conn.close()

    return render_template(
        "internship_success.html",
        name=full_name
    )


# =====================================================
# 24. PLACEMENTS PAGE
# =====================================================

@app.route("/placements")
def placements():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    readiness = 0

    matching_placements = []

    if student:

        _, _, readiness = analyze(
            student["skills"],
            student["target_field"]
        )

        for placement in PLACEMENTS:

            if (
                placement["field"].lower()
                ==
                student["target_field"].lower()
            ):

                matching_placements.append(
                    placement
                )

    return render_template(
        "placement.html",
        student=student,
        readiness=readiness,
        placements=matching_placements
    )


# =====================================================
# 25. PLACEMENTS API
# =====================================================

@app.route("/api/placements")
def api_placements():

    if "user_id" not in session:

        return jsonify({
            "error": "Unauthorized"
        }), 401

    field = request.args.get(
        "field",
        ""
    ).strip()

    if not field:

        return jsonify([])

    matching_placements = []

    for placement in PLACEMENTS:

        if (
            placement["field"].lower()
            ==
            field.lower()
        ):

            matching_placements.append(
                placement
            )

    return jsonify(
        matching_placements
    )


# =====================================================
# 26. COMPANIES
# =====================================================

@app.route("/companies")
def companies():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    all_companies = [

        {
            "name": "TCS",
            "field": "Data Analyst",
            "location": "Mumbai, Pune, Bengaluru",
            "opportunities": "Data Analyst, Business Analyst",
            "skills": "SQL, Excel, Power BI, Python"
        },

        {
            "name": "Infosys",
            "field": "Data Analyst",
            "location": "Pune, Bengaluru, Hyderabad",
            "opportunities": "Data Analyst, Software Developer",
            "skills": "Python, SQL, Excel, Statistics"
        },

        {
            "name": "Accenture",
            "field": "Business Intelligence",
            "location": "Pune, Bengaluru, Mumbai",
            "opportunities": "BI Analyst, Data Analyst",
            "skills": "SQL, Power BI, DAX, Data Modeling"
        },

        {
            "name": "Deloitte",
            "field": "Business Intelligence",
            "location": "Mumbai, Pune, Hyderabad",
            "opportunities": "BI Analyst, Data Analyst",
            "skills": "SQL, Power BI, Excel, Data Visualization"
        },

        {
            "name": "Wipro",
            "field": "Data Scientist",
            "location": "Pune, Bengaluru, Hyderabad",
            "opportunities": "Data Scientist, ML Engineer",
            "skills": "Python, Machine Learning, Pandas"
        },

        {
            "name": "Cognizant",
            "field": "Data Analyst",
            "location": "Pune, Chennai, Bengaluru",
            "opportunities": "Data Analyst, Business Analyst",
            "skills": "SQL, Python, Excel, Power BI"
        },

        {
            "name": "Capgemini",
            "field": "Software Engineer",
            "location": "Pune, Mumbai, Bengaluru",
            "opportunities": "Software Engineer, Developer",
            "skills": "Python, JavaScript, SQL, Git"
        },

        {
            "name": "IBM",
            "field": "Data Scientist",
            "location": "Bengaluru, Pune, Hyderabad",
            "opportunities": "Data Scientist, AI Engineer",
            "skills": "Python, Machine Learning, SQL"
        }
    ]

    if student:

        target_field = student["target_field"]

        companies_list = [

            company

            for company in all_companies

            if company["field"].lower()
            ==
            target_field.lower()
        ]

    else:

        companies_list = all_companies

    return render_template(
        "companies.html",
        student=student,
        companies=companies_list
    )


# =====================================================
# 27. LEARNING RESOURCES
# =====================================================

@app.route("/learning-resources")
def learning_resources():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    return render_template(
        "learning_resources.html",
        student=student
    )


# =====================================================
# 28. ASSESSMENTS
# =====================================================

@app.route("/assessments")
def assessments():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    return render_template(
        "assessments.html",
        student=student
    )


@app.route("/submit-assessment", methods=["POST"])
def submit_assessment():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get score and total from assessment form
    score_raw = request.form.get("score", "0")
    total_raw = request.form.get("total", "0")

    try:
        score = int(score_raw)
    except (ValueError, TypeError):
        score = 0

    try:
        total = int(total_raw)
    except (ValueError, TypeError):
        total = 0

    # Safety check
    if score < 0:
        score = 0

    if total < 0:
        total = 0

    if total > 0 and score > total:
        score = total

    # Save assessment result
    session["assessment_score"] = score
    session["assessment_total"] = total

    # Also save percentage
    if total > 0:
        percentage = round((score / total) * 100)
    else:
        percentage = 0

    session["assessment_percentage"] = percentage

    return redirect(url_for("assessment_result"))

# =====================================================
# 30. ASSESSMENT RESULT
# =====================================================

@app.route("/assessment-result")
def assessment_result():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    score = session.get(
        "assessment_score",
        0
    )

    total = session.get(
        "assessment_total",
        0
    )

    if total > 0:

        percentage = round(
            (score / total) * 100
        )

    else:

        percentage = 0

    if percentage >= 80:

        performance = "Excellent"

        message = (
            "Great job! You are well prepared."
        )

    elif percentage >= 60:

        performance = "Good"

        message = (
            "Good performance. Keep improving your skills."
        )

    elif percentage >= 40:

        performance = "Needs Improvement"

        message = (
            "Focus on your weak areas and practice regularly."
        )

    else:

        performance = "Beginner"

        message = (
            "You need more preparation. "
            "Follow your learning roadmap and practice regularly."
        )

    return render_template(
        "assessment_result.html",
        score=score,
        total=total,
        percentage=percentage,
        performance=performance,
        message=message
    )


# =====================================================
# =====================================================
# 31. REPORT
# =====================================================

@app.route("/report")
def report():

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    # ==========================================
    # ASSESSMENT RESULT
    # ==========================================

    score = session.get("assessment_score", 0)
    total = session.get("assessment_total", 0)

    try:
        score = int(score)
    except (ValueError, TypeError):
        score = 0

    try:
        total = int(total)
    except (ValueError, TypeError):
        total = 0

    # ==========================================
    # PERCENTAGE
    # ==========================================

    if total > 0:
        percentage = round((score / total) * 100)
    else:
        percentage = 0

    # ==========================================
    # PERFORMANCE
    # ==========================================

    if percentage >= 80:

        performance = "Excellent"

    elif percentage >= 60:

        performance = "Good"

    elif percentage >= 40:

        performance = "Average"

    else:

        performance = "Needs Improvement"

    # ==========================================
    # CAREER READINESS
    # ==========================================

    readiness = 0

    if student:

        _, _, readiness = analyze(
            student["skills"],
            student["target_field"]
        )

    # ==========================================
    # REPORT
    # ==========================================

    return render_template(
        "report.html",

        student=student,

        score=score,

        total=total,

        percentage=percentage,

        performance=performance,

        readiness=readiness
    )

# =====================================================
# 32. SETTINGS
# =====================================================

@app.route("/settings")
def settings():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "settings.html",
        user_name=session.get(
            "name",
            "Student"
        ),
        user_email=session.get(
            "email",
            ""
        )
    )

# =====================================================
# 33. WORKING PLACEMENT FEATURES
# =====================================================

def get_current_student():

    conn = get_db()

    student = conn.execute(
        """
        SELECT *
        FROM students
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    return student


def calculate_placement_match(student, placement):

    if not student:
        return {
            "matched": [],
            "missing": placement["skills"],
            "match_percentage": 0
        }

    current_skills = normalize_skills(
        student["skills"]
    )

    matched = []
    missing = []

    for skill in placement["skills"]:

        if skill.lower() in current_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    total = len(placement["skills"])

    if total > 0:
        percentage = round(
            len(matched) / total * 100
        )
    else:
        percentage = 0

    return {
        "matched": matched,
        "missing": missing,
        "match_percentage": percentage
    }


# =====================================================
# PLACEMENT APPLICATION TABLE
# =====================================================

def init_placement_features():

    conn = get_db()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS placement_applications (

            iid INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

            student_id INTEGER,

            company TEXT NOT NULL,

            role TEXT NOT NULL,

            field TEXT,

            status TEXT DEFAULT 'Applied',

            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS placement_drives (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            company TEXT NOT NULL,

            role TEXT NOT NULL,

            drive_date TEXT NOT NULL,

            location TEXT,

            eligibility TEXT
        )
        """
    )

    count = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM placement_drives
        """
    ).fetchone()["count"]

    if count == 0:

        drive_date = (
            datetime.now()
            + timedelta(days=15)
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        conn.execute(
            """
            INSERT INTO placement_drives
            (
                company,
                role,
                drive_date,
                location,
                eligibility
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Accenture",
                "Data Scientist",
                drive_date,
                "Pune",
                "B.Tech / B.E / MCA"
            )
        )

        second_drive = (
            datetime.now()
            + timedelta(days=30)
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        conn.execute(
            """
            INSERT INTO placement_drives
            (
                company,
                role,
                drive_date,
                location,
                eligibility
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Wipro",
                "Machine Learning Engineer",
                second_drive,
                "Bengaluru",
                "B.Tech / B.E"
            )
        )

    conn.commit()

    conn.close()


# =====================================================
# SMART JOB MATCH
# =====================================================

@app.route("/api/placement/matches")
def placement_matches():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    student = get_current_student()

    if not student:

        return jsonify({
            "student": None,
            "placements": []
        })

    result = []

    for placement in PLACEMENTS:

        if (
            placement["field"].lower()
            != student["target_field"].lower()
        ):
            continue

        match = calculate_placement_match(
            student,
            placement
        )

        result.append({

            "company": placement["company"],

            "role": placement["role"],

            "field": placement["field"],

            "location": placement["location"],

            "package": placement["package"],

            "experience": placement["experience"],

            "skills": placement["skills"],

            "eligibility": placement["eligibility"],

            "matched_skills": match["matched"],

            "missing_skills": match["missing"],

            "match_percentage":
                match["match_percentage"]
        })

    result.sort(
        key=lambda x:
        x["match_percentage"],
        reverse=True
    )

    return jsonify({
        "target_field":
            student["target_field"],

        "placements":
            result
    })


# =====================================================
# PLACEMENT SKILL GAP
# =====================================================

@app.route("/api/placement/skill-gap")
def placement_skill_gap():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    student = get_current_student()

    if not student:

        return jsonify({
            "current_skills": [],
            "required_skills": [],
            "missing_skills": []
        })

    matched, missing, readiness = analyze(
        student["skills"],
        student["target_field"]
    )

    return jsonify({

        "target_field":
            student["target_field"],

        "current_skills":
            [
                x.strip()
                for x in student["skills"].split(",")
                if x.strip()
            ],

        "required_skills":
            FIELD_SKILLS.get(
                student["target_field"],
                []
            ),

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "readiness":
            readiness
    })


# =====================================================
# IMPROVE MY MATCH
# =====================================================

@app.route("/api/placement/improve-match")
def improve_match():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    student = get_current_student()

    if not student:

        return jsonify({
            "message":
                "Please complete your profile first.",
            "skills": []
        })

    current_skills = normalize_skills(
        student["skills"]
    )

    suggestions = []

    for placement in PLACEMENTS:

        if (
            placement["field"].lower()
            != student["target_field"].lower()
        ):
            continue

        for skill in placement["skills"]:

            if skill.lower() not in current_skills:

                if skill not in suggestions:

                    suggestions.append(skill)

    priority = []

    for skill in suggestions:

        count = 0

        for placement in PLACEMENTS:

            if (
                placement["field"].lower()
                !=
                student["target_field"].lower()
            ):
                continue

            if skill in placement["skills"]:

                count += 1

        priority.append({

            "skill": skill,

            "importance":
                count,

            "message":
                f"Learning {skill} can improve your job match."
        })

    priority.sort(
        key=lambda x:
        x["importance"],
        reverse=True
    )

    return jsonify({

        "target_field":
            student["target_field"],

        "recommendations":
            priority
    })


# =====================================================
# PLACEMENT DRIVE
# =====================================================

@app.route("/api/placement/drive")
def placement_drive():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    conn = get_db()

    drive = conn.execute(
        """
        SELECT *
        FROM placement_drives
        WHERE drive_date::timestamp >= CURRENT_TIMESTAMP
        ORDER BY drive_date::timestamp
        LIMIT 1
        """
    ).fetchone()

    conn.close()

    if not drive:

        return jsonify({
            "available": False
        })

    return jsonify({

        "available": True,

        "id":
            drive["id"],

        "company":
            drive["company"],

        "role":
            drive["role"],

        "drive_date":
            drive["drive_date"],

        "location":
            drive["location"],

        "eligibility":
            drive["eligibility"]
    })


# =====================================================
# ELIGIBILITY CHECKER
# =====================================================

@app.route("/api/placement/eligibility")
def placement_eligibility():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    student = get_current_student()

    if not student:

        return jsonify({
            "eligible": False,

            "message":
                "Please complete your profile first."
        })

    result = []

    for placement in PLACEMENTS:

        if (
            placement["field"].lower()
            != student["target_field"].lower()
        ):
            continue

        match = calculate_placement_match(
            student,
            placement
        )

        eligible = (
            match["match_percentage"] >= 50
        )

        result.append({

            "company":
                placement["company"],

            "role":
                placement["role"],

            "eligible":
                eligible,

            "match_percentage":
                match["match_percentage"],

            "missing_skills":
                match["missing"]
        })

    return jsonify({
        "results": result
    })


# =====================================================
# APPLY FOR PLACEMENT
# =====================================================

@app.route(
    "/api/placement/apply",
    methods=["POST"]
)
def apply_placement():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "No application data received."
        }), 400

    company = str(
        data.get("company", "")
    ).strip()

    role = str(
        data.get("role", "")
    ).strip()

    field = str(
        data.get("field", "")
    ).strip()

    if not company or not role:

        return jsonify({
            "error":
                "Company and role are required."
        }), 400

    student = get_current_student()

    student_id = None

    if student:
        student_id = student["id"]

    conn = get_db()

    existing = conn.execute(
        """
        SELECT id
        FROM placement_applications
        WHERE student_id = ?
        AND company = ?
        AND role = ?
        """,
        (
            student_id,
            company,
            role
        )
    ).fetchone()

    if existing:

        conn.close()

        return jsonify({

            "success": False,

            "message":
                "You have already applied for this placement."
        })

    conn.execute(
        """
        INSERT INTO placement_applications
        (
            student_id,
            company,
            role,
            field,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student_id,
            company,
            role,
            field,
            "Applied"
        )
    )

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,

        "message":
            f"Application submitted successfully for {company}."
    })


# =====================================================
# APPLICATION TRACKING
# =====================================================

@app.route("/api/placement/applications")
def placement_applications():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    student = get_current_student()

    if not student:

        return jsonify({

            "applied": 0,

            "shortlisted": 0,

            "interview": 0,

            "selected": 0,

            "applications": []
        })

    conn = get_db()

    applications = conn.execute(
        """
        SELECT *
        FROM placement_applications
        WHERE student_id = ?
        ORDER BY applied_at DESC
        """,
        (
            student["id"],
        )
    ).fetchall()

    conn.close()

    applied = 0
    shortlisted = 0
    interview = 0
    selected = 0

    result = []

    for application in applications:

        status = application["status"]

        if status == "Applied":
            applied += 1

        elif status == "Shortlisted":
            shortlisted += 1

        elif status == "Interview":
            interview += 1

        elif status == "Selected":
            selected += 1

        result.append({

            "id":
                application["id"],

            "company":
                application["company"],

            "role":
                application["role"],

            "status":
                application["status"],

            "applied_at":
                application["applied_at"]
        })

    return jsonify({

        "applied":
            applied,

        "shortlisted":
            shortlisted,

        "interview":
            interview,

        "selected":
            selected,

        "applications":
            result
    })


# =====================================================
# PLACEMENT AI ADVISOR
# =====================================================

@app.route("/api/placement/advice")
def placement_advice():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    student = get_current_student()

    if not student:

        return jsonify({

            "advice": [
                "Complete your student profile first.",
                "Add your current technical skills.",
                "Select your target career."
            ]
        })

    matched, missing, readiness = analyze(
        student["skills"],
        student["target_field"]
    )

    advice = []

    if readiness < 40:

        advice.append(
            "Your placement readiness is currently low. "
            "Focus on your missing technical skills first."
        )

    elif readiness < 70:

        advice.append(
            "You have a good foundation. "
            "Improve your missing skills and start practicing interviews."
        )

    else:

        advice.append(
            "Your technical preparation is strong. "
            "You can start applying actively."
        )

    if missing:

        advice.append(
            "Priority skills to learn: "
            + ", ".join(missing[:4])
        )

    advice.append(
        "Practice aptitude questions regularly "
        "to improve your placement performance."
    )

    advice.append(
        "Prepare a resume highlighting your "
        "projects, technical skills and achievements."
    )

    advice.append(
        "Practice HR and technical interview questions "
        "before attending placement drives."
    )

    return jsonify({

        "target_field":
            student["target_field"],

        "readiness":
            readiness,

        "missing_skills":
            missing,

        "advice":
            advice
    })


# =====================================================
# PLACEMENT PAGE DATA
# =====================================================

@app.route("/api/placement/dashboard")
def placement_dashboard():

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first."
        }), 401

    student = get_current_student()

    if not student:

        return jsonify({

            "target_field":
                "Not selected",

            "readiness":
                0,

            "technical":
                0,

            "aptitude":
                0,

            "interview":
                0,

            "resume":
                0
        })

    _, missing, readiness = analyze(
        student["skills"],
        student["target_field"]
    )

    # Demo preparation components.
    # These can later be connected to actual assessments.
    technical = readiness

    aptitude = min(
        100,
        max(
            0,
            readiness - 5
        )
    )

    interview = min(
        100,
        max(
            0,
            readiness - 10
        )
    )

    resume = min(
        100,
        max(
            0,
            readiness - 3
        )
    )

    overall = round(
        (
            technical
            + aptitude
            + interview
            + resume
        ) / 4
    )

    return jsonify({

        "target_field":
            student["target_field"],

        "readiness":
            overall,

        "technical":
            technical,

        "aptitude":
            aptitude,

        "interview":
            interview,

        "resume":
            resume,

        "missing_skills":
            missing
    })
# =====================================================
# START APPLICATION
# =====================================================

init_db()
init_placement_features()

if __name__ == "__main__":
    app.run(debug=True)