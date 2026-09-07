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
# Find Best Answer
# =========================================================

def find_best_answer(user_question):

    user_question = user_question.lower().strip()

    if not user_question:
        return "Please enter a question."

    # Normalize common plural forms
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
    words = [replacements.get(word, word) for word in words]

    normalized_question = " ".join(words)

    # Convert user question to TF-IDF
    user_vector = vectorizer.transform([normalized_question])

    # Calculate similarity
    similarities = cosine_similarity(
        user_vector,
        question_vectors
    )[0]

    # Get best match
    best_index = similarities.argmax()
    best_score = similarities[best_index]

    # Minimum confidence level
    if best_score >= 0.30:
        return questions_answers[best_index]["answer"]

    return "Sorry, I don't know the answer to that question."


# =========================================================
# Terminal Chatbot
# =========================================================

def start_chatbot():

    print("=" * 50)
    print("          PYTHON Q&A CHATBOT")
    print("=" * 50)

    print("Ask me any Python programming question.")
    print("Type 'exit' to stop.")
    print()

    while True:

        user_question = input("You: ")

        if user_question.lower().strip() == "exit":

            print("Bot: Thank you! Goodbye.")
            break

        answer = find_best_answer(user_question)

        print("Bot:", answer)
        print()


# =========================================================
# Run Terminal Chatbot
# =========================================================

if __name__ == "__main__":
    start_chatbot()