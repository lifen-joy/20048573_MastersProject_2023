


#Cleaning and pre-processing data

# Remove gendered pronouns from the stop words set as this is needed for the testing
gendered_pronouns = {'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself'}
stop_words = stop_words.difference(gendered_pronouns)

#Core imports

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


import nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
#tokenize
from nltk.tokenize import word_tokenize
nltk.download('punkt')
#Stem words 
from nltk.stem.porter import PorterStemmer

#regular expressions 
import re

#most common words
from collections import Counter 

def clean_text(text):
    # Remove special characters, numbers, and quotation marks
    cleaned_text = re.sub(r"[^a-zA-Z'\s]", " ", text)

    # Convert the text to lowercase
    cleaned_text = cleaned_text.lower()

    # Remove phone numbers and prices
    cleaned_text = re.sub(r"\b\d{5,}\b", "", cleaned_text)

    # Remove website URLs
    cleaned_text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*'(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", cleaned_text)

    # Replace newline characters with spaces
    cleaned_text = cleaned_text.replace("\n", " ")

    # Remove 's (apostrophe followed by s)
    cleaned_text = re.sub(r"'s", "", cleaned_text)

    # Remove stopwords while keeping gendered pronouns
    words = cleaned_text.split()
    words = [word for word in words if word not in stop_words]
    cleaned_text = ' '.join(words)

    return cleaned_text


# Tokenize https://www.geeksforgeeks.org/text-preprocessing-in-python-set-1/

def tokenize_text(text):
    return word_tokenize(text)

# Apply the tokenizing function to the clean_copy column
data['clean_copy'] = data['clean_copy'].apply(tokenize_text)

#Stem words 

stemmer = PorterStemmer()

def stem_words(words):
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words

# Apply the stemming function to the clean_copy column
data['clean_copy'] = data['clean_copy'].apply(stem_words)


# Word list from literature and company research  

masculine_words: ['active', 'adventurous', 'aggress', 'ambitio', 'analy', 'assert', 'athlet', 'autonom', 'battle', 'boast', 'challeng', 'champion', 'compet', 'confident', 'courag', 'decid', 'decision', 'decisive', 'defend', 'determin', 'domina', 'dominant', 'driven', 'fearless', 'fight', 'force', 'greedy', 'head-strong', 'headstrong', 'hierarch', 'hostil', 'impulsive', 'independen', 'individual', 'intellect', 'lead', 'logic', 'objective', 'opinion', 'outspoken', 'persist', 'principle', 'reckless', 'self-confiden', 'self-relian', 'self-sufficien', 'selfconfiden', 'selfrelian', 'selfsufficien', 'stubborn', 'superior', 'unreasonab', 'Actor', 'Bogeyman', 'Boogeyman', 'Businessman', 'Businessmen', 'Chairman', 'Congressman', 'Fireman', 'Guys', 'Housekeeping', 'Mailman', 'Man hours', 'Man made', 'Man up', 'Mankind', 'Manpower', 'Mastered', 'Mastering', 'Old geezer', 'Policeman', 'Postman', 'Steward', 'The common man', 'gentlemen', 'male', 'man', 'master']

feminine_words: ['affectionate', 'agree', 'cheer', 'child', 'co-operat', 'collab', 'commit', 'communal', 'compassion', 'connect', 'considerate', 'cooperat', 'depend', 'emotiona', 'empath', 'enthusias', 'feel', 'flatterable', 'gentle', 'honest', 'inclusive', 'inter-dependen', 'inter-persona', 'inter-personal', 'interdependen', 'interpersona', 'interpersonal', 'kind', 'kinship', 'loyal', 'modesty', 'nag', 'nurtur', 'pleasant', 'polite', 'quiet', 'respon', 'sensitiv', 'share', 'sharin', 'submissive', 'support', 'sympath', 'tender', 'together', 'trust', 'understand', 'warm', 'whin', 'yield', 'Actress', 'Crone', 'Female', 'Gals', 'Girl', 'Girls', 'Hag', 'Ladies', 'Ladies room', 'Lady', 'Lady time', 'Ladylike', 'Prostitute', 'Skank', 'Skanky', 'Slut', 'Stewardess', 'Stewardesses', 'Tramp', 'Whore', 'sirmadam']

# Common pronoun used text from spoken language 
masculine_pronouns = ['he', 'him', 'his', 'himself', 'man', 'men', 'male', 'father', 'brother', 'son', 'uncle', 'grandfather', 'nephew', 'husband', 'boyfriend', 'groom', 'king', 'prince', 'emperor', 'sir', 'lord']

feminine_pronouns = ['she', 'her', 'hers', 'herself', 'woman', 'women', 'female', 'mother', 'sister', 'daughter', 'aunt', 'grandmother', 'niece', 'wife', 'girlfriend', 'bride', 'queen', 'princess', 'empress', 'lady', 'madam']

# Checking text for word 

def find_gendered_words(tokens, word_list):
    return [word for word in word_list if word in tokens]


# Function to analyze and display gendered words information in the clean text

def analyze_gendered_words(clean_text, original_text):
    fem_words = find_gendered_words(clean_text, feminine_words)
    masc_words = find_gendered_words(clean_text, masculine_words)
    fempro_words = find_gendered_words(clean_text, feminine_pronouns)
    maspro_words = find_gendered_words(clean_text, masculine_pronouns)

    print('Feminine words in text:', len(fem_words))
    print('Masculine words in text:', len(masc_words))
    print('Pronouns words in text: fem', len(fempro_words), 'male', len(maspro_words))
    print('Pronouns words in text: fem', fempro_words, 'male', maspro_words)
    print('Feminine words found:', fem_words)
    print('Masculine words found:', masc_words)
    print('Original Ad_copy text:')
    print(original_text)

# Checking results 
sample_row = data.sample().iloc[0]
clean_text = sample_row['clean_copy']
original_text = sample_row['Ad_copy']
analyze_gendered_words(clean_text, original_text)


total_fem_words = 0
total_masc_words = 0
total_fem_pronouns = 0
total_masc_pronouns = 0

for tokens in data['clean_copy']:
    fem_words = find_gendered_words(tokens, feminine_words)
    masc_words = find_gendered_words(tokens, masculine_words)
    total_fem_words += len(fem_words)
    total_masc_words += len(masc_words)

for tokens in data['clean_copy']:
    fem_pronouns = find_gendered_words(tokens, feminine_pronouns)
    masc_pronouns = find_gendered_words(tokens, masculine_pronouns)
    total_fem_pronouns += len(fem_pronouns)
    total_masc_pronouns += len(masc_pronouns)


print('Total feminine words in dataset:', total_fem_words)
print('Total masculine words in dataset:', total_masc_words)
print('Total feminine pronouns in dataset:', total_fem_pronouns)
print('Total masculine pronouns in dataset:', total_masc_pronouns)



def label_gender(row):
    fem_words = find_gendered_words(row['clean_copy'], feminine_words)
    masc_words = find_gendered_words(row['clean_copy'], masculine_words)
    fem_pronouns = find_gendered_words(row['clean_copy'], feminine_pronouns)
    masc_pronouns = find_gendered_words(row['clean_copy'], masculine_pronouns)

    fem_total = len(fem_pronouns) * 2 + len(fem_words)
    masc_total = len(masc_pronouns) * 2 + len(masc_words)

    if fem_total == 0 and masc_total == 0:
        return 0
    elif fem_total > masc_total:
        return 1
    else:
        return 2

data['gender_label'] = data.apply(label_gender, axis=1)