# app.py
import streamlit as st
from pdf_loader import load_pdf_text
from bedrock_chat import ask_claude

st.set_page_config(page_title="Claude PDF Chatbot", layout="wide")

st.title("📄 Claude PDF Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("PDF Reader")
    
    # Option 1: Upload a PDF from the UI
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_file is not None:
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())
        raw_text = load_pdf_text("temp_uploaded.pdf", single_file=True)
        st.session_state.raw_text = raw_text
        st.success("PDF Uploaded and Loaded!")

    # Option 2: Load PDF from folder (still keep this)
    st.markdown("---")
    folder_path = "../data"
    if st.button("Load PDF from /data"):
        raw_text = load_pdf_text(folder_path)
        st.session_state.raw_text = raw_text
        st.success("PDF Loaded from /data!")


# Chat Section
if "raw_text" in st.session_state:
    user_input = st.text_input("Ask Claude something based on the PDF:")
    
    if st.button("Send") and user_input:
        full_prompt = f"Here is the document:\n\n{st.session_state.raw_text}\n\nHuman: {user_input}\n\nAssistant:"
        response = ask_claude(full_prompt)
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Claude", response))

# Show chat history
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑‍💻 {speaker}:** {msg}")
    else:
        st.markdown(f"**🤖 {speaker}:** {msg}")
