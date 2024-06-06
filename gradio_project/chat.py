import gradio as gr
import openai
import requests
import json

def chat_interface():
    def chat_response(message, history, api_key, model_choice):
        print(history)
        if not chat_history:
            intro_message = "Hi There! I am your talent acquisition specialist. How can I help you today?"
            chat_history = [intro_message]
        if model_choice == 'OpenAI':
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                "max_tokens": tokens,
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))
            print(response.json())

            if response.status_code == 200:
                result = response.json()
                output = result["choices"][0]["message"]["content"]
                for i in range(min(len(output), int(tokens))):
                    yield output[:i + 1]
            else:
                yield f"Error: {response.status_code} - {response.text}"
        elif model_choice == 'Hugging Face':
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=tokens,
                temperature=0.7
            )
            output = response.choices[0].message.content
            for i in range(min(len(output), int(tokens))):
                yield output[:i + 1]
        elif model_choice == 'Groq':
            pass

    with gr.Blocks() as chat:
        chat_interface = gr.ChatInterface(
            chat_response
        )
    return chat, chat_interface
