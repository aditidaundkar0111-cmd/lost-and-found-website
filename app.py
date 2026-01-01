from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta
import json
import os
import uuid
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from difflib import SequenceMatcher
import re
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Email configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# File paths
USERS_FILE = 'data/users.json'
ITEMS_FILE = 'data/items.json'
REPORTS_FILE = 'data/reports.json'
ADMINS_FILE = 'data/admins.json'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            # Compress image
            img = Image.open(filepath)
            img.thumbnail((800, 800))
            img.save(filepath, quality=85, optimize=True)
            return filename
        except:
            return None
    return None

# Initialize data files
def init_data_files():
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)   
    if not os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, 'w') as f:
            json.dump({}, f) 
    if not os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, 'w') as f:
            json.dump({}, f)  
    if not os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, 'w') as f:
            json.dump({'admin@lostandfound.com': generate_password_hash('admin123')}, f)
init_data_files()

# Utility functions
def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))   
        admins = load_json(ADMINS_FILE)
        if session['user_email'] not in admins:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def send_email(to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("✅ Email sent successfully")
        return True

    except Exception as e:
        print("❌ Email sending failed:", e)
        return False

def calculate_similarity(str1, str2):
    """Calculate similarity between two strings (0-1)"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_matches(item_id, item_type):
    """Find matching items using AI-like matching"""
    items = load_json(ITEMS_FILE)
    current_item = items.get(item_id, {})
    if not current_item:
        return []
    matches = []
    opposite_type = 'found' if item_type == 'lost' else 'lost'
    
    for id, item in items.items():
        if id == item_id or item.get('type') != opposite_type or item.get('status') == 'matched':
            continue
        
        # Calculate similarity scores
        name_similarity = calculate_similarity(current_item.get('name', ''), item.get('name', ''))
        category_match = 1.0 if current_item.get('category') == item.get('category') else 0.0
        location_similarity = calculate_similarity(current_item.get('location', ''), item.get('location', ''))
        color_match = 1.0 if current_item.get('color', '').lower() == item.get('color', '').lower() else 0.0
        
        # Weighted score
        score = (name_similarity * 0.4) + (category_match * 0.3) + (location_similarity * 0.2) + (color_match * 0.1)
        
        if score > 0.5:
            matches.append({
                'item_id': id,
                'name': item.get('name'),
                'category': item.get('category'),
                'location': item.get('location'),
                'color': item.get('color'),
                'score': round(score * 100, 2),
                'description': item.get('description'),
                'reported_by': item.get('reported_by'),
                'date': item.get('date')
            })
    
    return sorted(matches, key=lambda x: x['score'], reverse=True)

# Routes
@app.route('/')
def home():
    items = load_json(ITEMS_FILE)
    verified_count = sum(
        1 for item in items.values()
        if item.get('status') == 'active'
    )
    matched_count = sum(
        1 for item in items.values()
        if item.get('status') == 'matched'
    )
    total_items = verified_count + matched_count
    return render_template('index.html', verified_count=verified_count, total_items=total_items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password too short'}), 400
        if not email or not password or not name:
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        users = load_json(USERS_FILE)
        if email in users:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        users[email] = {
            'name': name,
            'password': generate_password_hash(password),
            'joined': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(USERS_FILE, users)
        return jsonify({'success': True, 'message': 'Registration successful!'}), 201
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        users = load_json(USERS_FILE)
        admins = load_json(ADMINS_FILE)
        
        # Check users
        if email in users and check_password_hash(users[email]['password'], password):
            session['user_email'] = email
            session['user_name'] = users[email]['name']
            session['is_admin'] = False
            return jsonify({'success': True, 'message': 'Login successful!'}), 200
        
        # Check admins
        if email in admins and check_password_hash(admins[email], password):
            session['user_email'] = email
            session['user_name'] = 'Admin'
            session['is_admin'] = True
            return jsonify({'success': True, 'message': 'Admin login successful!'}), 200
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/browse')
def browse():
    items = load_json(ITEMS_FILE)
    verified_items = [
        {**item, 'id': id} for id, item in items.items() 
        if item.get('verified') and item.get('status') != 'matched'
    ]
    return render_template('browse.html', items=verified_items)

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        data = request.form   
        required_fields = ['name', 'category', 'type', 'location', 'description']
        if not all(data.get(field) for field in required_fields):
            return jsonify({'success': False, 'message': 'All fields required'}), 400
        
        item_id = str(uuid.uuid4())
        items = load_json(ITEMS_FILE)
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            image_filename = save_image(request.files['image'])
        
        items[item_id] = {
            'name': data.get('name'),
            'category': data.get('category'),
            'type': data.get('type'),
            'location': data.get('location'),
            'color': data.get('color', ''),
            'description': data.get('description'),
            'image': image_filename,
            'reported_by': session['user_email'],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'verified': False,
            'status': 'pending'
        } 
        save_json(ITEMS_FILE, items) 
        return jsonify({'success': True, 'message': 'Item reported successfully! Awaiting admin verification.', 'item_id': item_id}), 201
    return render_template('report.html')

@app.route('/api/my-items')
@login_required
def my_items():
    items = load_json(ITEMS_FILE)
    user_items = [
        {**item, 'id': id} for id, item in items.items() 
        if item.get('reported_by') == session['user_email']
    ]
    return jsonify(user_items)

@app.route('/api/item/<item_id>/matches')
def get_item_matches(item_id):
    items = load_json(ITEMS_FILE)
    if item_id not in items:
        return jsonify({'error': 'Item not found'}), 404
    item_type = items[item_id].get('type')
    matches = find_matches(item_id, item_type)
    return jsonify(matches)

@app.route('/api/search')
def search_items():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    item_type = request.args.get('type', '')
    items = load_json(ITEMS_FILE)
    results = []
    for id, item in items.items():
        if not item.get('verified') or item.get('status') == 'matched':
            continue     
        if category and item.get('category') != category:
            continue    
        if item_type and item.get('type') != item_type:
            continue   
        if query and query not in item.get('name', '').lower() and query not in item.get('description', '').lower():
            continue 
        results.append({**item, 'id': id})
    return jsonify(results)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    items = load_json(ITEMS_FILE)
    pending = sum(1 for item in items.values() if item.get('status') == 'pending')
    verified = sum(1 for item in items.values() if item.get('verified'))
    matched = sum(1 for item in items.values() if item.get('status') == 'matched')
    
    return render_template('admin_dashboard.html', 
                         pending=pending, 
                         verified=verified, 
                         matched=matched)

@app.route('/admin/items')
@admin_required
def admin_items():
    items = load_json(ITEMS_FILE)
    all_items = [{**item, 'id': id} for id, item in items.items()]
    return render_template('admin_items.html', items=all_items)

@app.route('/api/admin/verify/<item_id>', methods=['POST'])
@admin_required
def verify_item(item_id):
    items = load_json(ITEMS_FILE)
    if item_id not in items:
        return jsonify({'error': 'Item not found'}), 404
    items[item_id]['verified'] = True
    items[item_id]['status'] = 'active'

    item_type = items[item_id]['type']
    matches = find_matches(item_id, item_type)

    if matches:
       best_match = matches[0]
       matched_id = best_match['item_id']

       # Mark both items as matched
       items[item_id]['status'] = 'matched'
       items[matched_id]['status'] = 'matched'

       # Email to LOST item user
       send_email(
           items[item_id]['reported_by'],
           "🎉 Match Found!",
           f"""
           <h2>🎉 Great News!</h2>

           <p>Your item <b>{items[item_id]['name']}</b> has been successfully matched.</p>

           <p>
           For safety and verification, user contact details are not shared directly.
           </p>

           <p>
           👉 Please <b>log in to the Lost & Found website</b> and contact the
           <b>Lost & Found Admin</b> using the Contact page to collect your item.
           </p>

           <p>
           The admin will verify the details and arrange a safe, supervised handover.
           </p>

           <p>
           Regards,<br>
           <b>Lost & Found Team</b>
           </p>
           """
       )

       # Email to FOUND item user
       send_email(
           items[matched_id]['reported_by'],
           "🎉 Match Found!",
           f"""
           <h2>🎉 Great News!</h2>

           <p>Your reported item <b>{items[matched_id]['name']}</b> has been successfully matched.</p>

           <p>
           For safety and verification, user contact details are not shared directly.
           </p>

           <p>
           👉 Please <b>log in to the Lost & Found website</b> and contact the
           <b>Lost & Found Admin</b> using the Contact page to hand over the item.
           </p>

           <p>
           The admin will verify the details and arrange a safe, supervised handover.
           </p>

           <p>
           Regards,<br>
           <b>Lost & Found Team</b>
           </p>
           """
       )

    # Save changes
    save_json(ITEMS_FILE, items)

    return jsonify({'success': True, 'message': 'Item verified'}), 200

@app.route('/api/admin/reject/<item_id>', methods=['POST'])
@admin_required
def reject_item(item_id):
    items = load_json(ITEMS_FILE)
    if item_id not in items:
        return jsonify({'error': 'Item not found'}), 404
    del items[item_id]
    save_json(ITEMS_FILE, items)
    return jsonify({'success': True, 'message': 'Item rejected'}), 200

@app.route('/api/item/<item_id>/notify', methods=['POST'])
@login_required
def notify_match(item_id):
    items = load_json(ITEMS_FILE)
    if item_id not in items:
        return jsonify({'error': 'Item not found'}), 404   
    item = items[item_id]
    recipient_email = item.get('reported_by')
    subject = f"Potential Match Found for Your {item.get('type').title()} Item!"
    message = f"""
    <h2>Match Alert</h2>
    <p>Hi {session.get('user_name')},</p>
    <p>We found a potential match for your {item.get('type')} item: <strong>{item.get('name')}</strong></p>
    <p><strong>Details:</strong></p>
    <ul>
        <li>Category: {item.get('category')}</li>
        <li>Location: {item.get('location')}</li>
        <li>Color: {item.get('color')}</li>
        <li>Date: {item.get('date')}</li>
    </ul>
    <p>Please log in to the website to view details and contact the person who reported the {item.get('type')} item.</p>
    <p>Best regards,<br>Lost & Found Team</p>
    """   
    if send_email(recipient_email, subject, message):
        return jsonify({'success': True, 'message': 'Notification sent!'}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to send email'}), 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.get_json()       
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()       
        if not all([name, email, subject, message]):
            return jsonify({'success': False, 'message': 'All fields required'}), 400        
        # Store contact message
        reports = load_json(REPORTS_FILE)
        reports[str(uuid.uuid4())] = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_json(REPORTS_FILE, reports)
        
        # Send confirmation to user
        response_message = f"""
        <h2>We Received Your Message</h2>
        <p>Hi {name},</p>
        <p>Thank you for contacting us about: <strong>{subject}</strong></p>
        <p>We will review your message and get back to you shortly.</p>
        <p>Best regards,<br>Lost & Found Team</p>
        """
        send_email(email, "We Received Your Message", response_message)        
        return jsonify({'success': True, 'message': 'Message sent! We will contact you soon.'}), 200   
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)