import gradio as gr

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
    return config, hf_api_key, openai_api_key, groq_api_key, model_choice, search_engine, exa_api_key
