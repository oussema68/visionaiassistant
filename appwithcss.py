import base64
import streamlit as st
from pathlib import Path
import google.generativeai as genai

from api_key import api_key

# Configure the page
st.set_page_config(page_title="Image Analysis", page_icon=":robot:")

# Custom CSS for chat bubbles
st.markdown("""
    <style>
    .user-bubble {
        background-color: #ADD8E6;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        text-align: left;
    }
    .ai-bubble {
        background-color: #98FB98;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        text-align: left;
    }
    .message-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 10px;
    }
    .message-container.user {
        justify-content: flex-end;
    }
    </style>
""", unsafe_allow_html=True)

# Configure genai with the API key
genai.configure(api_key=api_key)

# Set the model configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Apply safety measures
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """

"""   #include your prompt and how you want the model to act within the brackets

# Cache the model initialization
@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro-exp-0801",
        generation_config=generation_config,
        safety_settings=safety_settings
    )

model = load_model()

# Cache the AI response
@st.cache_data
def generate_ai_response(prompt_parts):
    try:
        return model.generate_content(prompt_parts)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Set the logo
st.image("logo/logo.png", width=200)

# Set the title
st.title("Image Analysis")

# Set the subtitle
st.subheader("Your personal companion now can see and help even more")
uploaded_file = st.file_uploader("Let me seeee ", type=["png", "jpg", "jpeg"])

submit_button = st.button("Submit")

# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# If the user uploads an image
# Store the image in session state
if uploaded_file and submit_button:
    # Process the uploaded image
    image_data = uploaded_file.getvalue()
    st.session_state["uploaded_image"] = image_data  # Save image to session state
    uploaded = st.session_state["uploaded_image"]

    # Convert the image data to base64 for Markdown display
    image_b64 = base64.b64encode(image_data).decode("utf-8")
    image_md = f"![User Image](data:image/png;base64,{image_b64})"
    
    # Add the image to chat history as a user message
    st.session_state["chat_history"].append({"role": "user", "content": image_md, "image_data": image_data  })
    
    
    # Display the image
    st.image(image_data, width=350)
    

    # Define the image as a part of the prompt
    image_parts = [{"mime_type": uploaded_file.type, "data": image_data}]
    
    # Combine the system prompt and image data
    prompt_parts = [image_parts[0], system_prompt]

    # Generate content based on the image and system prompt
    response = generate_ai_response(prompt_parts)
    st.session_state["chat_history"].append({"role": "assistant", "content": response.text})

# Display the conversation with styled chat bubbles
for message in st.session_state["chat_history"]:
    if message["role"] == "user":
        if message["content"].startswith("![User Image]"):
            st.markdown(f"""
            <div class="message-container user">
                <div class="user-bubble">
            """, unsafe_allow_html=True)
            # Use st.image to display the image
            st.image(message["image_data"], width=350)
            st.markdown(f"""
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-container user"><div class="user-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message-container"><div class="ai-bubble">{message["content"]}</div></div>', unsafe_allow_html=True)


# Chat interface with manual clearing
if "user_message" not in st.session_state:
    st.session_state["user_message"] = ""

if "message_count" not in st.session_state:
    st.session_state["message_count"] = 0



    

# Get user input
user_message = st.text_input("Say something...", key=f"input_{st.session_state['message_count']}")

if st.button("Send"):
    if user_message:
        # Add the user message to the chat history
        st.session_state["chat_history"].append({"role": "user", "content": user_message})

        # Increment the counter to change the key, resetting the input field
        st.session_state["message_count"] += 1

        # Include the previously uploaded image in the conversation, if available
        if "uploaded_image" in st.session_state:
            image_parts = [{"mime_type": "image/png", "data": st.session_state["uploaded_image"]}]
            prompt_parts = [image_parts[0], user_message]
        else:
            prompt_parts = [user_message]

        # Generate response from the AI
        chat_response = generate_ai_response(prompt_parts)

        # Add the AI response to the chat history
        st.session_state["chat_history"].append({"role": "assistant", "content": chat_response.text})

        # Update the page to reflect the new chat state
        st.rerun()  # If rerun isn't available, you can remove this line
