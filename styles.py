CUSTOM_CSS = """
<style>
    .block-container {
        /* Increased top padding to push all content below the fixed header */
        padding: 6rem 1rem 2rem 1rem;
    }

    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    h1 {
        color: #1976d2;
        text-align: center;
        padding-bottom: 5px;
        margin-bottom: 5px;
    }
    h3 {
        color: #2e7d32;
    }
    h1, h2, h3, h4, h5, h6 {
        border-bottom: none !important;
        padding-bottom: 0 !important;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stMarkdown {
        margin-bottom: 0.25rem;
    }
    .stRadio {
        margin-bottom: 0.1rem;
    }
    .stRadio > label {
        font-weight: bold;
        color: #1976d2;
        margin-bottom: 0.25rem !important;
    }
    .stRadio > div {
        gap: 0.3rem;
    }
    .element-container {
        margin-bottom: 0.5rem;
    }
    .welcome-container {
        background-color: transparent;
        box-shadow: none;
        border: none;
        margin: 0 0 2rem 0;
        text-align: left;
    }
    .ai-classification-box {
        background-color: #cfe2f3;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        margin-top: 15px;
        line-height: 1.4;
    }
    .classification-title {
        font-size: 14px;
        font-weight: 500;
        color: #616161;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .classification-main {
        font-size: 22px;
        font-weight: bold;
        color: #000000;
    }
    .classification-fullname {
        font-size: 16px;
        font-weight: 500;
        color: #424242;
    }
    .suggestion-container {
        padding: 0.5rem 0.1rem;
    }
    .suggestion-container .stButton > button {
        background-color: #f0f2f6;
        color: #333;
        border: 1px solid #dcdcdc !important;
        border-radius: 12px !important;
        font-size: 10px;
        font-weight: 500;
        text-align: left !important;
        padding: 0.5rem 1rem !important;
        margin-bottom: 3px !important;
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }
    .suggestion-container .stButton > button:hover {
        background-color: #e6e8eb !important;
        border-color: #b0b0b0 !important;
        color: #000;
    }
    .suggestion-container .stButton > button:focus {
        box-shadow: none !important;
    }
</style>
"""