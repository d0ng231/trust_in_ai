# AI-Assisted Medical Imaging Assessment Tool

This project provides a web-based platform for clinicians to assess and validate AI-driven classifications of medical images, specifically Optical Coherence Tomography Angiography (OCTA) scans for diabetic retinopathy. The tool presents users with an AI's diagnosis and one of three types of explanations (text, Grad-CAM, or graph-based). It records the clinicians' feedback, trust levels, and interactions to evaluate the efficacy and usability of different AI explanation methods.


## Project Structure

```

.
├── results/                \# Directory where assessment JSON files are saved
├── main.py                   \# Main application entry point
├── evaluation.py             \# Contains the UI and logic for the evaluation dashboard
├── components.py             \# UI components for the assessment interface
├── config.py                 \# Configuration settings (file paths, modes, etc.)
├── data\_handler.py           \# Handles saving assessment data to JSON files
├── image\_loader.py           \# Loads image and explanation data from metadata
├── state\_manager.py          \# Manages session state for the Streamlit app
├── styles.py                 \# Custom CSS for styling the application
├── inference.py              \# Functions for interacting with the VLM
├── metadata.json             \# Metadata file linking images to labels and explanations
└── requirements.txt          \# Python package dependencies

````

## Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Install Dependencies**
    Ensure you have Python 3.8+ installed. Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Data Configuration**
    * Place your OCTA images and explanation images in the appropriate directories.
    * Update the `metadata.json` file to correctly point to the image files. The paths should be accessible from where you run the application.
    * Modify the `OUTPUT_DIR` in `config.py` to set where the assessment results should be saved.

## Running the Application

The application has two modes, which can be toggled in the `config.py` file.

### 1. Assessment Mode

This is the default mode for collecting data from clinicians.

* **Configuration**: In `config.py`, set `EVALUATION_MODE = False`.
* **Run Command**:
    ```bash
    streamlit run main.py
    ```
* The application will launch in your web browser, starting with the pre-assessment questionnaire.

### 2. Evaluation Mode

This mode is for analyzing the collected assessment data.

* **Configuration**: In `config.py`, set `EVALUATION_MODE = True`.
* **Run Command**:
    ```bash
    streamlit run main.py
    ```
* The application will launch the evaluation dashboard, which loads all `.json` files from the `results` directory.
