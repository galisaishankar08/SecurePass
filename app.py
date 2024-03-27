from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from passwordpolicy import PasswordPolicy

app = Flask(__name__)
password_policy = PasswordPolicy()

# Enable CORS for all domains on all routes
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    
    password = data.get('password')
    name = data.get('name')
    dob = data.get('dob')
    email = data.get('email')
    
    if not all([password, name, dob, email]):
        return jsonify({"error": "Missing data for password check."}), 400

    is_secure, message = password_policy.is_password_secure(password, name, dob, email)
    return jsonify({"is_secure": is_secure, "message": message})

if __name__ == "__main__":
    app.run(debug=True)
