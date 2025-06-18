from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple in-memory session tracker
user_sessions = {}

@app.route("/")
def home():
    return render_template("index.html")  # Serves index.html from /templates

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    user_id = request.remote_addr

    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": "greeting"}

    session = user_sessions[user_id]

    # Step 1: Greet and ask name
    if session["step"] == "greeting":
        session["step"] = "name"
        return jsonify({"reply": "Hi, this is the ChatBot created by Rahul. 👋\nMay I know your name, please?"})

    elif session["step"] == "name":
        session["name"] = user_input
        session["step"] = "menu"
        return jsonify({"reply": f"Nice to meet you, {user_input}! How can I assist you today?\n\n"
                                 "1. Savings Account\n2. Current Account\n3. Credit Card\n"
                                 "4. Personal Loan\n5. Vehicle Loan\n\nPlease type the option number."})

    elif session["step"] == "menu":
        services = {
            "1": "💰 *Savings Account*: Up to 6% interest. Zero maintenance. 24x7 access.",
            "2": "🏦 *Current Account*: Ideal for businesses. Overdraft, cheque, priority support.",
            "3": "💳 *Credit Card*: Rewards, cashback & 0% interest for 90 days.",
            "4": "💸 *Personal Loan*: Up to ₹20L, 10.25% rate, instant disbursal.",
            "5": "🚗 *Vehicle Loan*: Finance up to 100% on-road price. Low EMIs."
        }
        if user_input in services:
            session["last_option"] = user_input
            session["step"] = "after_service"
            return jsonify({"reply": f"{services[user_input]}\n\n"
                                     "Reply with:\n1️⃣ Main Menu\n2️⃣ Know More\n0️⃣ Exit"})
        else:
            return jsonify({"reply": "⚠️ Invalid option. Please type 1–5."})

    elif session["step"] == "after_service":
        if user_input == "1":
            session["step"] = "menu"
            return jsonify({"reply": "Back to Main Menu:\n\n"
                                     "1. Savings Account\n2. Current Account\n3. Credit Card\n"
                                     "4. Personal Loan\n5. Vehicle Loan"})
        elif user_input == "2":
            session["step"] = "more_help"
            return jsonify({"reply": "📞 This is a *testing bot*. Limited details available.\n"
                                     "🧑‍💼 A banking agent will contact you shortly.\n\n"
                                     "Reply with:\n1️⃣ Main Menu\n0️⃣ Exit"})
        elif user_input == "0":
            user_sessions.pop(user_id, None)
            return jsonify({"reply": "🙏 Thank you for chatting with Rahul Bank. Goodbye!"})
        else:
            return jsonify({"reply": "Please reply with 1️⃣, 2️⃣, or 0️⃣."})

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

    else:
        session["step"] = "menu"
        return jsonify({"reply": "Let’s start over. Select an option:\n1–Savings\n2–Current\n3–Credit Card\n4–Loan\n5–Vehicle Loan"})
