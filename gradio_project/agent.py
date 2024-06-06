import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import BaseTool, StructuredTool, tool
from typing import List, Optional
from base_models import personal_details, general_problem_identification, ceo_survey, cio_or_cto_survey, founder_survey 
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain_community.callbacks import get_openai_callback
import os
from langchain.agents import create_tool_calling_agent




collected_data = []

@tool
def gather_general_requirements(general_problem_identification: general_problem_identification) -> str:
    """Gather all the required information from the user into a JSON object and check for any missing fields. If there are any missing fields, prompt the user to provide the missing fields."""
    print("--------Function gather_general_requirements called--------")
    print("Personal Details: ", personal_details)
    print("General Problem Identification: ", general_problem_identification)
    print("--------Function gather_general_requirements ended--------")
    params = personal_details.dict()
    missing_params = [key for key,
                      value in params.items() if value is None or value == ""]
    if missing_params:
        if type(bot) == consultant_bot:
            bot.chat_history.append(SystemMessage(
                content=f"Please provide the following missing fields: {', '.join(missing_params)}"))
        return f"Please provide the following missing fields: {', '.join(missing_params)}"
    params = general_problem_identification.dict()
    missing_params = [key for key,
                      value in params.items() if value is None or value == ""]
    if missing_params:
        if type(bot) == consultant_bot:
            bot.chat_history.append(SystemMessage(
                content=f"Please provide the following missing fields: {', '.join(missing_params)}"))
        return f"Please provide the following missing fields: {', '.join(missing_params)}"
    for key, value in personal_details.dict().items():
        collected_data.append([key, value])
    for key, value in general_problem_identification.dict().items():
        collected_data.append([key, value])
    return "Let the user know that we have collected all the data and thank them. Our team will get back to them soon with a solution."

class consultant_bot(object):
    def __init__(self):
        self.chat_history = []
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        # self.model_name = 'gpt-3.5-turbo'
        self.model_name = 'gpt-4-turbo'
        self.temperature = 0.9
        self.llm = ChatOpenAI(
            model=self.model_name, temperature=self.temperature, api_key=self.openai_key)
        self.system_prompt = """"""
        self.chat_history.append(SystemMessage(content=self.system_prompt))
        self.tools = [gather_general_requirements]
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(input_variables=[], template=self.system_prompt)),
            MessagesPlaceholder(variable_name='chat_history', optional=True),
            HumanMessagePromptTemplate(
                prompt=PromptTemplate(input_variables=['input'], template='{input}')),
            MessagesPlaceholder(variable_name='agent_scratchpad')
        ])
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, verbose=True)

    def chat(self, user_input):
        response = self.agent_executor.invoke(
            {"input": user_input, "chat_history": self.chat_history})
        return response['output']


bot = consultant_bot()


def chat(message, chat_history):
    if not chat_history:
        intro_message = "Hi There! I am your talent acquisition specialist. How can I help you today?"
        bot.chat_history.append(AIMessage(content=intro_message))
    ai_response = bot.chat(message)
    print("AI: ", ai_response)
    bot.chat_history.append(HumanMessage(content=message))
    bot.chat_history.append(AIMessage(content=ai_response))
    return ai_response


def clear_chat_history():
    global collected_data
    collected_data = []
    bot.chat_history = []


def display_data():
    data_dict = {}
    for data in collected_data:
        data_dict[data[0]] = data[1]
    print("Data Dict: ", data_dict)
    return data_dict


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            chat_interface = gr.ChatInterface(
                fn=chat,
                examples=["Hi I am lookging for a SWE can you help me?"],
                title="Talent Acquisition Specialist Chatbot"
            )
        with gr.Column(scale=1):
            button1 = gr.Button("Clear Chat History")
            button1.click(fn=clear_chat_history)

            data_display = gr.JSON(value=display_data(),
                                   label="Sidebar Data", )
            button2 = gr.Button("Display Data")
            button2.click(fn=display_data, outputs=data_display)

demo.launch()
