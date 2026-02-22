from flask import Flask, render_template, request, session
import random
import os
app = Flask(__name__)
app.secret_key = "secret_key_123"

words = {
    "easy": [
        "cat", "dog", "sun", "hat", "bat", "pen", "cup", "book", "fish", "tree",
        "milk", "ball", "star", "moon", "duck", "frog", "ship", "car", "ring", "cake",
        "bird", "leaf", "wind", "rain", "snow", "sand", "rock", "lamp", "door", "hand",
        "foot", "nose", "eye", "ear", "bed", "box", "toy", "key", "map", "road",
        "hill", "farm", "king", "lion", "wolf", "bear", "ant", "bee", "cow", "pig", "soap", "comb", "towel", "plate", "fork", "spoon", "rice", "salt", "tea", "juice",
        "shirt", "jeans", "belt", "cap", "bag", "bus", "bike", "road", "park", "shop",
        "bank", "card", "cash", "bill", "gift", "game", "song", "film", "photo", "clock",
        "watch", "chair", "desk", "floor", "wall", "roof", "fan", "light", "match", "stick",
        "glass", "bowl", "brush", "paste", "cream", "oil", "pan", "pot", "tap", "mug"
    ],
    
    "medium": [
        "apple", "house", "green", "water", "river", "chair", "table", "plant", "bread", "light",
        "phone", "clock", "cloud", "smile", "laugh", "dream", "train", "plane", "brush", "glass",
        "sweet", "salad", "grape", "stone", "beach", "ocean", "horse", "sheep", "tiger", "zebra",
        "panda", "eagle", "shark", "whale", "snake", "spoon", "plate", "candy", "sugar", "spice",
        "shirt", "pants", "shoes", "socks", "jacket", "pillow", "blanket", "window", "garden", "forest", 
        "kitchen", "bedroom", "bathroom", "office", "school", "market", "hospital", "garden", "street", "station",
        "ticket", "wallet", "pocket", "laptop", "mobile", "charger", "remote", "battery", "screen", "speaker",
        "breakfast", "lunch", "dinner", "coffee", "butter", "cheese", "vegetable", "chicken", "bottle", "basket",
        "mirror", "curtain", "pillow", "blanket", "helmet", "traffic", "signal", "engine", "petrol", "driver",
        "teacher", "student", "doctor", "farmer", "worker", "manager", "meeting", "holiday", "travel", "weather"
    ],
    
    "hard": [
        "python", "flask", "hangman", "computer", "program", "library", "science", "network", "database", "function",
        "variable", "integer", "boolean", "compile", "execute", "package", "project", "machine", "learning", "artificial",
        "intelligence", "algorithm", "developer", "software", "hardware", "internet", "security", "encryption", "protocol", "analysis",
        "framework", "application", "interface", "iteration", "recursion", "optimization", "architecture", "repository", "deployment", "automation",
        "configuration", "integration", "virtualization", "containerization", "microservice", "scalability", "performance", "debugging", "scripting", "synchronization",
        "electricity", "refrigerator", "microwave", "television", "apartment", "maintenance", "transportation", "communication", "reservation", "appointment",
        "supermarket", "restaurant", "delivery", "groceries", "laundry", "cleaning", "furniture", "decoration", "equipment", "technology",
        "transaction", "investment", "insurance", "subscription", "registration", "identification", "documentation", "application", "verification", "notification",
        "organization", "management", "responsibility", "productivity", "schedule", "commitment", "preparation", "celebration", "invitation", "conversation",
        "environment", "recycling", "sustainability", "nutrition", "exercise", "meditation", "communication", "coordination", "transport", "accommodation"
    ]
}

HANGMAN = [
"""
  |
  |
  |
  |
=====""",
"""
  +---+
  |
  |
  |
=====""",
"""
  +---+
  |   O
  |
  |
=====""",
"""
  +---+
  |   O
  |   |
  |
=====""",
"""
  +---+
  |   O
  |  /|
  |
=====""",
"""
  +---+
  |   O
  |  /|\\
  |
=====""",
"""
  +---+
  |   O
  |  /|\\
  |  / \\
====="""
]

@app.route("/", methods=["GET", "POST"])
def index():

    if "score" not in session:
        session["score"] = 0

    message = ""

    word = session.get("word")
    guessed = session.get("guessed", [])
    wrong = session.get("wrong", 0)

    if request.method == "POST":

        # Start new game
        if request.form.get("difficulty"):
            difficulty = request.form.get("difficulty")
            word = random.choice(words[difficulty])
            session["word"] = word
            session["guessed"] = []
            session["wrong"] = 0
            guessed = []
            wrong = 0
            message = ""

        # Guess letter
        elif request.form.get("letter") and word:
            letter = request.form.get("letter").lower()

            if wrong < 6 and not all(l in guessed for l in word):

                if letter.isalpha() and len(letter) == 1:
                    if letter not in guessed:
                        guessed.append(letter)
                        session["guessed"] = guessed

                        if letter not in word:
                            session["wrong"] += 1
                            wrong = session["wrong"]

            # Check Win
            if all(l in guessed for l in word):
                session["score"] += 1
                message = "win"

            # Check Lose
            if wrong >= 6:
                message = "lose"

    wrong = min(wrong, len(HANGMAN) - 1)

    return render_template(
        "index.html",
        word=word,
        guessed=guessed,
        wrong=wrong,
        hangman=HANGMAN[wrong],
        score=session["score"],
        message=message
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)