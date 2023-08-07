#!/usr/bin/env python
# coding: utf-8

# In[9]:

import pandas as pd
import nltk
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob


# In[ ]:


# Configuração inicial
BASE_URL = 'https://www.amazon.com.br/Echo-Dot-3%C2%AA-Gera%C3%A7%C3%A3o-Cor-Preta/product-reviews/B07PDHSJ1H/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews'
LIMIT = 200
MAX_PAGES = 20  # Número de páginas a serem raspadas

# Inicializar o webdriver (neste exemplo, estou usando o Chrome)
# Certifique-se de ter o chromedriver instalado e configurado corretamente
driver = webdriver.Chrome()

all_reviews = []

for page_number in range(1, MAX_PAGES + 1):
    driver.get(f"{BASE_URL}&pageNumber={page_number}")
    time.sleep(5)  # Aumentar o tempo de espera para garantir que a página carregue completamente

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Ajuste no processo de extração dos títulos
    letter_space_elements = soup.select('span.a-letter-space')
    titles = [elem.next_sibling.string if elem.next_sibling else "" for elem in letter_space_elements]
    
    contents = [content_tag.text.strip() for content_tag in soup.select('span[data-hook="review-body"]')]

    current_reviews = list(zip(titles, contents))
    
    # Verificar se coletamos avaliações na página atual
    if not current_reviews:
        print(f"No reviews found on page {page_number}. Exiting loop.")
        break

    all_reviews.extend(current_reviews)
    print(f"Collected {len(current_reviews)} reviews from page {page_number}. Total reviews: {len(all_reviews)}")

    # Se já coletamos o número desejado de avaliações, podemos sair do loop
    if len(all_reviews) >= LIMIT:
        break

driver.quit()

# Transformar as avaliações em um DataFrame
df_reviews = pd.DataFrame(all_reviews, columns=['Title', 'Content'])
print(f"Total reviews collected: {df_reviews.shape[0]}")


# In[20]:


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to preprocess the text data
def preprocess_text(text):
    # Convert the text to lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('portuguese'))
    words = [word for word in words if word not in stop_words]

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    return ' '.join(words)

# Preprocess the 'Title' and 'Content' columns
data['Title'] = data['Title'].apply(preprocess_text)
data['Content'] = data['Content'].apply(preprocess_text)

# Display the first few rows of the preprocessed data
data.head()


# In[21]:


# Load the data
data = pd.read_csv('avalicao_produto.csv')

# Display the first few rows of the data
data.head()


# In[22]:


# Combine the 'Title' and 'Content' columns into a single 'text' column
data['text'] = data['Title'] + ' ' + data['Content']

# Create a vectorizer
vectorizer = CountVectorizer()

# Vectorize the text data
X = vectorizer.fit_transform(data['text'])


# In[23]:


# Function to get the sentiment
def get_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Get the sentiment polarity
    polarity = blob.sentiment.polarity

    # Return the sentiment
    if polarity > 0:
        return 'positivo'
    elif polarity < 0:
        return 'negativo'
    else:
        return 'neutro'

# Get the sentiment for each review
data['sentiment'] = data['text'].apply(get_sentiment)


# In[24]:


data.head()


# In[25]:


data['sentiment'].value_counts()


# In[ ]:




