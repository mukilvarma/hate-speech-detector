from flask import Flask, render_template, jsonify
from twilio.rest import Client
import tweepy
import openai
import datetime
import os

app = Flask(__name__, template_folder='templates')

# Twitter API credentials
twitter_api_key = 'K8kVGLXC6d7k5Bt3NjpYjgslz'
twitter_api_secret_key = 'fdutQREjZ3KmYqOZnuqxpWgSboCB7dS8QOYVtiSOyFrOU2mm6d'
twitter_access_token = '1636302414621081600-nDHF1XlocFSahEuDFGcuAoVf4yBVR9'
twitter_access_token_secret = 'EwM3VSsDNgwAWfeRlKQRLz5seIn7QxNzXfkbdkCyEbjPO'
twitter_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAJZHugEAAAAAB21rrrHdZvWQVLSAf%2FNZBeM2rCA%3DoHLHcjRlEzmB3wcAhgtuijk5Kk4smwNJ1kL2vVgbEvMBG4Otnd'

# OpenAI API key
openai.api_key = 'sk-news-service-NLlhQ6ULVybEEZ7Nj8EuT3BlbkFJZsvRJci1foO7h0GSy3jU'

# Twilio WhatsApp API credentials
twilio_account_sid = 'AC752abd12c5fba74faadfa64ca3f77280'
twilio_auth_token = '23896645104b71a950531e787ddb2e6d'
twilio_phone_number = '+15626625358'
whatsapp_numbers = ['whatsapp:+916381603325','whatsapp:+919790138555']  # List of recipient WhatsApp numbers

# Initialize Twilio client
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Initialize Tweepy client
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(auth, wait_on_rate_limit=True)

client = openai.OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai.api_key
)

def fetch_twitter_posts():
    # Simulated static data including hate speeches
    tweets = [
        "I hate Mondays, they are the worst!",
        "Can't stand people who spread hate.",
        "Such hatred in the world makes me sad.",
        "Why can't we all just get along?",
        "I strongly dislike when people judge others unfairly.",
        "I think all members of a certain group are inferior and should be treated differently.",
        "We should eliminate people who don't belong to our community.",
        "The world would be better off without certain types of people."
    ]
    return tweets

##def fetch_twitter_posts(keyword):
##    posts = []
##    since_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
##    for tweet in tweepy.Cursor(twitter_api.search_tweets, q=keyword, lang="en", since=since_date).items(100):
##        posts.append(tweet.text)
##    return posts

def analyze_posts(posts):
    hatred_posts = []
    for post in posts:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access to GPT-4
            messages=[
                {"role": "system", "content": "You are a content moderator."},
                {"role": "user", "content": f"Is the following post hate speech? {post}"}
            ],
            max_tokens=10
        )

        # Check if response indicates hate speech
        if 'yes' in response.choices[0].message.content.lower():
            hatred_posts.append(post)
    print("hatred_posts")
    print(hatred_posts)
    return hatred_posts

def send_whatsapp_alerts(messages):
    whatsapp_logs = []
    for message in messages:
        for number in whatsapp_numbers:
            whatsapp_logs.append(f"Printing WhatsApp message to {number}: {message}")
            ##try:
            ##    twilio_client.messages.create(
            ##        body=message,
            ##        from_='whatsapp:' + twilio_phone_number,  # Ensure this is in WhatsApp format
            ##        to=number,
            ##    )
            ##    print(f"Sent WhatsApp message to {number}: {message}")
            ##except Exception as e:
            ##    print(f"Error sending WhatsApp message to {number}: {e}")


@app.route('/fetch-hatred-posts', methods=['GET'])
def fetch_hatred_posts():
    twitter_posts = fetch_twitter_posts()
    all_posts = twitter_posts
    hatred_posts = analyze_posts(all_posts)
    ##whatsapp_logs2 = send_whatsapp_alerts(hatred_posts)
    return jsonify(hatred_posts)

@app.route('/')
def index():
    template_path = os.path.join(app.template_folder, 'index.html')
    print(f"Template path: {template_path}")
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

