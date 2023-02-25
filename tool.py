from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Load the CSV file with the non-inclusive words and their inclusive alternatives
def load_word_list():
    with open('dictionary.csv', newline='', encoding='utf-8') as csvfile:
        word_list = list(csv.DictReader(csvfile))
    return word_list

# Check the input text for non-inclusive words and return a list of recommendations
def check_text(input_text, word_list):
    recommendations = []
    for word in word_list:
        if word['word'].lower() in input_text.lower():
            recommendations.append(word)
    return recommendations

# Render the main page with the form
@app.route('/')
def index():
    return render_template('index.html')

# Process the form submission and display the results
@app.route('/', methods=['POST'])
def check_text_submit():
    input_text = request.form['text']
    word_list = load_word_list()
    recommendations = check_text(input_text, word_list)
    return render_template('results.html', recommendations=recommendations, input_text=input_text)

if __name__ == '__main__':
    app.run(debug=True)


#Reference list
