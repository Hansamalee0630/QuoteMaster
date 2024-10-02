from flask import Flask, render_template, request, redirect, url_for, session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import time

app = Flask(__name__)
app.secret_key = '1234'  # Needed for session management

# Sample quotes
quotes = [
    "Dream big and work hard",
    "Love deeply and worry less",
    "Stay positive and stay focused"
]

def quote_master_game(user_quote):
    # Retrieve game state from session
    computer_quote = session.get('computer_quote')
    remaining_time = session.get('remaining_time')
    start_time = session.get('start_time')

    # Measure elapsed time
    elapsed_time = time.time() - start_time

    # Check if the user took too long
    if elapsed_time > remaining_time:
        return {
            "result": "lose",
            "message": f"Time's up! You took over 15 seconds. You lose! ☠️",
            "computer_quote": computer_quote,
            "similarity": 0,
            "remaining_time": 0
        }

    # Calculate similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([computer_quote, user_quote])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # Determine if user wins
    if similarity > 0.5:
        return {
            "result": "win",
            "message": f"Congratulations! You win. 😎✨\nSimilarity score: {similarity:.2f}",
            "computer_quote": computer_quote,
            "similarity": similarity,
            "remaining_time": remaining_time
        }
    else:
        remaining_time -= elapsed_time
        if remaining_time <= 0:
            return {
                "result": "lose",
                "message": f"No more time left. You lose! 😭\nSimilarity score: {similarity:.2f}",
                "computer_quote": computer_quote,
                "similarity": similarity,
                "remaining_time": 0
            }
        else:
            # Update session with new remaining time
            session['remaining_time'] = remaining_time
            return {
                "result": "continue",
                "message": f"Sorry, not similar enough. 😔\nSimilarity score: {similarity:.2f}\nRemaining time: {remaining_time:.2f} seconds\nKeep working...",
                "computer_quote": computer_quote,
                "similarity": similarity,
                "remaining_time": remaining_time
            }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    if request.method == 'POST':
        user_quote = request.form['quote']
        result = quote_master_game(user_quote)
        if result['result'] == 'continue':
            return render_template('quote.html', quote=session['computer_quote'], remaining_time=result['remaining_time'], message=result['message'])
        else:
            return render_template('result.html', result=result)

    # Initialize game state for a new game
    computer_quote = random.choice(quotes)
    session['computer_quote'] = computer_quote
    session['remaining_time'] = 15  # Reset time for each round
    session['start_time'] = time.time()

    return render_template('quote.html', quote=computer_quote, remaining_time=15)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        new_quote = request.form['quote']
        quotes.append(new_quote)
        return redirect(url_for('quote'))
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)