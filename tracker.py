import requests
import json
import os
from datetime import date

# ── CONFIG ──────────────────────────────────────────────
# TWILIO_SID    = "PASTE_YOUR_SID_HERE"
# TWILIO_TOKEN  = "PASTE_YOUR_TOKEN_HERE"
# FROM_WHATSAPP = "whatsapp:+14155238886"
# TO_WHATSAPP   = "whatsapp:+91XXXXXXXXX"  # your Indian number

TWILIO_SID    = os.getenv("TWILIO_SID")
TWILIO_TOKEN  = os.getenv("TWILIO_TOKEN")
FROM_WHATSAPP = "whatsapp:+14155238886"
TO_WHATSAPP   = os.getenv("TO_WHATSAPP")

THRESHOLD     = 0.01
STATE_FILE = "eur_inr_state.json"
# ────────────────────────────────────────────────────────

def is_active_period():
    today = date.today()
    return today.day >= 20 or today.day == 1

def get_rate():
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return round(r.json()["rates"]["INR"], 4)

def load_state():
    today = str(date.today())
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
        if state.get("date") == today:
            return state
    return {
        "date": today,
        "last_notified_rate": None,
        "day_high": None,
        "day_low": None,
        "high_notified": False,
        "low_notified": False,
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def send_whatsapp(msg):
    from twilio.rest import Client
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(body=msg, from_=FROM_WHATSAPP, to=TO_WHATSAPP)
    print(f"Sent: {msg}")

def main():
    if not is_active_period():
        print(f"Outside active period (day {date.today().day}). Skipping.")
        return

    rate = get_rate()
    state = load_state()
    messages = []

    if state["last_notified_rate"] is None:
        state["last_notified_rate"] = rate
        state["day_high"] = rate
        state["day_low"] = rate
        save_state(state)
        print(f"Initialised. Current EUR/INR: {rate}")
        return

    new_high = rate > state["day_high"]
    new_low  = rate < state["day_low"]

    if new_high:
        state["day_high"] = rate
        state["high_notified"] = False
    if new_low:
        state["day_low"] = rate
        state["low_notified"] = False

    if new_high and not state["high_notified"]:
        messages.append(f"📈 *EUR/INR Daily High!*\nRate: ₹{rate}\nToday's high so far.")
        state["high_notified"] = True

    if new_low and not state["low_notified"]:
        messages.append(f"📉 *EUR/INR Daily Low!*\nRate: ₹{rate}\nToday's low so far.")
        state["low_notified"] = True

    diff = rate - state["last_notified_rate"]
    if abs(diff) >= THRESHOLD:
        direction = "risen ⬆️" if diff > 0 else "fallen ⬇️"
        messages.append(
            f"💱 *EUR/INR Alert*\n"
            f"Rate has {direction} by {abs(diff):.2f}\n"
            f"Now: ₹{rate}  |  Was: ₹{state['last_notified_rate']}"
        )
        state["last_notified_rate"] = rate

    for msg in messages:
        send_whatsapp(msg)

    save_state(state)
    print(f"Checked. Rate: {rate} | High: {state['day_high']} | Low: {state['day_low']}")

if __name__ == "__main__":
    print("DEBUG → SID exists:", bool(TWILIO_SID))
    main()
