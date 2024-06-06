#!/bin/bash

# Create project structure
mkdir -p gradio_project
cd gradio_project

# Create Python files
echo "import gradio as gr

def update_visibility(choice):
    return gr.Textbox.update(visible=(choice == 'Exa AI'), interactive=True)

def config_sidebar():
    with gr.Blocks() as config:
        with gr.Accordion('Configuration', open=False):
            with gr.Row():
                hf_api_key = gr.Textbox(label='Hugging Face API Key', placeholder='Enter your Hugging Face API Key')
                openai_api_key = gr.Textbox(label='OpenAI API Key', placeholder='Enter your OpenAI API Key')
                groq_api_key = gr.Textbox(label='Groq API Key', placeholder='Enter your Groq API Key')
            with gr.Row():
                model_choice = gr.Dropdown(choices=['Hugging Face', 'OpenAI', 'Groq'], label='Select Model')
            with gr.Row():
                search_engine = gr.Dropdown(choices=['DuckDuckGo', 'Exa AI'], label='Select Search Engine')
                exa_api_key = gr.Textbox(label='Exa AI API Key', placeholder='Enter your Exa AI API Key if you are using Exa', visible=True)
            search_engine.change(fn=update_visibility, inputs=search_engine, outputs=exa_api_key)
    return config, hf_api_key, openai_api_key, groq_api_key, model_choice, search_engine, exa_api_key" > config.py

echo "import gradio as gr
import openai

def chat_interface():
    def chat_response(message, history, system_prompt, tokens, api_key, model_choice):
        openai.api_key = api_key
        response = f'System prompt: {system_prompt}\nMessage: {message}.'
        for i in range(min(len(response), int(tokens))):
            yield response[:i + 1]

    with gr.Blocks() as chat:
        system_prompt = gr.Textbox('You are a helpful AI.', label='System Prompt')
        slider = gr.Slider(10, 100, label='Tokens')
        chat_interface = gr.ChatInterface(
            chat_response,
            additional_inputs=[system_prompt, slider]
        )
    return chat, system_prompt, slider, chat_interface" > chat.py

echo "import gradio as gr

def data_storage():
    with gr.Blocks() as data:
        collected_data = gr.Textbox(label='Collected Data', placeholder='Data will be displayed here')
    return data, collected_data" > data_storage.py

echo "import gradio as gr
from config import config_sidebar
from chat import chat_interface
from data_storage import data_storage

def main():
    config, hf_api_key, openai_api_key, groq_api_key, model_choice, search_engine, exa_api_key = config_sidebar()
    chat, system_prompt, slider, chat_interface = chat_interface()
    data, collected_data = data_storage()

    with gr.Blocks() as demo:
        config.render()
        chat.render()
        data.render()

    demo.launch()

if __name__ == '__main__':
    main()" > app.py

# Create requirements.txt
echo "gradio
openai" > requirements.txt

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py