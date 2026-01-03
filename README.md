🔍 Lost & Found Website

A secure, admin-verified **Lost & Found web application** with AI-assisted item matching and email notifications.

This project is designed for **academic use** and demonstrates a complete real-world workflow with admin control to prevent false claims.

---

## 📌 Project Overview

The Lost & Found Website allows users to report lost or found items, while an admin verifies reports and confirms matches using an AI-assisted matching system.  
Items are never matched automatically — **admin approval is mandatory** for safety and authenticity.

---

## ✨ Features

### 👤 User Features
- 🔐 User Registration & Login
- 📝 Report Lost or Found Items
- 🔍 Browse Verified Items Only
- 📧 Receive Email Notification after Match Confirmation
- 📞 Contact Support via Contact Form

### 🛡️ Admin Features
- ✅ Verify or Reject Reported Items
- 🔍 View AI-Suggested Matches
- 🤝 Manually Confirm Correct Matches
- 📧 Trigger Email Notifications
- 📊 Admin Dashboard with Statistics

---

## 🧠 Core Working Logic

### Item Lifecycle
pending → active → matched

markdown
Copy code

- **pending** → Item reported by user (not visible publicly)
- **active** → Admin verified (visible to all users)
- **matched** → Admin confirmed match (emails sent)

📌 AI suggests matches, **admin makes the final decision**.

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, Tailwind CSS
- **Backend:** Python (Flask)
- **Database:** JSON files
- **AI Matching:** String similarity algorithm
- **Email Service:** Gmail SMTP
- **Authentication:** Session-based login

---

## 📁 Project Structure

lost_found_website/
├── app.py
├── requirements.txt
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── browse.html
│ ├── report.html
│ ├── contact.html
│ ├── admin_dashboard.html
│ └── admin_items.html
├── static/
│ └── uploads/
└── data/
├── users.json
├── items.json
├── reports.json
└── admins.json

Copy code

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Install Dependencies
```bash
pip install -r requirements.txt
Configure Environment Variables
Create a .env file (do NOT upload to GitHub):

env
Copy code
SECRET_KEY=your_secret_key
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
📌 Gmail App Password is required (2-Step Verification enabled).

Run the Application
bash
Copy code
python app.py
Access the website at:
👉 http://localhost:5000

🔑 Default Admin Account
Field	Value
Email	admin@lostandfound.com
Password	admin123

📌 This is a system login ID, not an actual email inbox.

🔄 How the System Works
👤 User Flow
Register / Login

Report Lost or Found Item

Item waits for admin verification

Browse verified items

Receive email after admin confirms match

🛡️ Admin Flow
Login as Admin

Verify or Reject items

View AI-suggested matches

Confirm correct match

Emails sent to both users

Item marked as matched

🤖 AI Matching System
AI suggests matches based on:

Item name similarity (40%)

Category match (30%)

Location similarity (20%)

Color match (10%)

Only matches with more than 50% similarity score are suggested.

📌 AI assists the admin — it does not auto-match items.

📧 Email Notifications
Emails are sent only after admin confirms a match:

❌ No email on report

❌ No email on verification

✅ Email only after confirmation

This prevents false notifications and misuse.

🗃️ Database Format (items.json)
json
Copy code
{
  "item_id": {
    "name": "Charger",
    "type": "lost",
    "category": "Electronics",
    "location": "Library",
    "color": "Black",
    "description": "Samsung charger",
    "reported_by": "user@example.com",
    "date": "2026-01-03 10:30:00",
    "status": "active"
  }
}
🌐 API Endpoints
User
POST /register

POST /login

GET /logout

GET /browse

POST /report

GET /api/my-items

GET /api/search

Admin
GET /admin/dashboard

GET /admin/items

POST /api/admin/verify/<item_id>

POST /api/admin/reject/<item_id>

GET /api/admin/matches/<item_id>

POST /api/admin/confirm-match/<item_id>/<match_id>

Contact
POST /contact

🎓 Academic Justification
Admin verification prevents fake claims

AI reduces manual effort

Manual confirmation ensures safety

Email notifications are controlled

JSON database used for simplicity

🚧 Known Limitations
SMTP email is synchronous (slight delay)

JSON database (not production-ready)

AI is rule-based (not ML)

🔮 Future Enhancements
Asynchronous email queue

Database integration (SQLite / MySQL)

Image-based similarity matching

College email restriction

Mobile application

Admin audit logs
