from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import string

app = Flask(__name__)

# List of common passwords
common_passwords = [
    "123456", "password", "123456789", "12345678", "12345", "1234567",
    "qwerty", "abc123", "password1", "123123", "admin", "letmein", "welcome"
]

# Function to check password strength
def check_password_strength(password):
    feedback = []
    score = 0

    # Length criteria
    if len(password) >= 8:
        score += 20
    else:
        feedback.append("Use at least 8 characters.")

    # Uppercase criteria
    if any(char.isupper() for char in password):
        score += 20
    else:
        feedback.append("Add uppercase letters.")

    # Lowercase criteria
    if any(char.islower() for char in password):
        score += 20
    else:
        feedback.append("Add lowercase letters.")

    # Numbers criteria
    if any(char.isdigit() for char in password):
        score += 20
    else:
        feedback.append("Include numbers.")

    # Special characters criteria
    if any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for char in password):
        score += 20
    else:
        feedback.append("Add special characters.")

    # Determine strength
    if score <= 40:
        strength = "Weak"
    elif score <= 80:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, feedback, score

# Function to generate a random password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    # Simple validation 
    if username == "admin" and password == "admin123":
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/password_checker')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    strength, feedback, score = check_password_strength(password)
    suggested_password = generate_password() if strength != "Strong" else None
    return jsonify({
        "strength": strength,
        "feedback": feedback,
        "score": score,
        "suggested_password": suggested_password
    })

@app.route('/awareness')
def awareness():
    tips = [
        "Use a password that is at least 8 characters long.",
        "Include a mix of uppercase and lowercase letters, numbers, and special characters.",
        "Avoid using common passwords like '123456', 'password', or your name.",
        "Do not reuse the same password across multiple accounts.",
        "Enable two-factor authentication (2FA) whenever possible for extra security.",
        "Change your passwords regularly to reduce the risk of compromise."
    ]
    return render_template('awareness.html', tips=tips)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
