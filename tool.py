from flask import Flask, render_template, request, jsonify
import csv

#state this is the app
app = Flask(__name__)

import csv

data = []


# Load the data from the CSV file
with open('dictionary.csv', 'r') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        data.append(row)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def check_text():
    # Get the user input from the form
    text = request.form['text']

    # Split the text into words
    words = text.split()

    # Initialize a list to store any offensive words
    offensive_words = []

    # Loop through each word in the text
    for word in words:
        # Check if the word is in the dictionary
        for item in data:
            if word.lower() == item['Word'].lower():
                # If the word is in the dictionary, add it to the list of offensive words
                offensive_words.append(word)

    # Initialize a list to store the suggested replacements
    replacements = []

    # Loop through each offensive word
    for word in offensive_words:
        # Find the corresponding entry in the dictionary
        for item in data:
            if word.lower() == item['Word'].lower():
                # If an alternative word is available, add it to the list of replacements
                if item['Alt word']:
                    replacements.append(item['Alt word'])
                # Otherwise, use the original word as the replacement
                else:
                    replacements.append(word)

    # Render the results page with the offensive words and suggested replacements
    return render_template('results.html', text=text, offensive_words=offensive_words, replacements=replacements)

if __name__ == '__main__':
    app.run(debug=True)
