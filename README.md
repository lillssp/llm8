# Lecture Notes Maker

A small web app that turns raw lecture notes, text files or slides into well-structured study notes with formulas.

- **Input:** pasted text or a file (`.txt`, `.md`, `.docx`, `.pdf`).
- **Output:** Markdown notes (headings, lists, bold key terms, LaTeX formulas) with no introductions or closing remarks, just the result.
- **Model:** Google Gemini.
- **Built with:** Streamlit.

## Run locally

```
pip install -r requirements.txt
streamlit run app.py
```