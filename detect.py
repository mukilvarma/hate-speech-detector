import tweepy
import facebook
import openai
from datetime import datetime, timedelta
import schedule
import time
import requests

# Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Facebook access token
fb_access_token = 'YOUR_FB_ACCESS_TOKEN'

# OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# WhatsApp API credentials (example using Twilio WhatsApp API)
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_WHATSAPP_NUMBER = 'YOUR_TWILIO_WHATSAPP_NUMBER'
WHATSAPP_NUMBERS = ['whatsapp:+15551234567', 'whatsapp:+15552345678']  # List of recipient WhatsApp numbers

# Set up tweepy authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

# Set up Facebook Graph API
fb_graph = facebook.GraphAPI(fb_access_token)

# List of keywords (initially empty)
keywords = []

def detect_hate_speech(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that identifies hate speech."},
            {"role": "user", "content": f"Does the following text contain hate speech? Answer 'Yes' or 'No'.\n\n{text}"}
        ]
    )
    return response.choices[0].message['content'].strip()

def search_social_media(keyword, tweet_count=10, fb_page_id=None, fb_limit=10):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    # Search Twitter
    tweets = twitter_api.search(q=keyword, count=tweet_count, tweet_mode='extended', since=thirty_days_ago.strftime('%Y-%m-%d'))
    tweet_links = []
    for tweet in tweets:
        text = tweet.full_text
        if detect_hate_speech(text) == 'Yes':
            tweet_links.append(f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}")
    
    # Search Facebook
    fb_links = []
    if fb_page_id:
        posts = fb_graph.get_connections(id=fb_page_id, connection_name='posts', limit=fb_limit)
        for post in posts['data']:
            if 'message' in post:
                post_date = datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z')
                if post_date >= thirty_days_ago:
                    text = post['message']
                    if detect_hate_speech(text) == 'Yes':
                        fb_links.append(f"https://www.facebook.com/{fb_page_id}/posts/{post['id']}")

    # Prepare and send WhatsApp messages
    message = f"Hate Speech Detected for keyword '{keyword}':\n"
    if tweet_links:
        message += "\nTwitter:\n" + "\n".join(tweet_links)
    if fb_links:
        message += "\nFacebook:\n" + "\n".join(fb_links)

    for number in WHATSAPP_NUMBERS:
        send_whatsapp_message(number, message)

def send_whatsapp_message(number, message):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    data = {
        'From': TWILIO_WHATSAPP_NUMBER,
        'Body': message,
        'To': number
    }
    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    response = requests.post(url, data=data, auth=auth)
    print(f"Message sent to {number}: {response.status_code}")

def schedule_daily_search():
    for keyword in keywords:
        schedule.every().day.at("06:00").do(search_social_media, keyword=keyword)

def manual_search(keyword):
    search_social_media(keyword)

# Example usage of manual search
# manual_search('example_keyword')

# Example usage of scheduling daily search
# keywords.append('example_keyword')
# schedule_daily_search()

# Example Flask application for keyword management and manual search
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', keywords=keywords)

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    keyword = request.form['keyword']
    keywords.append(keyword)
    schedule_daily_search()
    return render_template('index.html', keywords=keywords)

@app.route('/search_now/<keyword>', methods=['GET'])
def search_now(keyword):
    manual_search(keyword)
    return 'Search initiated. Check WhatsApp for results.'

if __name__ == '__main__':
    app.run(debug=True)
