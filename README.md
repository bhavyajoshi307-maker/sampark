# Sampark — Anonymous Vehicle Contact System

A QR-code-based system that lets bystanders anonymously contact a vehicle owner via quick alerts or live chat — without revealing anyone's identity.

## How It Works

1. A QR code is generated for each vehicle and physically attached to it
2. A bystander scans the QR code and lands on a contact page
3. They can send a **one-tap quick alert** (blocking, accident, lights on, request call) — forwarded instantly to the owner's Telegram
4. Or they can start an **anonymous live chat** with the owner via WebSockets
5. The owner receives a Telegram notification with a direct chat link whenever a new message arrives

## Folder Structure

```
sampark/
│
├── templates/
│   ├── contact.html        ← Quick alert + chat landing page
│   └── chat.html           ← Live anonymous chat UI
│
├── server.py               ← Flask + SocketIO backend
├── database.py             ← SQLite setup script
├── qr.py                   ← QR code generator
├── requirements.txt
└── vehicles.db             ← Auto-created on first run
```

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhavyajoshi307-maker/sampark.git
   cd sampark
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   python database.py
   ```

4. **Configure your settings** in `server.py` and `qr.py`:
   - Replace `BOT_TOKEN` with your Telegram bot token
   - Replace `BASE_URL` with your server's public URL (e.g. via [ngrok](https://ngrok.com))

5. **Generate QR codes**
   ```bash
   python qr.py
   ```

6. **Run the server**
   ```bash
   python server.py
   ```

## Registering as a Vehicle Owner (Telegram)

1. Open your Telegram bot
2. Send the command:
   ```
   /register CAR001
   ```
   Replace `CAR001` with your vehicle ID
3. You'll receive a confirmation message — you're now linked to that vehicle

## Tech Stack

- Python
- Flask
- Flask-SocketIO
- SQLite
- Telegram Bot API
- HTML / CSS / JavaScript
- qrcode
