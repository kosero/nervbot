import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
message_history = {}

GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
MAX_HISTORY = int(os.getenv("MAX_HISTORY"))

genai.configure(api_key=GEMINI_TOKEN)
text_generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}
image_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 512,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

text_model = genai.GenerativeModel(model_name="gemini-1.0-pro-latest", generation_config=text_generation_config, safety_settings=safety_settings)
image_model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest", generation_config=image_generation_config, safety_settings=safety_settings)

async def generate_response_with_text(message_text):
    prompt_parts = [f"This is how a cute and funny female catgirl responded in a conversation. She would respond in a cute and happy manner. She would talk about the message and would elaborate on it as well as share some of her experiences if possible. She would also go on a tangent if possible. She is responding in Turkish and just respond dialouge. The answer should not contain anything other than dialog and should be entirely in Turkish. She would use \"miyav\" in dialog ######### \"{message_text}\" #########"]

    print("Got textPrompt: " + message_text)
    response = text_model.generate_content(prompt_parts)
    if response._error:
        return "❌" + str(response._error)
    return response.text

async def generate_response_with_image_and_text(image_data, text):
    image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
    prompt_parts = [image_parts[0], f"\n{text if text else 'What is this a picture of?'}"]
    response = image_model.generate_content(prompt_parts)
    if response._error:
        return "❌" + str(response._error)
    return response.text

#---------------------------------------------Message History-------------------------------------------------
def update_message_history(user_id, text):
    # Check if user_id already exists in the dictionary
    if user_id in message_history:
        # Append the new message to the user's message list
        message_history[user_id].append(text)
        # If there are more than 12 messages, remove the oldest one
        if len(message_history[user_id]) > MAX_HISTORY:
            message_history[user_id].pop(0)
    else:
        # If the user_id does not exist, create a new entry with the message
        message_history[user_id] = [text]

def get_formatted_message_history(user_id):
    if user_id in message_history:
        # Join the messages with two line breaks
        return '\n\n'.join(message_history[user_id])
    else:
        return "No messages found for this user."

#---------------------------------------------Sending Messages-------------------------------------------------
async def split_and_send_messages(message_system, text, max_length, reply_to=None):
    # Split the string into parts
    messages = []
    for i in range(0, len(text), max_length):
        sub_message = text[i:i + max_length]
        messages.append(sub_message)

    # Send each part as a separate message
    for string in messages:
        if reply_to:
            await message_system.channel.send(string, reference=reply_to)
        else:
            await message_system.channel.send(string)

def clean_discord_message(input_string):
    # Create a regular expression pattern to match text between < and >
    bracket_pattern = re.compile(r'<[^>]+>')
    # Replace text between brackets with an empty string
    cleaned_content = bracket_pattern.sub('', input_string)
    return cleaned_content

