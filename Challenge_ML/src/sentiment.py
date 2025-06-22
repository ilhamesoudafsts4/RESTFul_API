from textblob import TextBlob

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    sentiment = "positive" if polarity >= 0 else "negative"
    return polarity, sentiment
