# SkillBridge 🎓

### Academia–Industry Collaboration Portal for Skill Mapping, Internships & Placements

## 📌 About the Project

**SkillBridge** is a web-based career guidance and skill-mapping platform designed to help college students understand their current skills, identify skill gaps, build personalized learning roadmaps, and prepare for internships and placements.

The platform connects **student skills with industry-required skills** and helps students understand what they need to learn for their target career.

It also provides colleges with an **overall skill-gap report** based on student assessments, helping institutions identify common skill gaps and plan training programs.

---

## 🎯 Problem Statement

Many college students have skills but do not know:

* Which skills are required for their target career
* Which skills they are currently missing
* What they should learn next
* Whether they are ready for internships and placements
* Which companies or opportunities match their skills

At the same time, colleges may not have a clear picture of the **common skill gaps among their students**.

SkillBridge aims to solve these problems through a single platform.

---

## 💡 Proposed Solution

SkillBridge compares a student's **current skills** with the **skills required for a selected career field**.

The system provides:

1. Current skill analysis
2. Required skill identification
3. Skill gap analysis
4. Placement readiness percentage
5. Personalized learning roadmap
6. Career and internship recommendations
7. Placement information
8. Company information
9. Learning resources
10. Skill assessment
11. Overall assessment report
12. College-level skill-gap analysis

---

## 🚀 Main Features

### 👤 Student Profile

Students can create and manage their profile with information such as:

* Name
* Email
* Education details
* Skills
* Resume

---

### 🔗 Skill Mapping

Students can select their target career and enter their current skills.

The system compares:

```text
Current Skills
      ↓
Required Career Skills
      ↓
Skill Comparison
      ↓
Matched Skills + Missing Skills
```

Example:

**Target Career:** Data Analyst

**Current Skills:**

* Python
* HTML
* CSS
* SQL

**Required Skills:**

* Python
* SQL
* Excel
* Power BI
* Data Visualization
* Statistics

**Missing Skills:**

* Excel
* Power BI
* Data Visualization
* Statistics

---

### 🗺️ Personalized Roadmap

Based on missing skills, SkillBridge provides a learning roadmap.

Example:

```text
Step 1 → Learn Excel
Step 2 → Learn SQL
Step 3 → Learn Power BI
Step 4 → Learn Data Visualization
Step 5 → Learn Statistics
Step 6 → Practice Projects
Step 7 → Apply for Internships
```

---

### 📊 Skill Assessment

Students can take assessments to evaluate their knowledge and skills.

The assessment helps calculate their:

* Score
* Skill level
* Strengths
* Weak areas
* Placement readiness

---

### 📈 Overall Report

The report section provides an overall view of the student's assessment performance.

It can include:

* Total assessment score
* Skills assessed
* Strong skills
* Weak skills
* Skill gaps
* Career readiness
* Improvement recommendations

---

### 💼 Internships & Jobs

Students can explore internship and job opportunities based on their selected career field and skills.

---

### 🎯 Placements

The placement section helps students understand placement opportunities and prepare for recruitment.

---

### 🏢 Companies

Students can explore companies and understand the types of skills they commonly require.

---

### 📚 Learning Resources

The platform provides learning resources for improving missing skills.

---

### 🏫 College Skill-Gap Report

SkillBridge can aggregate assessment/skill information to help colleges understand common student skill gaps.

Example:

```text
Skill Gap Analysis

SQL              → 45 students
Power BI         → 38 students
Excel            → 32 students
Data Visualization → 27 students
Statistics       → 21 students
```

This can help colleges organize targeted workshops and training programs.

---

## 🧠 Career Fields

SkillBridge can support different career fields such as:

### Data Analyst

* Python
* SQL
* Excel
* Power BI
* Data Visualization
* Statistics

### Data Scientist

* Python
* SQL
* Pandas
* NumPy
* Statistics
* Machine Learning
* Data Visualization

### Business Intelligence

* SQL
* Excel
* Power BI
* Data Visualization
* Data Modeling
* DAX

### Software Engineer

* Python
* HTML
* CSS
* JavaScript
* Git
* DSA
* SQL

---

## 🛠️ Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask

### Database

* SQLite

### Other Technologies

* REST/API-based functionality
* Resume upload
* Skill analysis
* Assessment system

---

## 📁 Project Structure

```text
SkillBridge/
│
├── app.py
├── requirements.txt
├── skillbridge.db
├── README.md
│
├── static/
│   ├── style.css
│   ├── app.js
│   ├── assessment.js
│   ├── internship.js
│   ├── placement.js
│   ├── report.js
│   ├── roadmap.js
│   └── settings.js
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── skill_mapping.html
│   ├── roadmap.html
│   ├── assessments.html
│   ├── assessment_result.html
│   ├── report.html
│   ├── internship.html
│   ├── internship_detail.html
│   ├── internship_details.html
│   ├── placement.html
│   ├── companies.html
│   ├── learning_resources.html
│   └── settings.html
│
└── uploads/
    └── resumes/
```

---

## ⚙️ Installation

### 1. Clone or download the project

Open the project folder in VS Code.

### 2. Create a virtual environment

```bash
python -m v
```
