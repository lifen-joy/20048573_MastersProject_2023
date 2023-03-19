from flask import Flask, render_template, request
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


app = Flask(__name__)

#Step 1
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
gendered_pronouns = {'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself'}
stop_words = stop_words.difference(gendered_pronouns)
   
def clean_text(text):
    
    cleaned_text = re.sub(r"[^a-zA-Z'\s]", " ", text)
    cleaned_text = cleaned_text.lower()
    cleaned_text = re.sub(r"\b\d{5,}\b", "", cleaned_text)
    cleaned_text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*'(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", "", cleaned_text)
    cleaned_text = cleaned_text.replace("\n", " ")
    cleaned_text = re.sub(r"'s", "", cleaned_text)
    words = cleaned_text.split()
    words = [word for word in words if word not in stop_words]
    cleaned_text = ' '.join(words)

    return cleaned_text

#Step 2
def tokenize_text(cleaned_text):
    return word_tokenize(cleaned_text)

#Step 3
def stem_words(cleaned_text):
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in cleaned_text]
    return cleaned_text



#step 4
masculine_words = ['active', 'adventurous', 'aggress', 'ambitio', 'analy', 'assert', 'athlet', 'autonom', 'battle', 'boast', 'challeng', 'champion', 'compet', 'confident', 'courag', 'decid', 'decision', 'decisive', 'defend', 'determin', 'domina', 'dominant', 'driven', 'fearless', 'fight', 'force', 'greedy', 'head-strong', 'headstrong', 'hierarch', 'hostil', 'impulsive', 'independen', 'individual', 'intellect', 'lead', 'logic', 'objective', 'opinion', 'outspoken', 'persist', 'principle', 'reckless', 'self-confiden', 'self-relian', 'self-sufficien', 'selfconfiden', 'selfrelian', 'selfsufficien', 'stubborn', 'superior', 'unreasonab', 'Actor', 'Bogeyman', 'Boogeyman', 'Businessman', 'Businessmen', 'Chairman', 'Congressman', 'Fireman', 'Guys', 'Housekeeping', 'Mailman', 'Man hours', 'Man made', 'Man up', 'Mankind', 'Manpower', 'Mastered', 'Mastering', 'Old geezer', 'Policeman', 'Postman', 'Steward', 'The common man', 'gentlemen', 'male', 'man', 'master']
feminine_words = ['affectionate', 'agree', 'cheer', 'child', 'co-operat', 'collab', 'commit', 'communal', 'compassion', 'connect', 'considerate', 'cooperat', 'depend', 'emotiona', 'empath', 'enthusias', 'feel', 'flatterable', 'gentle', 'honest', 'inclusive', 'inter-dependen', 'inter-persona', 'inter-personal', 'interdependen', 'interpersona', 'interpersonal', 'kind', 'kinship', 'loyal', 'modesty', 'nag', 'nurtur', 'pleasant', 'polite', 'quiet', 'respon', 'sensitiv', 'share', 'sharin', 'submissive', 'support', 'sympath', 'tender', 'together', 'trust', 'understand', 'warm', 'whin', 'yield', 'Actress', 'Crone', 'Female', 'Gals', 'Girl', 'Girls', 'Hag', 'Ladies', 'Ladies room', 'Lady', 'Lady time', 'Ladylike', 'Prostitute', 'Skank', 'Skanky', 'Slut', 'Stewardess', 'Stewardesses', 'Tramp', 'Whore', 'sirmadam']

stemmer = PorterStemmer()
masculine_pronouns = [stemmer.stem(word) for word in ['he', 'him', 'his', 'himself', 'man', 'men', 'male', 'father', 'brother', 'son', 'uncle', 'grandfather', 'nephew', 'husband', 'boyfriend', 'groom', 'king', 'prince', 'emperor', 'sir', 'lord']]
feminine_pronouns = [stemmer.stem(word) for word in ['she', 'her', 'hers', 'herself', 'woman', 'women', 'female', 'mother', 'sister', 'daughter', 'aunt', 'grandmother', 'niece', 'wife', 'girlfriend', 'bride', 'queen', 'princess', 'empress', 'lady', 'madam']]

def find_gendered_words(tokens, word_list):
    return [token for token in tokens if token in word_list]


def analyze_gendered_words(cleaned_text):
    tokens = tokenize_text(cleaned_text)
    stemmed_tokens = stem_words(tokens)
    
    fem_words = find_gendered_words(stemmed_tokens, feminine_words)
    masc_words = find_gendered_words(stemmed_tokens, masculine_words)
    fempro_words = find_gendered_words(stemmed_tokens, feminine_pronouns)
    maspro_words = find_gendered_words(stemmed_tokens, masculine_pronouns)

    return {
        'feminine_words_count': len(fem_words),
        'masculine_words_count': len(masc_words),
        'feminine_pronouns_count': len(fempro_words),
        'masculine_pronouns_count': len(maspro_words),
        'feminine_pronouns': fempro_words,
        'masculine_pronouns': maspro_words,
        'feminine_words': fem_words,
        'masculine_words': masc_words,
    }

#step 5  

def label_gender(cleaned_text):
    tokens = tokenize_text(cleaned_text)
    stemmed_tokens = stem_words(tokens)

    fem_words = find_gendered_words(stemmed_tokens, feminine_words)
    masc_words = find_gendered_words(stemmed_tokens, masculine_words)
    fem_pronouns = find_gendered_words(stemmed_tokens, feminine_pronouns)
    masc_pronouns = find_gendered_words(stemmed_tokens, masculine_pronouns)

    fem_total = len(fem_pronouns) * 2 + len(fem_words)
    masc_total = len(masc_pronouns) * 2 + len(masc_words)

    if fem_total == 0 and masc_total == 0:
        return 'Neutral'
    elif fem_total > masc_total:
        return 'Feminine'
    else:
        return 'Masculine'

#Step 6

def process_input_text(input_text):
    cleaned_text = clean_text(input_text)
    tokenized_text = tokenize_text(cleaned_text)
    stemmed_text = stem_words(tokenized_text)
    analysis_results = analyze_gendered_words(stemmed_text)

    return analysis_results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        analysis_results = process_input_text(input_text)
        gender_label = label_gender(input_text)
        processed_text = analysis_results['cleaned_text']
        return render_template('index.html', input_text=input_text, processed_text=processed_text, gender_label=gender_label, analysis_results=analysis_results)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
