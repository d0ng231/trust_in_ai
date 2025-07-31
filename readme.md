# AI-Assisted Medical Imaging Assessment Tool

This is a web-based platform for clinicians to assess AI-driven classifications of OCTA scans. The tool connects to Google Drive for all data management, allowing for a fully cloud-native workflow. It presents clinicians with an AI diagnosis and various explanation types (text, Grad-CAM, graph-based), then records their feedback to evaluate the AI's efficacy.

### Core Features

* **Cloud-Based**: All images, metadata, and results are stored and managed directly on Google Drive.
* **Interactive Explanations**: Supports text-based conversational chat with a Vision Language Model (VLM).
* **Secure Evaluation**: A password-protected dashboard provides a comprehensive analysis of all collected assessments.

---

## Architecture

The system consists of two main components:
1.  A **Streamlit web application** that serves as the user interface for both clinicians and researchers.
2.  A **Google Apps Script** that acts as a secure API bridge between the Streamlit app and your data stored in Google Drive.

---

## Setup and Installation

### Step 1: Google Drive Configuration

1.  In your Google Drive, create the necessary folders (e.g., `data`, `results`, `images`, `csvs`, `overlays`, `gradcam`).
2.  Upload your assets:
    * `metadata.json` and `password.txt` go into the `data` folder.
    * All image and CSV files go into their corresponding folders.
3.  For each folder you created, get its unique **Folder ID** from the URL in your browser (it's the long string of characters after `folders/`).

### Step 2: Deploy Google Apps Script

1.  Create a new Google Apps Script project.
2.  Paste the entire contents of `Code.gs` into the script editor.
3.  Update the `FOLDER_IDS` dictionary in the script with the actual IDs you collected in the previous step.
4.  Deploy the script as a **Web App**.
    * Click **Deploy > New deployment**.
    * Select **Web app** as the type.
    * For "Who has access," select **Anyone with Google account** or **Anyone** depending on your user base.
    * Click **Deploy**. You will need to authorize the script's permissions.
5.  Copy the generated **Web app URL**.

### Step 3: Configure the Python Application

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```
2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Update Configuration**
    * Open `config.py`.
    * Paste your **Web app URL** into the `APPSCRIPT_URL` variable.

---

## Running the Application

1.  **Launch the App**
    ```bash
    streamlit run main.py
    ```
    The application will open in your browser, ready for clinician assessments.

2.  **Accessing the Evaluation Dashboard**
    * To view the results, open the application's sidebar.
    * Enter the password (from your `password.txt` file on Google Drive) in the "Evaluation mode" expander.
    * This will unlock the dashboard and display the analytics from all saved assessments.