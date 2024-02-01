import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import string

input_folder = 'PreprocessData'

output_folder = 'Sentiment'

with open('positive.txt', 'r', encoding='utf-8') as file:
    positive_words = set(file.read().split())

with open('negative.txt', 'r', encoding='utf-8') as file:
    negative_words = set(file.read().split())

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

sid = SentimentIntensityAnalyzer()

def analyze_sentiment_and_save(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    words = word_tokenize(text)

    positive_score = sum(1 for word in words if word.lower() in positive_words)
    negative_score = sum(1 for word in words if word.lower() in negative_words)

    sentiment_scores = sid.polarity_scores(text)
    polarity_score = sentiment_scores['compound']

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(f'Positive Score: {positive_score}\n')
        file.write(f'Negative Score: {negative_score}\n')
        file.write(f'Polarity Score: {polarity_score}\n')

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename.replace(".txt", "_sentiment.txt"))

        analyze_sentiment_and_save(input_file_path, output_file_path)

print("Complete")
