from flask import Flask, render_template, request, jsonify
from airtable import Airtable

#state this is the app
app = Flask(__name__)

# Your Airtable API key and base ID
AIRTABLE_API_KEY = 'patwLoFtU6uCVQLbr.f21c5c8ee50b4462d3546257f605e31d0f81abab9420a7e15a9f1129f257b38e'
AIRTABLE_BASE_ID = 'appS6ep3oZKd27r1U'

# Create an Airtable object to interact with your base
airtable = Airtable(AIRTABLE_BASE_ID, 'WordList', api_key=AIRTABLE_API_KEY)

# Your homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Your form submission route
@app.route('/check', methods=['POST'])
def check_text():
    # Get the user's input text from the form
    text = request.form['text']

    # Split the text into a list of words
    words = text.split()

    # Look up each word in your Airtable base and check if it's offensive
    offensive_words = []
    for word in words:
        if airtable.search('Word', word):
            offensive_words.append(word)

    # If no offensive words are found, return a success message
    if not offensive_words:
        response = {
            'status': 'success',
            'message': 'Your text contains no offensive words!'
        }
    # If offensive words are found, return a list of suggestions
    else:
        suggestions = []
        for word in offensive_words:
            record = airtable.search('Word', word)[0]
            suggestions.append(record['fields'].get('Suggestion', ''))
        response = {
            'status': 'warning',
            'message': 'Your text contains offensive words. Here are some suggestions:',
            'offensive_words': offensive_words,
            'suggestions': suggestions
        }

    # Return the response as a JSON object
    return jsonify(response)
