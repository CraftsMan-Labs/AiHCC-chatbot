import gradio as gr
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
    return chat, system_prompt, slider, chat_interface
