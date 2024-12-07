import openai
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Question & Answer Generator", layout="wide")

st.sidebar.title("🔑 Enter Your API Key")
openai.api_key = st.sidebar.text_input("OpenAI API key", type="password")

st.markdown("<h1 style='text-align: center;'>📚 Question & Answer Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate 10 diverse questions and answers based on the input text.</p>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📤 Input Your Text Below")

col1, col2 = st.columns([1, 3])

with col1:
    uploaded_file = st.file_uploader("Upload a text file (optional)", type=["txt"])

with col2:
    text_input = st.text_area("Or enter your text directly:")

text = None
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
elif text_input.strip():
    text = text_input.strip()

def generate_questions_and_answers(input_text):
    if not input_text:
        st.warning("No input text provided. Please enter some text.")
        return []

    prompt = f"""
    You are an expert at creating educational content. Based on the following text, generate 10 diverse questions and provide their answers. The questions should include:
    1. Four comprehension questions.
    2. Three detail-oriented questions.
    3. Three analytical or critical thinking questions.

    Format the output as follows:
    - Question: [Write the question here]
    - Answer: [Write the corresponding answer here]

    Text: {input_text}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an expert at generating questions and answers for text comprehension."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        qa_pairs = response["choices"][0]["message"]["content"].strip().split("\n\n")
        questions_and_answers = [
            pair.split("\n") for pair in qa_pairs if "Question:" in pair and "Answer:" in pair
        ]
    except Exception as e:
        st.error(f"Error communicating with OpenAI API: {e}")
        return []

    return questions_and_answers

if text:
    st.markdown("---")
    st.subheader("📄 Generated Questions and Answers")
    with st.spinner("Generating questions and answers..."):
        qa_pairs = generate_questions_and_answers(text)

        if qa_pairs:
            df = pd.DataFrame({
                "Question": [qa[0].replace("Question: ", "") for qa in qa_pairs],
                "Answer": [qa[1].replace("Answer: ", "") for qa in qa_pairs]
            })

            st.dataframe(df, use_container_width=True)

            st.markdown("### 📥 Download")
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Questions and Answers as CSV",
                data=csv,
                file_name="generated_questions_and_answers.csv",
                mime="text/csv",
            )

        else:
            st.warning("No questions and answers could be generated for the provided text.")
else:
    st.info("Please upload a file or enter text to generate questions and answers.")



