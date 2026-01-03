🔍 Lost & Found Website

A secure, admin-verified Lost & Found web application with AI-assisted item matching and email notifications.

This project is developed as a college academic project and demonstrates a real-world workflow with admin control to prevent false claims.

📌 Project Overview

The Lost & Found Website allows users to report lost or found items.
An admin verifies each report and confirms matches using an AI-assisted matching system.

Items are never matched automatically.
Admin approval is mandatory to ensure safety and authenticity.

✨ Features
👤 User Features

User Registration & Login

Report Lost or Found Items

Browse Verified Items Only

Receive Email Notification after Match Confirmation

Contact Support via Contact Form

🛡️ Admin Features

Verify or Reject Reported Items

View AI-Suggested Matches

Manually Confirm Correct Matches

Trigger Email Notifications

Admin Dashboard with Statistics

🧠 Core Working Logic

Item Lifecycle

pending → active → matched

pending: Item reported by user (not visible publicly)

active: Admin verified (visible to all users)

matched: Admin confirmed match (emails sent)

AI only assists the admin.
The final decision is always manual.

🛠️ Technology Stack

Frontend: HTML5, Tailwind CSS

Backend: Python (Flask)

Database: JSON files

AI Matching: String similarity algorithm

Email Service: Gmail SMTP

Authentication: Session-based login

📁 Project Structure

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

⬆️ This is plain text, not a code block.
That’s why it will never turn horizontal.

🚀 Installation & Setup
Prerequisites

Python 3.8 or above

pip

Install Dependencies

Run the following command:

pip install -r requirements.txt

Configure Environment Variables

Create a .env file in the project root
(Do NOT upload this file to GitHub):

SECRET_KEY=your_secret_key
EMAIL_ADDRESS=yourgmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password


📌 Gmail App Password is required (2-Step Verification must be enabled).

Run the Application
python app.py


Access the website at:
http://localhost:5000

🔑 Default Admin Account

Email: admin@lostandfound.com

Password: admin123

📌 This is a system login ID, not an actual email inbox.

🔄 How the System Works
User Flow

Register / Login

Report Lost or Found Item

Item waits for admin verification

Browse verified items

Receive email after admin confirms match

Admin Flow

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

AI does not auto-match items.

📧 Email Notifications

No email on item report

No email on admin verification

Email sent only after admin confirms match

This prevents false notifications and misuse.

🎓 Academic Justification

Admin verification prevents fake claims

AI reduces manual effort

Manual confirmation ensures safety

Email notifications are controlled

JSON database used for simplicity

🚧 Known Limitations

SMTP email is synchronous (slight delay)

JSON database is not production-ready

AI is rule-based, not machine learning

🔮 Future Enhancements

Asynchronous email queue

Database integration (SQLite / MySQL)

Image-based similarity matching

College email restriction

Mobile application

Admin audit logs
