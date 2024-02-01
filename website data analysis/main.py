import os
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import string
from textstat import flesch_kincaid_grade, syllable_count

input_folder = 'PreprocessData'

with open('MasterDictionary/positive-words.txt', 'r', encoding='utf-8') as file:
    positive_words = set(file.read().split())

with open('MasterDictionary/negative-words.txt', 'r', encoding='utf-8') as file:
    negative_words = set(file.read().split())

input_df = pd.read_excel('input.xlsx')

columns = ['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
           'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
           'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
           'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']

result_df = pd.DataFrame(columns=columns)

sid = SentimentIntensityAnalyzer()

def analyze_and_append(input_file_path, url_id, url):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    words = word_tokenize(text)
    print(words)
    positive_score = sum(1 for word in words if word.lower() in positive_words)
    negative_score = sum(1 for word in words if word.lower() in negative_words)

    sentiment_scores = sid.polarity_scores(text)
    polarity_score = sentiment_scores['compound']

    sentences = nltk.sent_tokenize(text)
    total_words = len(words)
    total_syllables = sum(syllable_count(word) for word in words)
    avg_sentence_length = total_words / len(sentences) if len(sentences) != 0 else 0
    percentage_complex_words = (sum(1 for word in words if syllable_count(word) > 2) / total_words) * 100 if total_words != 0 else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = total_words / len(sentences) if len(sentences) != 0 else 0
    complex_word_count = sum(1 for word in words if syllable_count(word) > 2)
    syllable_per_word = total_syllables / total_words if total_words != 0 else 0
    personal_pronouns = sum(1 for word in words if word.lower() in ['i', 'we', 'my', 'ours', 'us'])
    avg_word_length = sum(len(word) for word in words) / total_words if total_words != 0 else 0

    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)

    result_df.loc[len(result_df)] = [url_id, url, positive_score, negative_score, polarity_score,subjectivity_score,
                                     avg_sentence_length, percentage_complex_words, fog_index,
                                     avg_words_per_sentence, complex_word_count, total_words,
                                     syllable_per_word, personal_pronouns, avg_word_length,
                                     ]

for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    filename = f'{url_id}.txt'
    input_file_path = os.path.join(input_folder, filename)

    analyze_and_append(input_file_path, url_id, url)

result_df.to_excel('combined_results.xlsx', index=False)

print("Complete")
