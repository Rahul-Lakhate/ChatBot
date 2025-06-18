from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple in-memory session tracker (not persistent)
user_sessions = {}

@app.route("/")
def home():
    return "🤖 Rahul Bank Chatbot is Running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    user_id = request.remote_addr  # simplistic session handling

    # Initialize session
    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": "greeting"}

    session = user_sessions[user_id]

    # Chat Flow
    if session["step"] == "greeting":
        session["step"] = "name"
        return jsonify({"reply": "Hi, this is the ChatBot created by Rahul. 👋\nMay I know your name, please?"})

    elif session["step"] == "name":
        session["name"] = user_input
        session["step"] = "menu"
        return jsonify({"reply": f"Nice to meet you, {user_input}! How can I assist you today?\n\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan\n\nPlease type the option number."})

    elif session["step"] == "menu":
        response_map = {
            "1": "💰 *Savings Account*: Our savings accounts offer up to 6% annual interest with zero maintenance charges. Ideal for daily banking with high returns.",
            "2": "🏦 *Current Account*: Perfect for businesses and frequent transactions. Enjoy overdraft, cheque books, and premium support.",
            "3": "💳 *Credit Card*: Choose from our rewards, cashback, or travel cards. 0% interest for the first 90 days. No joining fees!",
            "4": "💸 *Personal Loan*: Instant approvals up to ₹20 lakhs. Low interest starting at 10.25%. Minimal documentation required.",
            "5": "🚗 *Vehicle Loan*: Finance your dream car or bike with attractive EMIs and up to 100% on-road funding."
        }
        reply = response_map.get(user_input)
        if reply:
            session["step"] = "more_help"
            return jsonify({"reply": f"{reply}\n\nWould you like more assistance?\n\nType `1` to return to the main menu or `exit` to end the chat."})
        else:
            return jsonify({"reply": "⚠️ Invalid option. Please type a number between 1 and 5."})

    elif session["step"] == "more_help":
        if user_input == "1":
            session["step"] = "menu"
            return jsonify({"reply": "Back to Main Menu:\n\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan"})
        elif user_input.lower() == "exit":
            user_sessions.pop(user_id, None)
            return jsonify({"reply": "🙏 Thank you for chatting with Rahul Bank. Have a great day!"})
        else:
            return jsonify({"reply": "Please type `1` for main menu or `exit` to end the chat."})

    else:
        session["step"] = "menu"
        return jsonify({"reply": "Let’s start over. Please select an option:\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan"})
