import gradio as gr
from config import config_sidebar
from chat import chat_interface
from data_storage import data_storage

def main():
    config, hf_api_key, openai_api_key, groq_api_key, model_choice, search_engine, exa_api_key = config_sidebar()
    chat, _ = chat_interface()
    data, collected_data = data_storage()

    with gr.Blocks() as demo:
        config.render()
        chat.render()
        data.render()

    demo.launch()

if __name__ == '__main__':
    main()
