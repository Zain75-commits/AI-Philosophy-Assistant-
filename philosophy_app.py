import streamlit as st
import openai
from datetime import datetime
import os
from fpdf import FPDF

# Set page config
st.set_page_config(page_title="🧠 AI Philosophy Assistant", layout="wide")

# Load OpenAI API key from Streamlit secrets or environment
openai.api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Custom styles
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        .block-container {
            padding: 2rem 2rem 2rem 2rem;
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .stTextArea textarea {
            background-color: #f0f0f5;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>🧠 AI Philosophy Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Think deeply. Generate freely. Reflect authentically.</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for export and theme tag
with st.sidebar:
    st.header("🛠️ Options")
    export_format = st.radio("📤 Export as", ["Markdown", "PDF"])
    theme_tag = st.text_input("🏷️ Theme tag", placeholder="e.g. metaphysics, ethics...")
    st.markdown("Developed by **AI PhA**")

# Input area
st.subheader("💭 Enter Your Philosophical Thoughts")
user_input = st.text_area("Write your idea, argument, or paradox below", height=150, placeholder="Start writing something deep...")

# Voice Input Note
with st.expander("🎙️ Voice Input Help"):
    st.info("To use voice input, you can integrate JavaScript microphone support or use speech-to-text tools like Whisper.")

# Generate button
if st.button("✨ Generate Philosophical Concept"):
    if not user_input.strip():
        st.warning("Please enter your philosophical thoughts first.")
    else:
        with st.spinner("Thinking deeply..."):
            try:
                prompt = f"""
                You are an AI philosopher. Based on the following idea, generate an original and coherent philosophical concept or argument.
                It must be authentic, non-derivative, and titled.

                User input: {user_input}
                """
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.85
                )
                ai_idea = response['choices'][0]['message']['content']
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.success("Philosophical concept generated!")
                st.markdown(f"#### 🪷 Generated Concept

{ai_idea}", unsafe_allow_html=True)
                st.session_state.history.append({
                    "timestamp": timestamp,
                    "input": user_input,
                    "output": ai_idea,
                    "tag": theme_tag
                })
            except Exception as e:
                st.error(f"Error: {e}")

# History section
st.markdown("---")
st.subheader("📜 Philosophical Idea History")
if st.session_state.history:
    for i, entry in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"#### {i}. 🕒 {entry['timestamp']}  `#{entry['tag'] or 'untagged'}`")
        st.markdown(f"**User Input:** {entry['input']}")
        st.markdown(f"**Generated Output:** {entry['output']}")
        st.markdown("---")
else:
    st.info("No ideas generated yet. Begin your philosophical journey above.")

# Export options
if st.session_state.history:
    if st.button(f"📥 Download Session as {export_format}"):
        if export_format == "Markdown":
            md = "# AI Philosophy Session\n\n"
            for entry in st.session_state.history:
                md += f"## {entry['timestamp']} - {entry['tag'] or 'untagged'}\n"
                md += f"**Input:** {entry['input']}\n\n"
                md += f"**Output:**\n{entry['output']}\n\n"
            st.download_button("📄 Download Markdown", data=md, file_name="philosophy_session.md")
        else:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="AI Philosophy Session", ln=True, align="C")
            for entry in st.session_state.history:
                pdf.ln(10)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt=f"{entry['timestamp']} - {entry['tag'] or 'untagged'}", ln=True)
                pdf.set_font("Arial", '', 12)
                pdf.multi_cell(0, 10, txt=f"Input: {entry['input']}\n\nOutput:\n{entry['output']}")
            pdf_path = "/tmp/philosophy_session.pdf"
            pdf.output(pdf_path)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download PDF", f, file_name="philosophy_session.pdf")