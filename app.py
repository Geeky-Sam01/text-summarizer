from flask import Flask, render_template, request
from text_summ2 import generate_summzary

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        if rawtext.strip() == "":
            error_message = 'Please enter some text to summarize.'
            return render_template('index.html', error_message=error_message)
        final_summary, original_text, len_original, len_summary = generate_summzary(rawtext)
        return render_template('summary.html', final_summary=final_summary, original_text=original_text, len_original=len_original, len_summary=len_summary)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
