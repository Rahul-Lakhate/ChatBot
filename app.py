from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# In-memory session storage
user_sessions = {}

@app.route("/")
def home():
    return "🤖 Rahul Bank Chatbot is Running!"

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

    # Step 2: Get name
    elif session["step"] == "name":
        session["name"] = user_input
        session["step"] = "menu"
        return jsonify({"reply": f"Nice to meet you, {user_input}! How can I assist you today?\n\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan\n\nPlease type the option number."})

    # Step 3: Show service and ask for next action
    elif session["step"] == "menu":
        services = {
            "1": "💰 *Savings Account*: Our savings accounts offer up to 6% annual interest with zero maintenance charges.",
            "2": "🏦 *Current Account*: Perfect for businesses and frequent transactions. Overdraft, cheque book, premium support.",
            "3": "💳 *Credit Card*: Rewards, cashback, travel cards. 0% interest for 90 days. No joining fee!",
            "4": "💸 *Personal Loan*: Instant approvals up to ₹20 lakhs. Low interest starting at 10.25%.",
            "5": "🚗 *Vehicle Loan*: Attractive EMIs and up to 100% on-road funding for your dream car or bike."
        }

        if user_input in services:
            session["last_option"] = user_input
            session["step"] = "after_service"
            return jsonify({"reply": f"{services[user_input]}\n\nReply with:\n1️⃣ Main Menu\n2️⃣ Know More\n0️⃣ Exit"})
        else:
            return jsonify({"reply": "⚠️ Invalid option. Please type a number between 1 and 5."})

    # Step 4: After showing service details
    elif session["step"] == "after_service":
        if user_input == "1":
            session["step"] = "menu"
            return jsonify({"reply": "Back to Main Menu:\n\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan"})
        elif user_input == "2":
            session["step"] = "more_help"
            return jsonify({"reply": (
                "📞 This is a *testing bot*. We have lesser details available right now.\n"
                "🧑‍💼 Our banking agent will get in touch with you shortly.\n\n"
                "Reply with:\n1️⃣ Main Menu\n0️⃣ Exit"
            )})
        elif user_input == "0":
            user_sessions.pop(user_id, None)
            return jsonify({"reply": "🙏 Thank you for chatting with Rahul Bank. Have a great day!"})
        else:
            return jsonify({"reply": "Please type 1️⃣ for Main Menu, 2️⃣ for more info, or 0️⃣ to Exit."})

    # Step 5: After 'Know More'
    elif session["step"] == "more_help":
        if user_input == "1":
            session["step"] = "menu"
            return jsonify({"reply": "Back to Main Menu:\n\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan"})
        elif user_input == "0":
            user_sessions.pop(user_id, None)
            return jsonify({"reply": "🙏 Thank you for chatting with Rahul Bank. Have a great day!"})
        else:
            return jsonify({"reply": "Please type 1️⃣ for Main Menu or 0️⃣ to Exit."})

    # Default fallback
    else:
        session["step"] = "menu"
        return jsonify({"reply": "Let’s start over. Please choose a service:\n1. Savings Account\n2. Current Account\n3. Credit Card\n4. Personal Loan\n5. Vehicle Loan"})
