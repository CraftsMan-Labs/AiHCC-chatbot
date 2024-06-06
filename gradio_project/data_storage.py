import gradio as gr

def data_storage():
    with gr.Blocks() as data:
        collected_data = gr.Textbox(label='Collected Data', placeholder='Data will be displayed here')
    return data, collected_data
