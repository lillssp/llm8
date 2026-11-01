import streamlit as st
from docx import Document
from google import genai
from google.genai import types

MODEL = "gemini-3.5-flash"
MAX_CHARS = 60000  
MAX_PDF_MB = 18  

PROMPT = """You are an experienced and friendly mentor. Turn raw notes, text or slides \
from a university lecture into a well-structured, easy-to-follow set of study notes.

RULES:
1. Reply in the same language the materials are written in.
2. Output ONLY the notes themselves. No introductions, explanations or closing remarks \
such as "Here are your notes..." or "Hope this helps".
3. Tone: friendly but academic and technically accurate. Explain complex ideas clearly, \
without oversimplifying, and add short examples where useful.
4. The notes may be fragmentary: restore the logic and fill in the necessary theory \
so the result is a complete study guide.
5. If a PDF with slides is provided, consider not only the text but also the images, \
diagrams and charts: briefly describe what they show and what idea they illustrate.
6. Write formulas in LaTeX: $E = mc^2$ for inline and $$...$$ for display equations.
7. Markdown structure: headings '## ' and '### ', lists '- ' and '1. ', \
'---' between large blocks, **bold** for key terms.

Lecture materials:
"""

CSS = """
<style>
.stApp {
    background: linear-gradient(135deg, #fde4f2 0%, #ece4fd 100%);
}
[data-testid="stHeader"] { background: transparent; }
h1 { color: #b04a9c !important; text-align: center; }
.subtitle { text-align: center; color: #7a5c99; margin-bottom: 1.5rem; }
button[kind="primary"] {
    border-radius: 20px;
    background: linear-gradient(90deg, #f78fc6, #b69cf5);
    border: none;
    color: white;
}
input, textarea { border-radius: 14px !important; }
</style>
"""


def summarize(api_key, text, file):
    if not api_key:
        return "Please enter your Gemini API key."

    contents = [PROMPT]

    if text and text.strip():
        contents.append(text)

    if file:
        name = file.name.lower()
        if name.endswith(".pdf"):
            if file.size > MAX_PDF_MB * 1024 * 1024:
                return f"The PDF is too large (max {MAX_PDF_MB} MB)."
            contents.append(types.Part.from_bytes(data=file.getvalue(), mime_type="application/pdf"))
        elif name.endswith(".docx"):
            contents.append("\n".join(p.text for p in Document(file).paragraphs))
        else:
            contents.append(file.getvalue().decode("utf-8", errors="ignore"))

    if len(contents) == 1:
        return "Please add some text or a file."

    contents = [c[:MAX_CHARS] if isinstance(c, str) else c for c in contents]

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=MODEL, contents=contents)
        return response.text
    except Exception as e:
        return f"Error: {e}"


st.set_page_config(page_title="Lecture Notes Maker", page_icon="🌸")
st.markdown(CSS, unsafe_allow_html=True)

st.title("Lecture Notes Maker")
st.markdown(
    '<p class="subtitle">Paste your lecture notes or upload a file (.txt, .md, .docx, .pdf) and get '
    "well-structured study notes with formulas</p>",
    unsafe_allow_html=True,
)

api_key = st.text_input("Gemini API key", type="password", placeholder="...")
text = st.text_area("Lecture text", height=200)
file = st.file_uploader("Or upload a file", type=["txt", "md", "pdf", "docx"])

if st.button("Make notes", type="primary", use_container_width=True):
    with st.spinner("Writing your notes..."):
        result = summarize(api_key, text, file)
    with st.container(border=True):
        st.markdown(result)