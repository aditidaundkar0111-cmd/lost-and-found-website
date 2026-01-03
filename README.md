📦 Lost & Found Website

A secure, admin-verified lost and found system with AI-assisted matching

📌 Project Overview

This project is a college-level Lost & Found web application designed to help users report, verify, and recover lost items safely.
The system uses admin verification and AI-assisted matching to prevent false claims and ensure secure item handover.


✨ Key Features

👤 User Features
🔐 User Registration & Login
📝 Report Lost or Found Items
🔍 Browse Verified Items Only
🤖 View AI-suggested matches (admin-controlled)
📧 Email notifications after match confirmation
📞 Contact support via contact form


🛡️ Admin Features

✅ Verify or Reject reported items
🔍 View AI-suggested item matches
🤝 Manually confirm correct matches
📧 Trigger email notifications after confirmation
📊 Dashboard with item statistics


🧠 Core System Logic (Very Important)

Item Lifecycle
pending → active → matched

pending → Item reported by user (not public)
active → Admin verified (visible to all users)
matched → Admin confirmed match (emails sent)

📌 There is NO automatic matching or auto-emailing
📌 Admin always takes the final decision


🛠️ Technology Stack

Frontend: HTML5, Tailwind CSS
Backend: Python (Flask)
Database: JSON files
AI Matching: String similarity (SequenceMatcher)
Email: Gmail SMTP
Authentication: Session-based login


📂 Project Structure
lost_found_website/
├── app.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── browse.html
│   ├── report.html
│   ├── contact.html
│   ├── admin_dashboard.html
│   └── admin_items.html
├── static/
│   └── uploads/
└── data/
    ├── users.json
    ├── items.json
    ├── reports.json
    └── admins.json


🚀 Installation & Setup

Prerequisites
Python 3.8+
pip
Step 1: Install Dependencies
pip install -r requirements.txt

Step 2: Configure Email (.env)
SECRET_KEY=your_secret_key
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_app_password
📌 Gmail App Password is required (2FA enabled)

Step 3: Run Application
python app.py

Access at:
👉 http://localhost:5000


🔑 Default Admin Account
Field	Value
Email	admin@lostandfound.com
Password	admin123
📌 This is a system login ID, not an actual mailbox.

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
Manually confirm correct match
Emails sent to both users
Item marked as matched


🤖 AI Matching System

AI suggests matches using:
Name similarity (40%)
Category match (30%)
Location similarity (20%)
Color match (10%)
Only matches with >50% score are suggested.
📌 AI assists admin, it does not decide automatically.


📧 Email Notifications

Emails are sent only when admin confirms a match.
No email on report
No email on verification
Email only after confirmation
This ensures no false notifications.


🗃️ Database Format
items.json
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


🎓 Academic Justification (Viva Ready)

Admin verification prevents fake claims
AI reduces manual effort
Manual confirmation ensures safety
Email only after verification avoids misuse
JSON database used for simplicity


🚧 Known Limitations

SMTP email is synchronous (may be slow)
JSON database (not for production)
AI is rule-based, not ML


🔮 Future Enhancements

Async email queue
Database (SQLite / MySQL)
Image similarity matching
College email restriction
Mobile app
Admin audit logs