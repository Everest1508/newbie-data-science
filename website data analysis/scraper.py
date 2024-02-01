import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.read_excel('Input.xlsx')

def extract_article_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        title_element = soup.find('h1', class_='entry-title')
        title = title_element.text.strip() #if title_element else soup.find('h1', class_="tdb-title-text").text.strip()

        article_div = soup.find('div', class_='td-post-content tagdiv-type')
        article_text = article_div.text.strip() #if article_div else soup.find('div', class_="tdb-block-inner td-fix-index").text.strip()
    except:
        title_element = soup.find('h1', class_="tdb-title-text")
        title = title_element.text.strip() if title_element else ""

        article_div = soup.find('div', class_="td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")
        article_text = article_div.text.strip() if article_div else ""
    return title, article_text

for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    title, article_text = extract_article_data(url)

    with open(f'ScrapData/{url_id}.txt', 'w', encoding='utf-8') as file:
        file.write(f'{title}\n')
        file.write(f'{article_text}')

print("Complete")
