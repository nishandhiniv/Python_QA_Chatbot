/* =========================================================
   Python Q&A Chatbot - Main Script
   ========================================================= */


/* =========================================================
   Topic-wise Suggested Questions
   ========================================================= */

const topicQuestions = {

    basics: [
        "What is Python?",
        "What are variables in Python?",
        "What are the data types in Python?",
        "What is the difference between a list and a tuple?"
    ],

    operators: [
        "What are operators in Python?",
        "What are arithmetic operators in Python?",
        "What are comparison operators in Python?",
        "What are logical operators in Python?"
    ],

    conditionals: [
        "What is an if statement in Python?",
        "What is if-else in Python?",
        "What is elif in Python?",
        "What are conditional statements in Python?"
    ],

    loops: [
        "What is a for loop in Python?",
        "What is a while loop in Python?",
        "What is the difference between for and while loops?",
        "What is the use of the break statement?"
    ],

    collections: [
        "What is a list in Python?",
        "What is a tuple in Python?",
        "What is a set in Python?",
        "What is a dictionary in Python?"
    ],

    functions: [
        "What is a function in Python?",
        "What are parameters and arguments?",
        "What is a return statement in Python?",
        "What is a lambda function?"
    ],

    oop: [
        "What is a class in Python?",
        "What is an object in Python?",
        "What is inheritance in Python?",
        "What is polymorphism in Python?"
    ],

    advanced: [
        "What is exception handling in Python?",
        "What are modules and packages in Python?",
        "What is file handling in Python?",
        "What is recursion in Python?"
    ]
};


/* =========================================================
   Topic Names
   ========================================================= */

const topicNames = {

    basics: "Python Basics",

    operators: "Operators",

    conditionals: "Conditional Statements",

    loops: "Loops",

    collections: "Lists & Collections",

    functions: "Functions",

    oop: "Object Oriented Programming",

    advanced: "Advanced Python"
};


/* =========================================================
   Add Message to Chat
   ========================================================= */

