from flask import Flask, request, jsonify
import spacy
from textblob import TextBlob
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

def calculate_word_frequencies(doc):
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in STOP_WORDS and word.text not in punctuation:
            word_frequencies[word.text.lower()] = word_frequencies.get(word.text.lower(), 0) + 1
    
    max_frequency = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency
    
    return word_frequencies

def score_sentences(doc, word_frequencies):
    sentence_scores = {}
    for sent in doc.sents:
        sentence_scores[sent] = sum(word_frequencies.get(word.text.lower(), 0) for word in sent)
    return sentence_scores

def summarize(text):
    doc = nlp(text)
    word_frequencies = calculate_word_frequencies(doc)
    sentence_scores = score_sentences(doc, word_frequencies)
    
    num_points = 5  
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_points]
    
    summary = '\n'.join(f"• {sent.text.strip()}" for sent in top_sentences)
    return summary

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        sentiment = 'Positive'
        percentage = polarity * 100
    elif polarity < 0:
        sentiment = 'Negative'
        percentage = -polarity * 100
    else:
        sentiment = 'Neutral'
        percentage = 0
    return sentiment, percentage

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    text = data['text']
    summary = summarize(text)
    sentiment, percentage = analyze_sentiment(text)
    return jsonify({"summary": summary, "sentiment": sentiment, "percentage": percentage})

if __name__ == '__main__':
    app.run(debug=True)
