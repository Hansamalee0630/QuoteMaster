# Quote Master Game 📝✨

Welcome to the **Quote Master** game, a Flask-based web application where players must match their quotes with randomly selected quotes from the computer. The goal is to provide a quote that is **similar enough** (based on cosine similarity) to win the game!

## Features
- **Timer-based Challenge**: Players must input their quotes within 15 seconds.
- **Cosine Similarity Matching**: Your quote is compared against the computer’s quote using **TF-IDF** and **cosine similarity**.
- **Multiple Rounds**: If you’re not similar enough and still have time left, you get a chance to try again.

## Game Rules
1. A random quote is selected by the computer.
2. You must type a quote that is similar enough to the computer's quote (cosine similarity > 0.5).
3. You have only 15 seconds to submit your quote!
4. If your quote is not similar enough but you still have time, you get to try again until time runs out.
