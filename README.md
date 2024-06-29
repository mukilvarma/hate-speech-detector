# Detecting and Alerting Hate Speech in Twitter Using AI

This project is a Hate Speech Detector that uses OpenAI's language model to analyze posts fetched from Twitter. Detected hate speech messages are then sent as alerts via WhatsApp.

## Requirements

To run this project locally, you need:

- Python 3.x
- Flask
- Tweepy
- OpenAI API Key
- Twilio API credentials (for WhatsApp alerts)

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd hate-speech-detector

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt


3. **Set up your environment variables:**

   Create a `.env` file in the root directory and add the following:

   ```plaintext
   OPENAI_API_KEY=<your-openai-api-key>
   TWILIO_ACCOUNT_SID=<your-twilio-account-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
   TWILIO_PHONE_NUMBER=<your-twilio-phone-number>
   WHATSAPP_NUMBERS=<comma-separated-list-of-whatsapp-numbers>

4. **Run the application:**

   ```bash
   python detect.py

   Open your web browser and navigate to `http://localhost:5000`.

## Using the Hate Speech Detector

1. **Fetch Hatred Posts:**
   
   - Click on the "Fetch Hatred Posts" button to simulate fetching and analyzing hate speech posts from Twitter.

2. **View Results:**
   
   - Detected hate speech messages will be displayed on the screen and logged in the console.

## Notes

- **Twitter API**: The project uses mock data due to the lack of a live Twitter API subscription. To fetch real-time Twitter posts, a Twitter API subscription is required. Uncomment and integrate the Twitter API code in `app.py` for live results.
  
- **WhatsApp Alerts**: WhatsApp alerts are simulated using Twilio's API with mock data. To enable real WhatsApp alerts, a Twilio account with WhatsApp API capabilities is needed. Uncomment and integrate the Twilio WhatsApp code in `app.py` for live alerts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
