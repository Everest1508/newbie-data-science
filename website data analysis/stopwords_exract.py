import os

input_directory = "StopWords"
output_file = "StopWords/stopwords.txt"

for filename in os.listdir(input_directory):
    file_path = os.path.join(input_directory, filename)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as input_file:
            first_words = [line.split()[0].lower() for line in input_file]

        with open(output_file, 'a',encoding="utf-8") as stopwords_file:
            stopwords_file.write('\n'.join(first_words) + '\n')

print("Complete")
