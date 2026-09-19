import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing. Please add it to your .env file.")
    st.stop()

# --------------------------------------------------
# Groq Client
# --------------------------------------------------

client = Groq(api_key=GROQ_API_KEY)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student AI Chatbot",
    page_icon="",
    layout="centered"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">Student AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI-powered learning assistant</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("Chatbot Settings")

    model = st.selectbox(
        "Select Model",
        [
            "openai/gpt-oss-120b",
            "qwen/qwen3-32b"
        ]
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1
    )

    st.divider()

    st.subheader("Student Assistant")

    st.write("""
    Ask questions related to:

    - Python
    - Data Science
    - AI & ML
    - Mathematics
    - Programming
    - SQL
    - Computer Science
    - General studies
    """)

    if st.button("Clear Chat", use_container_width=True):

        st.session_state.messages = [
            {
                "role": "system",
                "content": """
You are an expert Student AI Tutor.

Your job is to help students learn concepts clearly.

Rules:
1. Explain concepts in simple language.
2. Give examples whenever useful.
3. Break difficult concepts into steps.
4. Encourage understanding rather than memorization.
5. If a student asks for code, explain the code as well.
6. If the question is ambiguous, ask for clarification.
7. Do not unnecessarily make answers complicated.
8. Use headings and bullet points when appropriate.
"""
            }
        ]

        st.rerun()

# --------------------------------------------------
# Initialize Chat History
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": """
You are an expert Student AI Tutor.

Your job is to help students learn concepts clearly.

Rules:
1. Explain concepts in simple language.
2. Give examples whenever useful.
3. Break difficult concepts into steps.
4. Encourage understanding rather than memorization.
5. If a student asks for code, explain the code as well.
6. If the question is ambiguous, ask for clarification.
7. Do not unnecessarily make answers complicated.
8. Use headings and bullet points when appropriate.
"""
        }
    ]

# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# User Input
# --------------------------------------------------

user_prompt = st.chat_input(
    "Ask your question..."
)

# --------------------------------------------------
# Generate Response
# --------------------------------------------------

if user_prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    # Generate AI response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        try:

            stream = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=2048,
                stream=True
            )

            for chunk in stream:

                if chunk.choices[0].delta.content:

                    content = chunk.choices[0].delta.content

                    full_response += content

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            response_placeholder.markdown(full_response)

            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )

        except Exception as e:

            st.error(
                f"Error while generating response: {str(e)}"
            )