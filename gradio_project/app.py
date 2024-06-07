import gradio as gr
from config import config_sidebar
from chat import chat_interface

def main():
    config, openai_api_key = config_sidebar()
    chat, _ = chat_interface()

    with gr.Blocks() as demo:
        config.render()
        chat.render()

    demo.launch()

if __name__ == '__main__':
    main()
