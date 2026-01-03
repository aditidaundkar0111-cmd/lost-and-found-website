# 🔍 Lost & Found Website

A secure, admin-verified Lost & Found web application with AI-assisted item matching and email notifications.

This project is developed as a college academic project and demonstrates a real-world workflow with admin control to prevent false claims.

---

## 📌 Project Overview

The Lost & Found Website allows users to report lost or found items.
Each reported item is verified by an admin before it becomes visible.
AI assists the admin in suggesting possible matches, but final confirmation is always manual.

---

## ✨ Features

### User Features
- User registration and login
- Report lost or found items
- Browse only verified items
- Receive email notification after match confirmation
- Contact support via contact form

### Admin Features
- Verify or reject reported items
- View AI-suggested matches
- Manually confirm correct matches
- Trigger email notifications
- View dashboard statistics

---

## 🔄 Item Lifecycle

pending → active → matched

pending: Item reported by user (not visible publicly)  
active: Admin verified (visible to all users)  
matched: Admin confirmed match (emails sent)

AI only assists the admin.  
The final decision is always manual.

---

## 🛠️ Technology Stack

Frontend: HTML5, Tailwind CSS  
Backend: Python (Flask)  
Database: JSON files  
AI Matching: String similarity algorithm  
Email Service: Gmail SMTP  
Authentication: Session-based login  

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
- Python 3.8 or above
- pip

### Install Dependencies
pip install -r requirements.txt

csharp
Copy code

### Configure Environment Variables

Create a `.env` file in the project root  
(Do NOT upload this file to GitHub)

SECRET_KEY=your_secret_key
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

vbnet
Copy code

Note: Gmail App Password is required (2-Step Verification must be enabled).

### Run the Application
python app.py

yaml
Copy code

Access the website at:
http://localhost:5000

---

## 🔑 Default Admin Account

Email: admin@lostandfound.com  
Password: admin123  

This is a system login ID, not an actual email inbox.

---

## 🔄 How the System Works

### User Flow
1. Register or login
2. Report lost or found item
3. Item waits for admin verification
4. Browse verified items
5. Receive email after admin confirms match

### Admin Flow
1. Login as admin
2. Verify or reject items
3. View AI-suggested matches
4. Confirm correct match
5. Emails sent to both users
6. Item marked as matched

---

## 🤖 AI Matching System

AI suggests matches based on:
- Item name similarity
- Category match
- Location similarity
- Color match

Only matches with more than 50% similarity score are suggested.

AI does not auto-match items.

---

## 📧 Email Notifications

- No email on item report
- No email on admin verification
- Email sent only after admin confirms match

This prevents false notifications and misuse.

---

## 🎓 Academic Justification

- Admin verification prevents fake claims
- AI reduces manual effort
- Manual confirmation ensures safety
- Controlled email notifications
- JSON database used for simplicity

---

## 🚧 Known Limitations

- SMTP email is synchronous (slight delay)
- JSON database is not production-ready
- AI is rule-based, not machine learning

---

## 🔮 Future Enhancements

- Asynchronous email queue
- Database integration (SQLite / MySQL)
- Image-based similarity matching
- College email restriction
- Mobile application
- Admin audit logs

---
