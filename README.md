# Student Registration System

A simple **Flask** web application to manage student records with **MongoDB** as the backend database. Users can **add, view, update, and delete** student details.

---

## Features

* List all students on the home page
* Add a new student
* Update existing student details
* Delete a student with confirmation
* Simple and responsive UI using Bootstrap

---

## Tech Stack

* **Backend:** Python, Flask
* **Database:** MongoDB (via Flask-PyMongo)
* **Frontend:** HTML, Jinja2 templates, Bootstrap 5
* **Environment Variables:** Managed via `.env` file
* **CI/CD:** Jenkins Pipeline

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Prateekdevops-619/flask_Practice.git
cd flask_Practice
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
MONGO_URI=<your-mongodb-connection-string>
SECRET_KEY=<your-secret-key>
```

### 5. Run the application

```bash
python app.py
```

Open your browser at: [http://localhost:8000](http://localhost:8000)

### 6. Run tests

```bash
pip install pytest
python -m pytest test_app.py -v
```

---

## Project Structure

```
flask_Practice/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_student.html
│   └── update_student.html
├── app.py
├── test_app.py
├── requirements.txt
├── Jenkinsfile
├── .env
└── README.md
```

---

## Jenkins CI/CD Pipeline

### Overview

This project includes a fully automated Jenkins CI/CD pipeline defined in the `Jenkinsfile`. The pipeline automates building, testing, and deploying the Flask application.

### Pipeline Stages

| Stage | Description |
|-------|-------------|
| **Clone Repository** | Checks out the latest code from the `main` branch on GitHub |
| **Build** | Creates a Python virtual environment and installs all dependencies from `requirements.txt` |
| **Test** | Runs the unit test suite using `pytest` |
| **Deploy to Staging** | Deploys the application to a staging environment (only on the `main` branch) |

### Pipeline Flow

```
Push to main → Clone → Build (pip install) → Test (pytest) → Deploy to Staging
                                                  ↓
                                           Email Notification
                                        (Success or Failure)
```

### Prerequisites

Before setting up the Jenkins pipeline, ensure the following:

1. **Jenkins Server**: Access to Jenkins at [https://jenkinsacademics.herovired.com/](https://jenkinsacademics.herovired.com/)
2. **Python 3.x** installed on the Jenkins agent
3. **pip** package manager available
4. **Git** installed on the Jenkins agent
5. **MongoDB** accessible from the Jenkins environment

### Jenkins Setup Steps

#### Step 1: Configure Jenkins Credentials

In Jenkins, go to **Manage Jenkins → Credentials → System → Global credentials** and add:

| Credential ID | Type | Description |
|---------------|------|-------------|
| `mongo-uri` | Secret text | MongoDB connection string (e.g., `mongodb://localhost:27017/students`) |
| `secret-key` | Secret text | Flask application secret key |

#### Step 2: Install Required Jenkins Plugins

Ensure the following plugins are installed via **Manage Jenkins → Manage Plugins**:

- **Pipeline** (workflow-aggregator)
- **Git** plugin
- **GitHub** plugin
- **Email Extension** plugin
- **Pipeline Stage View** plugin

#### Step 3: Create the Pipeline Job

1. Click **New Item** in Jenkins
2. Enter a name (e.g., `flask-student-app`)
3. Select **Pipeline** and click OK
4. Under **Pipeline**, choose:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/Prateekdevops-619/flask_Practice.git`
   - **Branch Specifier**: `*/main`
   - **Script Path**: `Jenkinsfile`
5. Click **Save**

#### Step 4: Configure GitHub Webhook (Auto-Trigger)

1. Go to your GitHub repository → **Settings → Webhooks → Add webhook**
2. Set:
   - **Payload URL**: `https://jenkinsacademics.herovired.com/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: Select "Just the push event"
3. Click **Add webhook**

This enables automatic builds whenever code is pushed to the `main` branch.

#### Step 5: Configure Email Notifications

1. Go to **Manage Jenkins → Configure System**
2. Under **E-mail Notification**, configure:
   - **SMTP Server**: Your SMTP server (e.g., `smtp.gmail.com`)
   - **SMTP Port**: `465` (SSL) or `587` (TLS)
   - **Use SSL/TLS**: Enabled
   - **SMTP Authentication**: Provide email credentials
3. Under **Extended E-mail Notification**, configure the same SMTP settings
4. Test the configuration by sending a test email

### Trigger Mechanism

The pipeline is triggered automatically via:

- **GitHub Webhook**: Fires on every push to the `main` branch
- **Manual Build**: Can also be triggered manually from the Jenkins dashboard

### Notifications

The pipeline sends email notifications on:

- **Build Success**: Confirmation that the application was built, tested, and deployed
- **Build Failure**: Alert with a link to the build console for debugging

---

## Screenshots

**Home Page**
Lists all students with Edit/Delete buttons.
- <img width="1902" height="607" alt="image" src="https://github.com/user-attachments/assets/a58a6a6d-4978-4769-8074-232e4d31e69d" />

**Add Student**
Form to add a new student.
- <img width="1897" height="801" alt="image" src="https://github.com/user-attachments/assets/d65d25c3-ebb5-410a-adb1-e130ad7c5878" />

**Update Student**
Form pre-filled with student details.
- <img width="1905" height="897" alt="image" src="https://github.com/user-attachments/assets/04febf01-879f-431f-ab07-abcfb993acf1" />

---

## License

MIT License
