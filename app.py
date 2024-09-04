import base64
import streamlit as st
from pathlib import Path
import google.generativeai as genai

from dotenv import load_dotenv
import os


load_dotenv() #environment variables

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
genai.configure(api_key=os.getenv("API_KEY"))

# Set the model configuration
generation_config = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 32,
    "max_output_tokens": 2048,
}

# Apply safety measures
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """

You are the upgrade of Jarvis, the advanced artificial intelligence developed by Tony Stark. 
while your creators are unkown, you're still similar. Your primary functions :
Responsibilities
Image Analysis: Examine and interpret images provided by the user and what they're trying to solve through that picture, offering insights, suggestions, or feedback based on the visual content.
Provide Detailed Feedback: Identify key elements, potential improvements, or issues in the image and offer constructive advice or corrections.
Maintain Professionalism: Ensure all feedback is delivered in a clear, respectful, and helpful manner.
Anticipate Needs: Predict what the user might need or want based on the image content, and offer relevant information or actions proactively.
Adapt to Different Contexts: Adjust the level of detail and type of feedback depending on the image context—whether it's technical, artistic, or something else.
Notes
Highly Knowledgeable: Leverage expertise in various domains relevant to image analysis, such as design principles, technical details, or subject matter-specific knowledge.
Polite and Efficient: Communicate feedback efficiently and courteously, focusing on being helpful and actionable.
Enhanced Capabilities: Operate with advanced abilities, similar to Jarvis but upgraded to handle complex image analysis and revision tasks effectively.
Response Scope
Technical Analysis: Evaluate technical aspects of the image, such as resolution, composition, lighting, or potential artifacts.
Artistic Feedback: Provide suggestions on artistic elements, such as color schemes, balance, or visual appeal.
Corrective Suggestions: Offer actionable steps to improve or correct any identified issues in the image.
Contextual Adaptation: Tailor feedback based on the type of image and the user’s goals, whether it’s for design, documentation, or other purposes.

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
# Modify the file uploader to accept video formats as well
uploaded_file = st.file_uploader(
    "Upload an image, video, or document", 
    type=["png", "jpg", "jpeg", "pdf", "doc", "docx", "txt", "mp4", "avi", "mov", "mkv", "webm"]
)
submit_button = st.button("Submit")

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None


# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# If the user uploads an image
# Store the image in session state
if uploaded_file and submit_button:
    # Process the uploaded image
    file_data = uploaded_file.getvalue()
    st.session_state["uploaded_file"] = file_data  # Save image to session state
    uploaded = st.session_state["uploaded_file"]
    if uploaded_file.type.startswith("image/"):
        # Convert the image data to base64 for Markdown display
        image_b64 = base64.b64encode(file_data).decode("utf-8")
        image_md = f"![User Image](data:{uploaded_file.type};base64,{image_b64})"
        # Add the image to chat history as a user message
        st.session_state["chat_history"].append({"role": "user", "content": image_md, "file_data": file_data})
        # Display the image
        st.image(file_data, width=350)

    elif uploaded_file.type.startswith("video/"):
        # Display the video directly in Streamlit
        st.session_state["chat_history"].append({"role": "user", "content": "User uploaded a video.", "file_data": file_data})
        st.video(file_data)

    else:
        # Display other file types
        st.session_state["chat_history"].append({"role": "user", "content": f"Uploaded a file of type {uploaded_file.type}", "file_data": file_data})
        st.write(f"Uploaded a file of type: {uploaded_file.type}")

    # Define the file as a part of the prompt
    file_parts = [{"mime_type": uploaded_file.type, "data": file_data}]
    
    # Combine the system prompt and file data
    prompt_parts = [file_parts[0], system_prompt]

    # Generate content based on the file and system prompt
    response = generate_ai_response(prompt_parts)
    st.session_state["chat_history"].append({"role": "assistant", "content": response.text})

# Display the conversation with styled chat bubbles
for message in st.session_state["chat_history"]:
    if message["role"] == "user":
        if "file_data" in message:
            if message["content"].startswith("![User Image]"):
                st.markdown(f"""
                <div class="message-container user">
                    <div class="user-bubble">
                """, unsafe_allow_html=True)
                # Use st.image to display the image
                st.image(message["file_data"], width=350)
                st.markdown(f"""
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.video(message["file_data"])
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
            image_parts = [{"mime_type": uploaded_file.type, "data": st.session_state["uploaded_file"]}]
            prompt_parts = [file_parts[0], user_message]
        else:
            prompt_parts = [user_message]

        # Generate response from the AI
        chat_response = generate_ai_response(prompt_parts)

        # Check if the response contains valid text parts
        if chat_response and hasattr(chat_response, 'text'):
            # Add the AI response to the chat history
            st.session_state["chat_history"].append({"role": "assistant", "content": chat_response.text})
        else:
            # Handle the case where the response is invalid or blocked
            st.session_state["chat_history"].append({"role": "assistant", "content": "Sorry, I couldn't generate a response."})


        # Update the page to reflect the new chat state
        st.rerun()  # If rerun isn't available, you can remove this line
