import os
import gradio as gr

def config_sidebar():
    with gr.Blocks() as config:
        with gr.Accordion('Configuration', open=False):
            with gr.Row():
                openai_api_key = gr.Textbox(label='OpenAI API Key', placeholder='Enter your OpenAI API Key')
    os.environ['OPENAI_API_KEY'] = openai_api_key
    return config, openai_api_key