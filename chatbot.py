from questions_answers import questions_answers
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# Prepare Knowledge Base
# =========================================================

questions = [item["question"] for item in questions_answers]

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

question_vectors = vectorizer.fit_transform(questions)


# =========================================================
# Casual Conversation
# =========================================================

casual_responses = {

    "hi": "Hi! 👋 How can I help you with Python?",

    "hello": "Hello! 👋 Ask me a Python programming question.",

    "hey": "Hey! 🐍 What would you like to learn about Python?",

    "good morning": "Good morning! ☀️ Ready to learn Python?",

    "good afternoon": "Good afternoon! 😊 What Python topic would you like to explore?",

    "good evening": "Good evening! 🌙 Ask me a Python question.",

    "how are you": "I'm doing great! 😊 Ready to help you learn Python.",

    "thanks": "You're welcome! 😊 Keep learning Python!",

    "thank you": "You're welcome! 🐍 Happy learning!",

    "bye": "Goodbye! 👋 Keep practicing Python!",

    "goodbye": "Goodbye! 👋 See you next time!"
}


# =========================================================
# Python Topic Keywords
# =========================================================

python_keywords = [
    "python",
    "variable",
    "data type",
    "datatype",
    "string",
    "integer",
    "float",
    "boolean",
    "list",
    "tuple",
    "set",
    "dictionary",
    "dict",
    "function",
    "lambda",
    "argument",
    "parameter",
    "return",
    "loop",
    "for loop",
    "while loop",
    "if statement",
    "if else",
    "elif",
    "conditional",
    "operator",
    "arithmetic",
    "comparison",
    "logical",
    "class",
    "object",
    "inheritance",
    "encapsulation",
    "polymorphism",
    "oops",
    "oop",
    "exception",
    "error handling",
    "try",
    "except",
    "module",
    "package",
    "file handling",
    "file",
    "numpy",
    "pandas",
    "matplotlib",
    "machine learning",
    "algorithm",
    "recursion",
    "pip",
    "library",
    "import",
    "syntax",
    "indentation",
    "tf-idf",
    "cosine similarity"
]


# =========================================================
# Check Whether Question is Python Related
# =========================================================

def is_python_question(user_question):

    question = user_question.lower().strip()

    for keyword in python_keywords:

        if keyword in question:
            return True

    return False


# =========================================================
# Find Best Answer
# =========================================================

def find_best_answer(user_question):

    user_question = user_question.lower().strip()

    if not user_question:
        return "Please enter a question."


    # =====================================================
    # Casual Conversation Check
    # =====================================================

    if user_question in casual_responses:

        return casual_responses[user_question]


    # =====================================================
    # Python Related Check
    # =====================================================

    if not is_python_question(user_question):

        return (
            "Sorry, I can only answer questions related to "
            "Python programming. 🐍 Please ask me a "
            "Python-related question."
        )


    # =====================================================
    # Normalize Common Plural Forms
    # =====================================================

    replacements = {

        "variables": "variable",
        "functions": "function",
        "lists": "list",
        "tuples": "tuple",
        "sets": "set",
        "dictionaries": "dictionary",
        "integers": "integer",
        "floats": "float",
        "classes": "class",
        "objects": "object",
        "loops": "loop",
        "algorithms": "algorithm"
    }


    words = user_question.split()

    words = [
        replacements.get(word, word)
        for word in words
    ]

    normalized_question = " ".join(words)


    # =====================================================
    # Convert User Question to TF-IDF
    # =====================================================

    user_vector = vectorizer.transform(
        [normalized_question]
    )


    # =====================================================
    # Calculate Cosine Similarity
    # =====================================================

    similarities = cosine_similarity(
        user_vector,
        question_vectors
    )[0]


    # =====================================================
    # Get Best Match
    # =====================================================

    best_index = similarities.argmax()

    best_score = similarities[best_index]


    # =====================================================
    # Minimum Confidence Level
    # =====================================================

    if best_score >= 0.30:

        return questions_answers[
            best_index
        ]["answer"]


    return (
        "I couldn't find a matching answer in my "
        "Python knowledge base. 🐍 "
        "Please try asking your question in a different way."
    )


# =========================================================
# Terminal Chatbot
# =========================================================

def start_chatbot():

    print("=" * 50)

    print(
        "          PYTHON Q&A CHATBOT"
    )

    print("=" * 50)

    print(
        "Ask me any Python programming question."
    )

    print(
        "Type 'exit' to stop."
    )

    print()


    while True:

        user_question = input(
            "You: "
        )


        if user_question.lower().strip() == "exit":

            print(
                "Bot: Thank you! Goodbye."
            )

            break


        answer = find_best_answer(
            user_question
        )


        print(
            "Bot:",
            answer
        )

        print()


# =========================================================
# Run Terminal Chatbot
# =========================================================

if __name__ == "__main__":

    start_chatbot()