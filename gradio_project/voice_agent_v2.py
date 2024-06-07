import gradio as gr
import json
from persona_prompt.system_prompt import system_prompt
from tools import search_internet, ask_about_our_projects, send_email, ask_questions_based_on_role, tools_list
from dotenv import load_dotenv
from openai import OpenAI
import openai
from pathlib import Path
from io import BytesIO
import base64

load_dotenv()

client = OpenAI()

class consultant_bot(object):
    def __init__(self):
        self.model_name = 'gpt-4o'
        self.temperature = 0.8
        self.system_prompt = system_prompt
        self.tools = tools_list

    def chat(self, user_input, chat_history):
        bot_chat_history = []
        bot_chat_history.append({
            "role": "system",
            "content": self.system_prompt
        })
        for chat in chat_history:
            human_message = chat[0]
            ai_message = chat[1]
            bot_chat_history.append({
                "role": "user",
                "content": human_message
            })
            bot_chat_history.append({
                "role": "assistant",
                "content": ai_message
            })

        bot_chat_history.append({
            "role": "user",
            "content": user_input
        })
        print("bot_chat_history: ", bot_chat_history)
        completion = client.chat.completions.create(
            model=self.model_name,
            messages=bot_chat_history,
            temperature=self.temperature,
            functions=self.tools,
            function_call='auto'
        )
        response = completion.choices[0].message.content
        print("Entire response: ", completion)
        # check for function call
        if completion.choices[0].message.function_call is not None:
            print("function_call: ", completion.choices[0].message.function_call.name)
            arguments = completion.choices[0].message.function_call.arguments
            arguments = json.loads(arguments)
            if completion.choices[0].message.function_call.name == 'search_internet':
                response = search_internet(arguments['query'])
            elif completion.choices[0].message.function_call.name == 'ask_about_our_projects':
                response = ask_about_our_projects(arguments['query'])
            elif completion.choices[0].message.function_call.name == 'send_email':
                response = send_email(arguments['email_id'], arguments['email_sub'], arguments['email_body'])
            elif completion.choices[0].message.function_call.name == 'ask_questions_based_on_role':
                response = ask_questions_based_on_role(arguments['role'])

            # add the response to chat history
            print("tool_response: ", response)
            bot_chat_history.append({
                "role": "assistant",
                "content": f"Tool response: {response} Create a new message to continue the conversation to help the user. Remember you are Piper, an AI SDR."
            })
            # generate a suitable response
            completion = client.chat.completions.create(
                model=self.model_name,
                messages=bot_chat_history,
                temperature=self.temperature
            )
            response = completion.choices[0].message.content
        if not response:
            response = ""
        print("response: ", response)
        return response

    def text_to_speech(self, text, voice="alloy"):
        speech_file_path = Path(__file__).parent / "response.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)
        return str(speech_file_path)

    def generate_audio_html(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_bytes = BytesIO(audio_file.read())
        audio_base64 = base64.b64encode(audio_bytes.read()).decode("utf-8")
        audio_html = f'<audio src="data:audio/mpeg;base64,{audio_base64}" controls autoplay></audio>'
        return audio_html

bot = consultant_bot()

css = """
.gradio-container {
    height: 100vh !important;
    width: 100vw !important;
    display: flex;
    flex-direction: column;
}
#component-0 {
    flex-grow: 1;
    overflow: auto;
}
"""

def chat(message, chat_history):
    print("Human: ", message)
    print("chat_history: ", chat_history)
    ai_response = bot.chat(message, chat_history)
    print("AI: ", ai_response)
    audio_path = bot.text_to_speech(ai_response)
    print("Audio Path: ", audio_path)
    audio_html = bot.generate_audio_html(audio_path)
    return ai_response, audio_html

def transcribe(audio):
    print("Transcribing audio...:", audio)
    audio_file = open(audio, "rb")
    transcription = client.audio.transcriptions.create(model="whisper-1",
                                                       file=audio_file)
    print("Transcription: ", transcription)
    return transcription.text

with gr.Blocks(css=css) as demo:
    with gr.Row():
        audio_input = gr.Audio(sources="microphone", type="filepath", label="Speak to the AI")
        transcribed_text = gr.Textbox(label="Transcribed Text")
        submit_button = gr.Button("Submit")
    
    chat_history = gr.State([])

    def process_audio(audio, chat_history):
        transcribed_text = transcribe(audio)
        response, audio_html = chat(transcribed_text, chat_history)
        chat_history.append((transcribed_text, response))
        return transcribed_text, response, chat_history, audio_html

    submit_button.click(
        fn=process_audio,
        inputs=[audio_input, chat_history],
        outputs=[transcribed_text, gr.Textbox(label="AI Response"), chat_history, gr.HTML(label="AI Response Audio")]
    )

    buttons = gr.HTML(
        '''<a href='www.aihackerspace.com'>AI Hackerspace</a> 
        <a href="www.aihackerspace.com/schedule">Schedule a call</a>
        <a href="https://github.com/ruvnet">RuVs projects</a>''')

demo.launch(inline=False)