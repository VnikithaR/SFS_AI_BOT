---

````markdown
# SFS_InfoBot 🤖

SFS_InfoBot is an AI-powered chatbot built using Rasa for St. Francis de Sales College. It provides information about college events, courses, facilities, alumni achievements, skill development workshops, and much more. The bot uses a structured set of JSON files and integrates with MongoDB for real-time data fetching.

---

## 📁 Project Structure

```plaintext
SFS_InfoBot/
│
├── README.md
├── # Git Contribution Statistics.md
│
├── bot_data/                  # JSON data used by the bot
│   ├── Alumni_Achievements_Clubs/
│   ├── College_News_ Events/
│   ├── contact/
│   ├── courses/
│   │   ├── pg_courses/
│   │   └── ug_courses/
│   ├── events/
│   ├── facilities/
│   ├── institute_info/
│   │   └── admissions/
│   ├── Results_and_exam/
│   └── Skill_Development_Workshops/
│
├── frontend/                 # Frontend files (HTML, CSS, JS)
│   ├── index.html
│   ├── db_auth.py
│   ├── assets/
│   │   ├── apps/
│   │   ├── favicons/
│   │   └── icons/
│   ├── css/
│   └── js/
│
├── logs/                     # Logging and documentation
│   ├── contributions/
│   └── docs/
│
├── rasa/                     # Rasa chatbot files
│   ├── config.yml
│   ├── credentials.yml
│   ├── domain.yml
│   ├── endpoints.yml
│   ├── spell_checker_component.py
│   ├── actions/
│   ├── data/
│   ├── models/
│   └── .rasa/
│
├── scripts/                  # MongoDB integration scripts
│   └── import_to_mongodb.py
└── __pycache__/              # Cached Python files
````

---

## 🧠 Tech Stack

* **Rasa** – Natural Language Understanding & Dialogue Management
* **Python** – Backend logic for chatbot actions
* **MongoDB** – Data storage for structured information
* **HTML/CSS/JavaScript** – Frontend interface
* **PyMongo** – MongoDB interaction script

---

## 📦 MongoDB Collections

The database used: `sfs_infobot_db`

### Collection Names

```
# Alumni Achievements
Alumni_Achievements_Clubs_achievers
Alumni_Achievements_Clubs_alumni_2020
Alumni_Achievements_Clubs_marketing_club
Alumni_Achievements_Clubs_ncc_orientation

# College News & Events
College_News_ Events_college_news
College_News_ Events_media_coverage
College_News_ Events_newsletter

# Contact
contact_contact_info
contact_feedback_form

# PG Courses
courses_pg_courses_pg_courses_available
courses_pg_courses_pg_fee_details
courses_pg_courses_pg_syllabus

# UG Courses
courses_ug_courses_ug_courses_available
courses_ug_courses_ug_faculties
courses_ug_courses_ug_fee_details
courses_ug_courses_ug_programs_details
courses_ug_courses_ug_syllabus

# Events
events_college_events
events_festivals_special_days
events_upcoming_events

# Facilities
facilities_cultural_sports_facilities
facilities_facilities_at_sfs
facilities_ict_facilities
facilities_library_facilities
facilities_physical_facilities
facilities_welfare_facilities
facilities_wifi_facilities

# Institute Info
institute_info_admissions_admission_details
institute_info_campus
institute_info_college_timings
institute_info_founder
institute_info_history
institute_info_logo_anthem
institute_info_naac_data
institute_info_patron
institute_info_principal_message
institute_info_social_media_and_brochure
institute_info_values
institute_info_vision

# Results and Exams
Results_and_exam_exam_results
Results_and_exam_question_papers
Results_and_exam_result_certification

# Skill Development Workshops
Skill_Development_Workshops_advanced_excel_workshop
Skill_Development_Workshops_personal_branding_workshop
Skill_Development_Workshops_python_programming_workshop

# User data
users
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* MongoDB instance running locally or on a server
* Rasa (Install using `pip install rasa`)
* Frontend server (Optional: use Python `http.server`, Flask, etc.)

### Install Dependencies

```bash
pip install rasa pymongo
```

### Train the Bot

```bash
cd rasa
rasa train
```

### Run the Bot

```bash
rasa run actions &
rasa shell
```

### Import Data to MongoDB

```bash
cd scripts
python import_to_mongodb.py
```

---

## 🧩 Features

* 🎓 PG & UG Course Info (Syllabus, Fees, Faculty)
* 📅 Upcoming Events, Festivals, and Newsletters
* 🏫 Institute Details (History, Vision, Principal’s Message)
* 🏋️‍♂️ Facility Descriptions (ICT, Library, Sports)
* 🧠 Skill Development Workshops
* 📝 Exam Results and Question Papers
* 📞 Contact Info and Feedback

---

## 🛠 Authors & Contributors

* [Sambramam](./logs/contributions/sambramam_contributions.csv)
* [V Nikitha](./logs/contributions/vnikitha_contributions.csv)

---

## 📝 License

MIT License – feel free to use, modify, and distribute!

---

```


```
