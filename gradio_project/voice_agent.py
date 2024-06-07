import os
import requests
import gradio as gr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def transcribe_audio(audio):
    if audio is None:
        return "Error: No audio file provided."

    url = "https://api.deepgram.com/v1/listen"
    api_key = os.getenv("DEEPGRAM_API_KEY")
    
    # Ensure the audio file has the correct extension
    if not audio.endswith('.wav'):
        new_audio_path = audio + '.wav'
        os.rename(audio, new_audio_path)
        audio = new_audio_path
    
    try:
        with open(audio, 'rb') as audio_file:
            audio_data = audio_file.read()
    except Exception as e:
        return f"Error: Unable to read audio file. {str(e)}"
    
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/wav"
    }
    
    response = requests.post(url, headers=headers, data=audio_data)
    
    if response.status_code == 200:
        result = response.json()
        transcription = result['results']['channels'][0]['alternatives'][0]['transcript']
        return transcription
    else:
        return "Error: Unable to transcribe audio."

# Define the chatbot interface
def chatbot(audio):
    transcription = transcribe_audio(audio)
    return f"Transcription: {transcription}"

# Create Gradio interface
interface = gr.Interface(
    fn=chatbot,
    inputs=gr.Audio(sources="microphone", type="filepath"),
    outputs="text",
    title="Deepgram Chatbot",
    description="Record your voice and interact with the chatbot using Deepgram's transcription service."
)

# Launch the interface
if __name__ == "__main__":
    interface.launch()