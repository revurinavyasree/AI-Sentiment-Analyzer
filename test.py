from textblob import TextBlob

texts = [
    "I am happy",
    "I passed my exam",
    "I hate this",
    "This is amazing"
]

for text in texts:
    blob = TextBlob(text)
    print(text)
    print(blob.sentiment)
    print()