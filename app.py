from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

# Session memory (very basic; resets every restart)
user_sessions = {}

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    session_id = request.remote_addr  # basic session by IP

    if session_id not in user_sessions:
        user_sessions[session_id] = {
            "step": 0,
            "data": {}
        }

    session = user_sessions[session_id]
    step = session["step"]

    # Step 0: Welcome Message
    if step == 0:
        session["step"] += 1
        return jsonify({"reply": "Hi, this is the ChatBot created by Rahul. 👋\nWhat's your full name?"})

    # Step 1: Get Name
    elif step == 1:
        session["data"]["name"] = user_input
        session["step"] += 1
        return jsonify({"reply": f"Nice to meet you, {user_input} 😊. Can you share your phone number?"})

    # Step 2: Get Phone
    elif step == 2:
        session["data"]["phone"] = user_input
        session["step"] += 1
        return jsonify({"reply": "Got it! What's your email address?"})

    # Step 3: Get Email
    elif step == 3:
        session["data"]["email"] = user_input
        session["step"] += 1
        return jsonify({"reply": "Thank you. Please tell me your location (City or State) 🌍"})

    # Step 4: Get Location
    elif step == 4:
        session["data"]["location"] = user_input
        session["step"] += 1
        return jsonify({"reply": "What type of bank account are you looking for?\nPlease select one:\n1️⃣ Savings\n2️⃣ Current\n3️⃣ Salary\n4️⃣ Fixed Deposit"})

    # Step 5: Choose Account Type
    elif step == 5:
        options = {
            "1": "Savings",
            "2": "Current",
            "3": "Salary",
            "4": "Fixed Deposit"
        }
        selection = options.get(user_input.strip())

        if selection:
            session["data"]["account_type"] = selection
            session["step"] += 1
            return jsonify({"reply": f"You selected '{selection}' account.\n\n✅ Initial funding of ₹1,000 is required.\n📋 Basic KYC documents are mandatory.\n📅 Account will be activated in 24–48 hours.\n\nDo you agree to the terms and wish to proceed? (Yes/No)"})
        else:
            return jsonify({"reply": "⚠️ Please reply with a valid option number (1–4)."})

    # Step 6: Confirm Submission
    elif step == 6:
        if user_input.lower() in ["yes", "y"]:
            name = session["data"].get("name")
            acc_type = session["data"].get("account_type")
            session["step"] += 1
            return jsonify({"reply": f"🎉 Thank you {name}! Your request to open a {acc_type} account has been recorded. Our executive will contact you shortly."})
        else:
            session["step"] += 1
            return jsonify({"reply": "❌ No problem. You can start the process again anytime."})

    # Step 7+: Ended
    else:
        return jsonify({"reply": "🙏 Thank you for using Rahul's ChatBot. Type 'restart' to begin again."})

@app.route("/restart", methods=["POST"])
def restart():
    session_id = request.remote_addr
    user_sessions.pop(session_id, None)
    return jsonify({"reply": "🔄 Session restarted. Hi, this is the ChatBot created by Rahul. What's your full name?"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
