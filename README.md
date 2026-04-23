# EUR-INR-Tracker
Euro to INR automated tracker to send monthly updates
# EUR/INR Rate Tracker

A lightweight Python script that sends you a WhatsApp notification when the euro to INR exchange rate moves by 25 paise, or hits a new daily high or low.

Built for NRIs and anyone who transfers money between Europe and India and wants to catch good rates without checking manually.

---

## What it does

- Sends a WhatsApp alert when EUR/INR rises or falls by 25 paise from the last notified rate
- Notifies you when the rate hits a new daily high or daily low
- Only runs between the 20th and 1st of each month (the typical salary transfer window)
- Runs automatically every hour via GitHub Actions, completely free

---

## How it works

The script fetches the live EUR/INR rate from a free exchange rate API, compares it against the last recorded state, and sends a WhatsApp message via Twilio if any of the alert conditions are met. State is cached between runs using GitHub Actions cache so daily highs and lows persist across hourly checks.

---

## Stack

- Python 3.11
- Twilio WhatsApp API (free sandbox)
- exchangerate-api.com (free tier)
- GitHub Actions (free, runs hourly)

---

## Setup

### 1. Twilio

1. Sign up at twilio.com
2. Go to Messaging > Try it out > Send a WhatsApp message
3. Activate the sandbox by sending the join code from your WhatsApp
4. Note your Account SID and Auth Token from the dashboard

### 2. Fork this repo

Fork this repository to your own GitHub account.

### 3. Add secrets

Go to your repo > Settings > Secrets and variables > Actions and add:

| Secret name   | Value                              |
|---------------|------------------------------------|
| TWILIO_SID    | Your Twilio Account SID            |
| TWILIO_TOKEN  | Your Twilio Auth Token             |
| TO_WHATSAPP   | whatsapp:+91XXXXXXXXXX             |

### 4. Run it

Go to Actions > EUR/INR Tracker > Run workflow to trigger a manual run and confirm your WhatsApp receives the message.

After that it runs automatically every hour.

---

## Configuration

In `tracker.py` you can adjust:

- `THRESHOLD` — default is 0.25 (25 paise). Lower it to test, raise it if you want fewer alerts.
- The `is_active_period()` function controls which days of the month it runs.

---

## Example alerts

```
EUR/INR Daily High!
Rate: 109.91
Today's high so far.

EUR/INR Alert
Rate has risen by 0.30
Now: 110.21  |  Was: 109.91
```

---

## Note on the Twilio sandbox

The free Twilio sandbox only sends messages to numbers that have explicitly joined it. Each person who wants to use this script needs their own Twilio account. This repo is intentionally kept as a self-hosted tool rather than a shared service.

---

## Author

Built by Indu Havaldar. Design Lead, calligraphy artist, and reluctant but effective Python scripter.
