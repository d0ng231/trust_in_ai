CUSTOM_CSS = """
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    .upload-box {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        background-color: #fafafa;
    }
    .explanation-box {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        min-height: 150px;
    }
    .questions-box {
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 5px;
        border: none;
        box-shadow: none;
    }
    .ai-classification-box {
        background-color: #fff3e0;
        padding: 8px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin: 3px 0;
    }
    h1 {
        color: #1976d2;
        text-align: center;
        padding-bottom: 5px;
        margin-bottom: 5px;
    }
    h3 {
        color: #2e7d32;
        margin-top: 5px;
        margin-bottom: 5px;
        border-bottom: none !important;
    }
    h4 {
        margin-top: 5px;
        margin-bottom: 5px;
        border-bottom: none !important;
    }
    .stRadio > label {
        font-weight: bold;
        color: #1976d2;
    }
    .confidence-label {
        font-size: 16px;
        font-weight: bold;
        color: #1976d2;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stMarkdown {
        margin-bottom: 0.25rem;
    }
    .stRadio > div {
        gap: 0.3rem;
    }
    .stRadio {
        margin-bottom: 0.25rem;
    }
    .stTextArea > div > div > textarea {
        margin-bottom: 0.25rem;
        color: black !important;
    }
    .stTextArea textarea[disabled] {
        color: black !important;
        -webkit-text-fill-color: black !important;
        opacity: 1 !important;
    }
    .stSlider > div > div > div {
        margin-bottom: 0.25rem;
    }
    hr {
        display: none !important;
    }
    h1, h2, h3, h4, h5, h6 {
        border-bottom: none !important;
        padding-bottom: 0 !important;
    }
    .stMarkdown > div > h3:after {
        display: none !important;
    }
    .main .block-container h3 {
        border-bottom: none !important;
    }
    div[data-testid="stMarkdownContainer"] hr {
        display: none !important;
    }
    .stRadio > label {
        margin-bottom: 0.25rem !important;
    }
    .element-container .stRadio {
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
    }
    .element-container {
        margin-bottom: 0.5rem;
    }
    .main-header {
        margin-bottom: 0.5rem;
    }
    .load-button {
        background-color: #1976d2;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        width: 100%;
    }
    .pre-questionnaire-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        max-width: 600px;
        margin: 0 auto;
    }
    .submit-button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
</style>
"""