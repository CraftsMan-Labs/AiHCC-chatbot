import streamlit as st
import json
from persona_prompt.system_prompt import system_prompt
from tools import search_internet, \
    ask_about_our_projects, \
    send_email, \
    ask_questions_based_on_role, \
    tools_list
from dotenv import load_dotenv
from openai import OpenAI

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
            print("function_call: ",
                  completion.choices[0].message.function_call.name)
            arguments = completion.choices[0].message.function_call.arguments
            arguments = json.loads(arguments)
            if completion.choices[0].message.function_call.name == 'search_internet':
                response = search_internet(arguments['query'])
            elif completion.choices[0].message.function_call.name == 'ask_about_our_projects':
                response = ask_about_our_projects(arguments['query'])
            elif completion.choices[0].message.function_call.name == 'send_email':
                response = send_email(
                    arguments['email_id'], arguments['email_sub'], arguments['email_body'])
            elif completion.choices[0].message.function_call.name == 'ask_questions_based_on_role':
                response = ask_questions_based_on_role(arguments['role'])

            # add the response to chat history
            print("tool_response: ", response)
            bot_chat_history.append({
                "role": "assistant",
                "content": f"Tool response: {response} Create a new message to continue the conversation to help the user. Remeber you are Piper, an AI SDR."
            })
            # generate a suitbal response
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


bot = consultant_bot()


def chat(message, chat_history):
    print("Human: ", message)
    print("chat_history: ", chat_history)
    ai_response = bot.chat(message, chat_history)
    print("AI: ", ai_response)
    return ai_response

st.title("Strategix")

st.markdown(
    """
    <a href='www.aihackerspace.com'>AI Hackerspace</a> 
    <a href="www.aihackerspace.com/schedule">Schedule a call</a>
    <a href="https://github.com/ruvnet">RuVs projects</a>
    """,
    unsafe_allow_html=True
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        st.session_state["chat_history"].append(("user", user_input))
        ai_response = chat(user_input, st.session_state["chat_history"])
        st.session_state["chat_history"].append(("assistant", ai_response))

if st.session_state["chat_history"]:
    for i, (role, message) in enumerate(st.session_state["chat_history"]):
        if role == "user":
            st.text(f"User: {message}")
        else:
            st.text(f"Assistant: {message}")
