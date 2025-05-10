# **SFS InfoBot**

A web-based chatbot application powered by **Rasa** for NLP and **MongoDB** for data-driven responses. It helps students, faculty, and visitors access comprehensive college-related information such as courses, events, facilities, alumni updates, and more through a conversational interface.

---

## **Table of Contents**

1. [Overview](#overview)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Setup and Configuration](#setup-and-configuration)
6. [Rasa Model Training](#rasa-model-training)
7. [MongoDB Integration](#mongodb-integration)
8. [Frontend Interaction](#frontend-interaction)
9. [Usage](#usage)
10. [Testing](#testing)
11. [Contributing](#contributing)
12. [License](#license)
13. [Acknowledgements](#acknowledgements)

---

## **Overview**

SFS InfoBot is a chatbot designed to help users find various college-related information through a conversational interface. The bot integrates **Rasa** for processing natural language and **MongoDB** for storing and retrieving dynamic data. Key functionalities of the bot include:

* **Alumni Achievements & Clubs**
* **College News & Events**
* **Courses Offered** (Undergraduate & Postgraduate fee, faculty, syllabus details.)
* **Facilities Available**(Library, WIFI, Sports, ICT, etc.)
* **Skill Development Workshops**
* **Exam Results & Certifications**
* **Contact & Feedback Info**

---

## **Technologies Used**

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Python, Rasa (Core & NLU)
* **Database**: MongoDB

* **Libraries & Frameworks**:

  * **Rasa**: NLP and chatbot logic
  * **Flask** or **FastAPI** (for backend API)
  * **MongoDB**: Dynamic data storage
  * **Pymongo**: MongoDB cient  for Python

---

## **Installation**

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sfs-infobot.git
cd sfs-infobot
```

### 2. Install Frontend Dependencies

Navigate to the `frontend` directory and install the necessary dependencies:

```bash
cd frontend
npm install
```

### 3. Set Up Backend (Rasa & MongoDB)

* **Install Rasa**:

```bash
pip install rasa
```

* **Install MongoDB** and **pymongo**:

```bash
pip install pymongo
```

### 4. MongoDB Setup

Ensure MongoDB is installed and running. Follow [MongoDB's installation guide](https://www.mongodb.com/docs/manual/installation/) if you haven't set it up yet. Then, populate your MongoDB database with data from the `bot_data` directory by running the script:

```bash
python scripts/import_to_mongodb.py
```

---

## **Project Structure**

Here's a breakdown of the project structure:

```plaintext
C:.
|   README.md
|
+---bot_data
|   +---Alumni_Achievements_Clubs
|   +---College_News_Events
|   +---contact
|   +---courses
|   +---events
|   +---facilities
|   +---institute_info
|   +---Results_and_exam
|   +---Skill_Development_Workshops
|
+---frontend                                   
|   +---assets
|   +---css
|   +---js
|   +---index.html
|
+---rasa
|   +---actions
|   +---data
|   +---models
|   +---config.yml
|   +---domain.yml
|   +---endpoints.yml
|
+---scripts
|   +---import_to_mongodb.py
```

* **bot\_data**: Contains the data (in JSON format) used by the chatbot to provide information to the users.
* **frontend**: The user interface for the chatbot, built with HTML, CSS, and JavaScript.
* **rasa**: Contains Rasa configuration files, custom actions, training data, and models.
* **scripts**: Python scripts to Imports JSON to MongoDB.

---

## **Setup and Configuration**

### 1. MongoDB Configuration

Make sure that MongoDB is running and configured correctly. The **`import_to_mongodb.py`** script populates the MongoDB database with the data from the `bot_data` folder. Run the script to load the data:

```bash
python scripts/import_to_mongodb.py
```

### 2. Rasa Configuration

* Update the **`credentials.yml`** and **`endpoints.yml`** files to match your MongoDB connection details.
* Ensure that any custom actions are properly configured in the **`domain.yml`** file.

---

## **Rasa Model Training**

To train the Rasa model, run the following command in the **rasa** directory:

```bash
rasa train
```

This will train the chatbot based on the defined intents, stories, and actions.

---

## **MongoDB Integration**

Each topic (e.g., courses, events) is stored as a JSON file and imported to MongoDB collections via the import script. Custom actions in Rasa then query MongoDB based on user intent and dynamically generate responses.

**Example:**

* User: "Tell me about PG courses"
* Bot queries `pg_courses_available` collection
* Responds with structured course list

---

## **Frontend Interaction**

* The **Frontend** is responsible for sending user inputs (messages) to the Rasa server via the **API**.
* After processing the message, Rasa sends a response (e.g., course details, faculty information) back to the frontend.
* The frontend then displays this response to the user in the chatbot interface.

### Example Interaction

1. **User**: "What courses do you offer?"
2. **Bot**: "We offer undergraduate and postgraduate courses in various fields, including Computer Science, Business Administration, etc."

### Chat UI Features

* Open/Close chatbot widget
* Welcome message on first open
* Send/Receive chat messages
* Typing indicator
* Session-specific user state and settings
* Login modal and feature toggles for user dashboard

**Backend API Integration:**

```javascript
POST http://localhost:5005/webhooks/rest/webhook
```

**Request Payload:**

```json
{
  "sender": "user",
  "message": "Show me the syllabus"
}
```

---

## **Usage**

To run the chatbot locally, follow these steps:

1. **Start the Rasa Server**:

```bash
rasa run --model models --enable-api --cors "*"
```

1. **Start the Frontend** (if applicable):

```bash
npm start
```

1. **Access the chatbot**: Open your browser and visit `http://localhost:3000` (or the configured port).

---

## **Testing**

### 1. **Unit Tests**: Ensure that custom actions, NLU configurations, and models are properly tested

### 2. **MongoDB Queries**: Test the data import script to verify correct population of MongoDB

### 3. **End-to-End Testing**: Test the complete chatbot workflow from frontend interaction to data retrieval from MongoDB

---

## **Contributing**

1. **Fork** the repository.
2. **Create a new branch**: `git checkout -b feature-name`.
3. **Commit** your changes: `git commit -am 'Add new feature'`.
4. **Push** your changes: `git push origin feature-name`.
5. **Create a pull request**.

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgements**

* **Rasa**: For providing the NLP engine for the chatbot.
* **MongoDB**: For providing the database to store and manage dynamic data.
* **All contributors**: Thanks for your contributions to making this project successful.
