# Assessment Tool Setup Guide

This guide provides step-by-step instructions to configure and run the assessment tool.

## Prerequisites

* A Google Account with access to Google Drive.
* Python 3.8+ installed on your local machine.
* Git installed on your local machine.

---

## Setup Instructions

### Part 1: Google Drive & Apps Script Configuration

1.  **Create Google Drive Folders**: In your Google Drive, create the following folders: `data`, `results`, `images`, `csvs`, `overlays`, and `gradcam`.

2.  **Upload Project Assets**:
    * Upload your `metadata.json` and `password.txt` files to the `data` folder.
    * Upload all images, CSVs, and other asset files into their corresponding folders.

3.  **Deploy the Google Apps Script**:
    * Create a new project in the [Google Apps Script editor](https://script.google.com).
    * Delete the default code and paste in the entire contents of the project's `Code.gs` file.
    * In the script, find the `FOLDER_IDS` dictionary and update it with the unique Folder ID for each folder you created. You can find a folder's ID in its URL (`drive.google.com/drive/folders/THIS_IS_THE_ID`).
    * Click **Deploy > New deployment**.
    * For **Select type**, choose **Web app**.
    * Under **Configuration**, set **Execute as** to **Me**.
    * Under **Configuration**, set **Who has access** to **Anyone**.
    * Click **Deploy**. You must **Authorize access** when prompted.
    * After deployment, copy the **Web app URL**.

### Part 2: Local Application Setup

1.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the Application**:
    * Open the `config.py` file.
    * Find the `APPSCRIPT_URL` variable and paste the **Web app URL** you copied from your Apps Script deployment.

---

## Usage Instructions

### Running the Application

Launch the Streamlit app from your terminal:
```bash
streamlit run main.py
```

### Accessing the Evaluation Dashboard

1.  Open the application in your browser.
2.  In the sidebar, click the **Evaluation mode** expander.
3.  Enter the password from your `password.txt` file and click **Enter**.