from flask import Flask, request, jsonify, send_file
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

user_sessions = {}

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    user_id = request.remote_addr

    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": "name"}
        return jsonify({"reply": "Hi, this is the ChatBot created by Rahul. 👋\nMay I know your full name, please?"})

    session = user_sessions[user_id]

    if session["step"] == "name":
        session["name"] = user_input
        session["step"] = "phone"
        return jsonify({"reply": f"Thanks, {user_input}. 📱 May I have your phone number?"})

    elif session["step"] == "phone":
        session["phone"] = user_input
        session["step"] = "email"
        return jsonify({"reply": "📧 Got it. Please provide your email address."})

    elif session["step"] == "email":
        session["email"] = user_input
        session["step"] = "location"
        return jsonify({"reply": "🌍 Great. Now, tell me your current city or location."})

    elif session["step"] == "location":
        session["location"] = user_input
        session["step"] = "menu"
        return jsonify({"reply": menu_message()})

    elif session["step"] == "menu":
        services = {
            "1": "💰 *Savings Account*: High interest, zero balance, 24/7 access.",
            "2": "🏦 *Current Account*: Business-friendly, bulk transfers, cheque book facility.",
            "3": "💳 *Credit Card*: Cashback, lounge access, fuel benefits.",
            "4": "💸 *Personal Loan*: Up to ₹20L, low interest, fast approval.",
            "5": "🚗 *Vehicle Loan*: 100% on-road price funding with flexible EMIs."
        }
        if user_input in services:
            session["last_service"] = user_input
            session["step"] = "after_service"
            return jsonify({"reply": f"{services[user_input]}\n\nReply with:\n1️⃣ Main Menu\n2️⃣ Know More\n0️⃣ Exit"})
        else:
            return jsonify({"reply": "⚠️ Please choose a valid option (1–5)."})

    elif session["step"] == "after_service":
        if user_input == "1":
            session["step"] = "menu"
            return jsonify({"reply": menu_message()})
        elif user_input == "2":
            session["step"] = "more_help"
            return jsonify({"reply": "📞 Thank you for your interest! Since this is a testing bot, we have limited info right now.\nOur banking agent will contact you shortly with complete details."})
        elif user_input == "0":
            user_sessions.pop(user_id, None)
            return jsonify({"reply": "🙏 Thank you for chatting with Rahul Bank. Goodbye!"})
        else:
            return jsonify({"reply": "Please type 1️⃣ for Main Menu, 2️⃣ for more info, or 0️⃣ to Exit."})

    elif session["step"] == "more_help":
        return jsonify({"reply": "👋 Is there anything else I can help with?\nType 1 for Main Menu or 0 to Exit."})

    return jsonify({"reply": "I didn't understand that. Please use the available options or type `0` to exit."})

def menu_message():
    return (
        "Main Menu:\n\n"
        "1️⃣ Savings Account\n"
        "2️⃣ Current Account\n"
        "3️⃣ Credit Card\n"
        "4️⃣ Personal Loan\n"
        "5️⃣ Vehicle Loan\n\n"
        "Please type the number of the service you'd like to explore."
    )
