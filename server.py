from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import sqlite3
import requests

app = Flask(__name__)
socketio = SocketIO(app)

BOT_TOKEN = "8668073115:AAEJcQwH9UNZgTxkHDG1myi3Dv0VQGUlHNw"

BASE_URL = "https://argentina-unvenerable-lorita.ngrok-free.dev/"


# -----------------------------
# Database helper
# -----------------------------
def get_db():
    return sqlite3.connect("vehicles.db", check_same_thread=False)


# -----------------------------
# Telegram notification
# -----------------------------
def notify_telegram(chat_id, message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=data)


# -----------------------------
# Get owner
# -----------------------------
def get_vehicle_owner(vehicle):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT chat_id FROM owners WHERE vehicle_id=?",
        (vehicle,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]

    return None


# -----------------------------
# Save message
# -----------------------------
def save_message(vehicle, message, sender):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chat_messages VALUES(?,?,?)",
        (vehicle, message, sender)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Load history
# -----------------------------
def load_messages(vehicle):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT message, sender FROM chat_messages WHERE vehicle=?",
        (vehicle,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# -----------------------------
# Telegram webhook
# -----------------------------
@app.route("/telegram", methods=["POST"])
def telegram_webhook():

    data = request.json

    if "message" in data:

        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.lower().startswith("/register"):

            parts = text.split()

            if len(parts) == 2:

                vehicle = parts[1].upper()

                conn = get_db()
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT OR REPLACE INTO owners(vehicle_id, chat_id) VALUES (?,?)",
                    (vehicle, chat_id)
                )

                conn.commit()
                conn.close()

                notify_telegram(
                    chat_id,
                    f"✅ Vehicle {vehicle} registered successfully."
                )

    return "ok"


# -----------------------------
# Vehicle contact page
# -----------------------------
@app.route("/vehicle/<vehicle_id>")
def vehicle_page(vehicle_id):

    return render_template(
        "contact.html",
        vehicle_id=vehicle_id
    )

@app.route("/quick_alert", methods=["POST"])
def quick_alert():

    vehicle = request.form["vehicle"]
    message = request.form["message"]

    owner = get_vehicle_owner(vehicle)

    if owner:

        notify_telegram(
            owner,
            f"🚗 Sampark Alert\n\nVehicle: {vehicle}\n\n{message}"
        )

    return render_template(
        "contact.html",
        vehicle_id=vehicle
    )

# -----------------------------
# Chat page
# -----------------------------
@app.route("/chat/<vehicle>")
def chat_page(vehicle):

    history = load_messages(vehicle)

    return render_template(
        "chat.html",
        vehicle=vehicle,
        history=history
    )


@app.route("/start_chat", methods=["POST"])
def start_chat():

    vehicle = request.form["vehicle"]

    history = load_messages(vehicle)

    return render_template(
        "chat.html",
        vehicle=vehicle,
        history=history
    )


# -----------------------------
# Join room
# -----------------------------
@socketio.on("join")
def join(data):

    vehicle = data["vehicle"]

    join_room(vehicle)


# -----------------------------
# Send message
# -----------------------------
@socketio.on("message")
def handle_message(data):

    vehicle = data["vehicle"]
    msg = data["message"]

    save_message(vehicle, msg, request.sid)

    emit("message", {
        "message": msg,
        "sender": request.sid
    }, room=vehicle)

    owner = get_vehicle_owner(vehicle)

    room_users = socketio.server.manager.rooms["/"].get(vehicle, set())

    history = load_messages(vehicle)

    if owner and len(room_users) < 2 and len(history) == 1:

        chat_link = f"{BASE_URL}/chat/{vehicle}"

        notify_telegram(
            owner,
            f"🚗 Sampark Alert\n\nNew message for vehicle {vehicle}\n\n\"{msg}\"\n\nOpen chat:\n{chat_link}"
        )


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
    