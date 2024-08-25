
# The Limit

<img src="https://github.com/oussema68/visionaiassistant/blob/master/logo/logo.png" alt="Logo" width="200"/>

**An ai vision assistant**

# Image Analysis Streamlit App

## Overview

This is a Streamlit web application that allows users to upload images or documents and receive detailed feedback, suggestions, or analysis based on the content. The app is powered by Google Generative AI for providing insights and responses based on the uploaded content.

## Features

- **Image/Document Upload:** Supports uploading images in PNG, JPG, JPEG formats, and documents in PDF, DOC, DOCX, and TXT formats.
- **AI-Powered Analysis:** Uses Google's Generative AI to analyze the content and provide feedback.
- **Chat Interface:** Interactive chat interface where users can ask questions and receive responses.
- **Customizable Interface:** User and AI messages are displayed in custom-styled chat bubbles.

## Installation

-**Create a virtual environment (optional but recommended):**


   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


-**Clone the repository:**

    

    git clone https://github.com/oussema68/visionaiassistant.git
    cd visionaiassistant
-**Create a .env file in the root directory:**

Inside the .env file, add your Google Generative AI API key:


    API_KEY=<your-google-generative-ai-api-key>
-**Install the required packages:**


    pip install -r requirements.txt

-**Run the Streamlit app:**

    streamlit run app.py


## Usage

**Upload an Image/Document:** Click on the "Let me seeee" button to upload an image or document.

**Submit for Analysis:** Once the file is uploaded, click the "Submit" button to receive feedback or analysis from the AI.

**Interactive Chat:** You can interact with the AI by typing questions or comments in the chat box and clicking "Send."

## Customization

**Styling:** The app uses custom CSS to style the chat bubbles. You can modify the CSS in the st.markdown section of the app.py file.

**Model Configuration:** The AI model's parameters like temperature, top_p, and top_k can be customized in the generation_config dictionary.
Repository Structure

**app.py:** The main script for running the Streamlit app.
requirements.txt: Lists the Python packages required to run the app.

**logo/:** Contains the logo image displayed in the app.

**.env:** Contains environment variables, including the API key (not included in the repo for security reasons).



## Contact
If you have any questions or feedback, feel free to contact me at ohammadi.oh@gmail.com.

