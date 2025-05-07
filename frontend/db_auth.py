from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import re
import bcrypt

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend JS

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sfs_infobot_db"]
users_collection = db["users"]

def validate_email(email):
    return re.match(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$", email)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    full_name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"success": False, "message": "Email already exists"}), 409

    users_collection.insert_one({
        "full_name": full_name,
        "email": email,
        "password": hash_password(password)
    })
    return jsonify({"success": True, "message": "Signup successful!"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    if user and check_password(user["password"], password):
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("newPassword")

    result = users_collection.update_one(
        {"email": email},
        {"$set": {"password": hash_password(new_password)}}
    )
    if result.matched_count == 0:
        return jsonify({"success": False, "message": "Email not found"}), 404
    return jsonify({"success": True, "message": "Password reset successful!"})

if __name__ == "__main__":
    app.run(debug=True)