function addMessage(message, sender) {

    const chatMessages =
        document.getElementById("chat-messages");

    if (!chatMessages) {
        return;
    }

    const messageWrapper =
        document.createElement("div");

    messageWrapper.className =
        `message-wrapper ${sender}`;

    const messageBubble =
        document.createElement("div");

    messageBubble.className =
        "message-bubble";

    messageBubble.textContent =
        message;

    messageWrapper.appendChild(
        messageBubble
    );

    chatMessages.appendChild(
        messageWrapper
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


/* =========================================================
   Typing Indicator
   ========================================================= */

function showTypingIndicator() {

    const chatMessages =
        document.getElementById("chat-messages");

    if (!chatMessages) {
        return;
    }

    /*
       Prevent duplicate typing indicators.
    */

    removeTypingIndicator();

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "message-wrapper bot";

    wrapper.id =
        "typing-indicator";

    const bubble =
        document.createElement("div");

    bubble.className =
        "message-bubble typing";

    bubble.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    wrapper.appendChild(
        bubble
    );

    chatMessages.appendChild(
        wrapper
    );

    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


function removeTypingIndicator() {

    const typingIndicator =
        document.getElementById(
            "typing-indicator"
        );

    if (typingIndicator) {
        typingIndicator.remove();
    }
}


/* =========================================================
   Send Question to Backend
   ========================================================= */

async function sendQuestion(questionText = null) {

    const questionInput =
        document.getElementById("question");

    const sendButton =
        document.getElementById("send-button");

    if (!questionInput) {
        return;
    }


    let question;


    /*
       If a suggested question was clicked,
       use that question.

       Otherwise use the text typed
       inside the input box.
    */

    if (
        questionText !== null &&
        questionText !== undefined
    ) {

        question =
            String(questionText).trim();

    } else {

        question =
            questionInput.value.trim();
    }


    if (!question) {
        return;
    }


    /* =====================================================
       Show user question
       ===================================================== */

    addMessage(
        question,
        "user"
    );


    /* Clear input */

    questionInput.value = "";


    if (sendButton) {
        sendButton.disabled = true;
    }


    /* Show typing */

    showTypingIndicator();


    try {

        const response =
            await fetch(
                "/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


        /* =================================================
           Login expired
           ================================================= */

        if (response.status === 401) {

            removeTypingIndicator();

            addMessage(
                "Your login session has expired. Please login again.",
                "bot"
            );

            setTimeout(
                () => {
                    window.location.href =
                        "/login";
                },
                1500
            );

            return;
        }


        const result =
            await response.json();


        removeTypingIndicator();


        /* =================================================
           Show bot answer
           ================================================= */

        if (result.answer) {

            addMessage(
                result.answer,
                "bot"
            );

        } else {

            addMessage(
                "Sorry, I couldn't find an answer.",
                "bot"
            );
        }


    } catch (error) {

        console.error(
            "Question error:",
            error
        );

        removeTypingIndicator();

        addMessage(
            "Unable to connect to the chatbot. Please try again.",
            "bot"
        );

    } finally {

        if (sendButton) {
            sendButton.disabled = false;
        }

        questionInput.focus();
    }
}


/* =========================================================
   Show Topic Suggestions
   ========================================================= */

function showTopicSuggestions(topic) {

    /*
       Make sure topic exists.
    */

    const questions =
        topicQuestions[topic];

    if (
        !questions ||
        questions.length === 0
    ) {
        console.warn(
            "No questions found for topic:",
            topic
        );

        return;
    }


    const chatMessages =
        document.getElementById(
            "chat-messages"
        );

    if (!chatMessages) {
        return;
    }


    const topicName =
        topicNames[topic] ||
        "Python";


    /* =====================================================
       Suggestion wrapper
       ===================================================== */

    const suggestionWrapper =
        document.createElement("div");

    suggestionWrapper.className =
        "message-wrapper bot topic-suggestions";


    /* =====================================================
       Suggestion bubble
       ===================================================== */

    const suggestionBubble =
        document.createElement("div");

    suggestionBubble.className =
        "message-bubble";


    /* =====================================================
       Title
       ===================================================== */

    const title =
        document.createElement("strong");

    title.textContent =
        `💡 ${topicName} - Suggested Questions`;

    suggestionBubble.appendChild(
        title
    );


    /* =====================================================
       Question container
       ===================================================== */

    const suggestionContainer =
        document.createElement("div");

    suggestionContainer.className =
        "topic-suggestion-list";


    /*
       Keep these styles here so the dynamically
       created questions always remain clickable.
    */

    suggestionContainer.style.marginTop =
        "10px";

    suggestionContainer.style.display =
        "flex";

    suggestionContainer.style.flexDirection =
        "column";

    suggestionContainer.style.gap =
        "7px";


    /* =====================================================
       Create question buttons
       ===================================================== */

    questions.forEach(
        question => {

            const button =
                document.createElement("button");

            button.type =
                "button";

            button.className =
                "suggested-question";

            button.textContent =
                question;

            /*
               Store actual question.
            */

            button.dataset.question =
                question;


            /*
               Extra safety:
               directly handle the click also.
            */

            button.addEventListener(
                "click",
                function(event) {

                    event.preventDefault();
                    event.stopPropagation();

                    const selectedQuestion =
                        this.dataset.question ||
                        this.textContent.trim();

                    if (!selectedQuestion) {
                        return;
                    }

                    sendQuestion(
                        selectedQuestion
                    );
                }
            );


            suggestionContainer.appendChild(
                button
            );

        }
    );


    suggestionBubble.appendChild(
        suggestionContainer
    );


    suggestionWrapper.appendChild(
        suggestionBubble
    );


    chatMessages.appendChild(
        suggestionWrapper
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


/* =========================================================
   Suggested Question Click Handler
   ========================================================= */

function setupSuggestedQuestionClicks() {

    /*
       Use document-level event delegation.

       This supports:
       1. Questions already present in index.html
       2. Questions dynamically created by topic cards
    */

    document.addEventListener(
        "click",
        function(event) {

            const button =
                event.target.closest(
                    ".suggested-question"
                );


            if (!button) {
                return;
            }


            /*
               If the button already has its own
               listener, don't send twice.
            */

            if (
                button.closest(
                    ".topic-suggestion-list"
                )
            ) {
                return;
            }


            event.preventDefault();
            event.stopPropagation();


            const question =
                button.dataset.question ||
                button.getAttribute("data-question") ||
                button.textContent.trim();


            if (!question) {
                return;
            }


            sendQuestion(
                question
            );

        }
    );
}


/* =========================================================
   Get Topic From Card
   ========================================================= */

function getTopicFromCard(card) {

    if (!card) {
        return null;
    }


    /*
       First priority:
       data-topic attribute.
    */

    let topic =
        card.dataset.topic;


    if (topic) {

        topic =
            topic.toLowerCase().trim();

        if (topicQuestions[topic]) {
            return topic;
        }
    }


    /*
       Backup:
       Try to identify topic from the
       visible card text.
    */

    const text =
        card.textContent
            .toLowerCase()
            .trim();


    if (
        text.includes("basic") ||
        text.includes("python basics")
    ) {
        return "basics";
    }


    if (
        text.includes("operator")
    ) {
        return "operators";
    }


    if (
        text.includes("conditional") ||
        text.includes("if")
    ) {
        return "conditionals";
    }


    if (
        text.includes("loop")
    ) {
        return "loops";
    }


    if (
        text.includes("collection") ||
        text.includes("list")
    ) {
        return "collections";
    }


    if (
        text.includes("function")
    ) {
        return "functions";
    }


    if (
        text.includes("object") ||
        text.includes("oop")
    ) {
        return "oop";
    }


    if (
        text.includes("advanced")
    ) {
        return "advanced";
    }


    return null;
}


/* =========================================================
   Topic Cards
   ========================================================= */

function setupTopicCards() {

    const topicCards =
        document.querySelectorAll(
            ".topic-card"
        );


    if (!topicCards.length) {

        console.warn(
            "No topic cards found."
        );

        return;
    }


    topicCards.forEach(
        card => {

            /*
               Make cards behave like clickable
               controls.
            */

            card.style.cursor =
                "pointer";


            card.addEventListener(
                "click",
                function(event) {

                    event.preventDefault();
                    event.stopPropagation();


                    const topic =
                        getTopicFromCard(
                            this
                        );


                    if (!topic) {

                        console.warn(
                            "Unable to identify topic card:",
                            this.textContent
                        );

                        return;
                    }


                    /*
                       Show related questions.

                       IMPORTANT:
                       Do NOT automatically send
                       any question.
                    */

                    showTopicSuggestions(
                        topic
                    );

                }
            );

        }
    );
}


/* =========================================================
   Enter Key Support
   ========================================================= */

function setupEnterKey() {

    const questionInput =
        document.getElementById(
            "question"
        );


    if (!questionInput) {
        return;
    }


    questionInput.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendQuestion();
            }

        }
    );
}


/* =========================================================
   Welcome Message
   ========================================================= */

function showWelcomeMessage() {

    const chatMessages =
        document.getElementById(
            "chat-messages"
        );


    if (!chatMessages) {
        return;
    }


    if (
        chatMessages.dataset.welcomeShown ===
        "true"
    ) {
        return;
    }


    addMessage(
        "Hello! 👋 I'm your Python Q&A Chatbot. Ask me anything related to Python programming, or choose a topic below to see suggested questions.",
        "bot"
    );


    chatMessages.dataset.welcomeShown =
        "true";
}


/* =========================================================
   Logout
   ========================================================= */

function setupLogout() {

    const logoutButton =
        document.getElementById(
            "logout-button"
        );


    if (!logoutButton) {
        return;
    }


    logoutButton.addEventListener(
        "click",
        async () => {

            try {

                await fetch(
                    "/logout",
                    {
                        method: "POST"
                    }
                );

            } catch (error) {

                console.error(
                    "Logout error:",
                    error
                );
            }


            /*
               Keep chatbot name in localStorage.
            */

            window.location.href =
                "/login";
        }
    );
}


/* =========================================================
   Check Login Status
   ========================================================= */

async function checkLoginStatus() {

    try {

        const response =
            await fetch(
                "/check-login"
            );


        if (!response.ok) {

            window.location.href =
                "/login";

            return false;
        }


        const result =
            await response.json();


        if (!result.logged_in) {

            window.location.href =
                "/login";

            return false;
        }


        /* Display username */

        const usernameElements =
            document.querySelectorAll(
                ".logged-in-username"
            );


        usernameElements.forEach(
            element => {

                element.textContent =
                    result.username || "";

            }
        );


        return true;


    } catch (error) {

        console.error(
            "Login check error:",
            error
        );

        return false;
    }
}


/* =========================================================
   Page Initialization
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        const loggedIn =
            await checkLoginStatus();


        if (!loggedIn) {
            return;
        }


        /*
           Setup all features.
        */

        setupSuggestedQuestionClicks();

        setupTopicCards();

        setupEnterKey();

        setupLogout();

        showWelcomeMessage();


        /* Focus input */

        const questionInput =
            document.getElementById(
                "question"
            );


        if (questionInput) {
            questionInput.focus();
        }

    }
);