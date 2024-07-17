import pycurl   
from io import BytesIO
from textblob import TextBlob

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://newsapi.org/v2/top-headlines?country=us&pageSize=3&apiKey=2b8807019e5941a6941a4eb479020613')
c.setopt(c.WRITEDATA, buffer)

# Add User-Agent header
c.setopt(c.HTTPHEADER, ['User-Agent: GaiaBot/1.0'])

c.perform()
c.close()

body = buffer.getvalue()
data = (body.decode('utf-8'))

# Convert the JSON response to a dictionary
import json
response_json = json.loads(data)
alist= []
# Print only the titles of the articles
if response_json.get("status") == "ok" and response_json.get("articles"):
    articles = response_json.get("articles")
    print("Here are some recent news article titles:\n")
    for article in articles:
        title = article.get("title")
        alist.append((f"- {title}"))
else:
    print("Sorry, I couldn't fetch any news articles right now.")


import nltk
nltk.download('punkt')  # Download necessary data
from nltk.tokenize import word_tokenize

for title in alist: 
    text = str(title)
    words = word_tokenize(text)
    print(words)

    # Text to analyze

    blob = TextBlob(text)
    sentiment = blob.sentiment
    print("TextBlob Sentiment:", sentiment)
 
    # Determine if the sentence is happy or sad
    if sentiment.polarity > 0:
        print("The sentence is happy.")
    elif sentiment.polarity < 0:
        print("The sentence is sad.")
    else:
        print("The sentiment of the sentence is neutral or unclear.")