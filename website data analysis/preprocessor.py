import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

input_folder = 'ScrapData'
output_folder = 'PreprocessData'

with open('StopWords/stopwords.txt', 'r', encoding='utf-8') as file:
    custom_stopwords = set(file.read().split())

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def clean_and_save(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in custom_stopwords]

    cleaned_text = ' '.join(filtered_words)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)

        clean_and_save(input_file_path, output_file_path)

print("Complete")
