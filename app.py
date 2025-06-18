from flask import Flask, request, jsonify, send_file
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# In-memory session tracking
user_sessions = {}

@app.route("/")
def home():
    return send_file("index.html")  # Serves index.html from root directory

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    user_id = request.remote_addr

    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": "greeting"}

    session = user_sessions[user_id]

    # Step 1: Greeting
    if session["step"] == "greeting":
        session["step"] = "name"
        return jsonify({"reply": "Hi, this is the ChatBot created by Rahul. 👋\nMay I know your name, please?"})

    # Step 2: Capture Name
    elif session["step"] == "name":
        session["name"] = user_input
        session["step"] = "menu"
        return jsonify({"reply": f"Nice to meet you, {user_input}! How can I assist you today?\n\n"
                                 "1. Savings Account\n2. Current Account\n3. Credit Card\n"
                                 "4. Personal Loan\n5. Vehicle Loan\n\nPlease type the option number."})

    # Step 3: Show selected service info
    elif session["step"] == "menu":
        services = {
            "1": "💰 *Savings Account*: Earn up to 6% annual interest. No maintenance fees.",
            "2": "🏦 *Current Account*: Ideal for business transactions. Overdrafts, cheques & support.",
            "3": "💳 *Credit Card*: 0% interest for 90 days, rewards, cashback and travel perks.",
            "4": "💸 *Personal Loan*: Up to ₹20 lakhs, low interest, instant disbursal.",
            "5": "🚗 *Vehicle Loan*: Get up to 100% on-road funding. Low EMI options available."
        }

        if user_input in services:
            session["last_option"] = user_input
            session["step"] = "after_service"
            return jsonify({"reply": f"{services[user_input]}\n\n"
                                     "Reply with:\n1️⃣ Main Menu\n2️⃣ Know More\n0️⃣ Exit"})
        else:
            return jsonify({"reply": "⚠️ Invalid option. Please type a number between 1 and 5."})

    # Step 4: After showing service
    elif session["step"] == "after_service":
        if user_input == "1":
            session["step"] = "menu"
            return jsonify({"reply": "Back to Main Menu:\n\n"
                                     "1. Savings Account\n2. Current Account\n3. Credit Card\n"
                                     "4. Personal Loan\n5. Vehicle Loan"})
        elif user_input == "2":
            session["step"] = "more_help"
            return jsonify({"reply": "📞 This is a *testing bot*. Our agents will contact you soon.\n\n"
                                     "Reply with:\n1️⃣ Main Menu\n0️⃣ Exit"})
        elif user_input == "0":
            user_sessions.pop(user_id, None)
            return jsonify({"reply": "🙏 Thank you for chatting with Rahul Bank. Have a great day!"})
        else:
            return jsonify({"reply": "Please reply with 1️⃣, 2️⃣, or 0️⃣."})

    # Step 5: After know more
    elif session["step"] == "more_help":
        if user_input == "1":
            session["step"] = "menu"
            return jsonify({"reply": "Back to Main Menu:\n\n"
                                     "1. Savings Account\n2. Current Account\n3. Credit Card\n"
                                     "4. Personal Loan\n5. Vehicle Loan"})
        elif user_input == "0":
            user_sessions.pop(user_id, None)
            return jsonify({"reply": "🙏 Thank you for chatting with Rahul Bank. Goodbye!"})
        else:
            return jsonify({"reply": "Please reply with 1️⃣ for Main Menu or 0️⃣ to Exit."})

    # Default reset
    else:
        session["step"] = "menu"
        return jsonify({"reply": "Let’s start over. Please choose:\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan"})

