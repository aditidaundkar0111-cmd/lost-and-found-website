# Lost & Found Website

A modern, full-featured lost and found platform with AI-powered item matching, admin verification, and email notifications.

## Features

✨ **Core Features:**
- 🔐 User authentication (Login/Register)
- 📝 Report lost or found items
- 🔍 Browse verified items with advanced filters
- 🤖 AI-powered item matching system
- 📧 Email notifications for matches
- ✅ Admin verification system
- 📞 Contact form
- 📊 Admin dashboard

## Technology Stack

- **Frontend:** HTML5, Tailwind CSS (responsive design via CDN)
- **Backend:** Python Flask
- **Database:** JSON files
- **Email:** SMTP (Gmail)
- **AI Matching:** String similarity algorithm

## Project Structure

```
lost_found_website/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html        # Base layout with navbar
│   ├── index.html       # Home page
│   ├── register.html    # Registration page
│   ├── login.html       # Login page
│   ├── browse.html      # Browse items page
│   ├── report.html      # Report item page
│   ├── contact.html     # Contact page
│   ├── admin_dashboard.html  # Admin dashboard
│   └── admin_items.html      # Admin item management
├── static/
│   ├── css/
│   │   └── style.css    # Complete styling
│   └── js/
│       └── (scripts in HTML files)
└── data/               # JSON database files
    ├── users.json
    ├── items.json
    ├── reports.json
    └── admins.json
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd lost_found_website
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Email (Optional)
Edit `app.py` and update email configuration:
```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
```

To use Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an app password: https://myaccount.google.com/apppasswords
3. Use the app password in the config

### Step 4: Run the Application
```bash
python app.py
```

The website will be available at: **http://localhost:5000**

## Default Admin Account

- **Email:** admin@lostandfound.com
- **Password:** admin123

⚠️ Change this in production!

## How to Use

### For Regular Users:
1. **Register/Login** - Create your account
2. **Report Item** - Report a lost or found item
3. **Browse** - Check other reported items
4. **Get Notified** - Receive email when matches are found

### For Admins:
1. Login with admin credentials
2. Go to **Admin Dashboard**
3. Manage items and verify reports
4. View statistics and system status

## Features Explained

### 🤖 AI Matching System
Automatically matches items based on:
- Item name similarity (40% weight)
- Category match (30% weight)
- Location similarity (20% weight)
- Color match (10% weight)

Items with >50% match score are suggested to users.

### 📧 Email Notifications
When a match is found, users receive an email with:
- Potential match details
- Matching percentage
- Contact information

### ✅ Admin Verification
- All new reports require admin approval
- Admins can verify or reject items
- Prevents spam and false reports
- Ensures platform authenticity

## Database Structure

### Users (users.json)
```json
{
  "user@example.com": {
    "name": "User Name",
    "password": "hashed_password",
    "joined": "2025-12-27 10:30:00"
  }
}
```

### Items (items.json)
```json
{
  "item_id": {
    "name": "iPhone 14",
    "type": "lost",
    "category": "Electronics",
    "location": "Central Park",
    "color": "Black",
    "description": "Black iPhone 14 Pro...",
    "reported_by": "user@example.com",
    "date": "2025-12-27 10:30:00",
    "verified": true,
    "status": "active"
  }
}
```

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout

### Items
- `GET /browse` - Browse verified items
- `POST /report` - Report new item
- `GET /api/search` - Search with filters
- `GET /api/my-items` - Get user's items
- `GET /api/item/<id>/matches` - Get matches for item

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/items` - Manage items
- `POST /api/admin/verify/<id>` - Verify item
- `POST /api/admin/reject/<id>` - Reject item

### Other
- `POST /contact` - Contact form
- `POST /api/chatbot` - Chatbot response
- `POST /api/item/<id>/notify` - Send notification

## Customization

### Change Colors
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    ...
}
```

### Modify Categories
Edit the category options in:
- `templates/report.html`
- `templates/browse.html`

### Adjust Matching Algorithm
Modify the `find_matches()` function in `app.py` to change:
- Similarity thresholds
- Weight distribution
- Matching criteria

## Troubleshooting

### Port 5000 already in use
```bash
python app.py --port 5001
```

### Emails not sending
- Verify email configuration in `app.py`
- Check Gmail app password
- Verify firewall allows SMTP connections

### Database errors
- Check permissions on `data/` folder
- Ensure JSON files are not corrupted
- Delete data files to reset

## Future Enhancements

- 📸 Image upload for items
- 🗺️ Google Maps integration
- 💬 Messaging between users
- 🔔 Push notifications
- 📱 Mobile app
- 💳 Reward system
- 🌐 Multi-language support
- 🔒 Enhanced security features

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
- Create an issue on GitHub
- Contact: support@lostandfound.com
- Use the in-app chat assistant

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Happy Finding! 🔍** Help reunite lost items with their owners.
