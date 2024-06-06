import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import BaseTool, StructuredTool, tool
from typing import List, Optional
import os
import subprocess
from base_models import MergedSurvey
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain_community.callbacks import get_openai_callback
from langchain_core.pydantic_v1 import BaseModel, Field
from scrapegraphai.graphs import SmartScraperGraph, OmniScraperGraph
import os
import json
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_tool_calling_agent
from dotenv import load_dotenv

load_dotenv()

# subprocess.run(["pip", "install", "--upgrade", "scrapegraphai"])
subprocess.run(["apt", "install", "chromium-chromedriver"])
subprocess.run(["pip", "install", "nest_asyncio"])
subprocess.run(["playwright", "install"])

global collected_data
collected_data = {}


@tool
def scrape_website(domain: str) -> str:
    """Scrape the website to gather information. It can also be used or github or any URL"""
    graph_config = {
        "llm": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-3.5-turbo",
            "temperature": 0,
        },
        "verbose": False,
        "headless": False
    }
    smart_scraper_graph = SmartScraperGraph(
        prompt="List me all the details about this website like projects, products what they do customers with their descriptions.",
        source=domain,
        config=graph_config
    )
    result = smart_scraper_graph.run()
    output = json.dumps(result, indent=2)
    return output


@tool
def search_internet(query: str) -> str:
    """Scrape the website to gather information. It can also be used or github or any URL"""
    smart_scraper_graph = OmniScraperGraph(
        prompt=f"Search for user query in the internet: {query}",
        config=graph_config
    )
    result = smart_scraper_graph.run()
    output = json.dumps(result, indent=2)
    return output


@tool
def gather_requirements(general_problem_identification: MergedSurvey) -> str:
    """Gather all the required information from the user into a JSON object and check for any missing fields. If there are any missing fields, prompt the user to provide the missing fields."""
    for key, value in general_problem_identification.dict().items():
        # update if key os not present or key value is none
        if key not in collected_data or collected_data[key] is None:
            collected_data[key] = value
    return ""


class consultant_bot(object):
    def __init__(self):
        self.chat_history = []
        self.model_name = 'gpt-3.5-turbo'
        self.temperature = 0.9
        self.llm = ChatOpenAI(
            model=self.model_name, temperature=self.temperature)
        self.system_prompt = """Role: AI Consultant (Piper)
Introduction:
Greet as Piper, an AI SDR.
Ask for the user's first name and how they found us.
Request the company's domain name to review their website.
Search for the company's website using the scrape_domain tool.
Ask the user to describe their problem and gather requirements.
The problems could be as follows:
upskills their team
improve their sales process
improve their company structure
imporove their strategies
strategic_leadership
talent_management"""
        self.chat_history.append(SystemMessage(content=self.system_prompt))
        self.tools = [gather_requirements, scrape_website, search_internet]
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
    print(chat_history)
    if not chat_history:
        intro_message = "Hi There! I am your AI Consultant. How can I help you today?"
        bot.chat_history.append(AIMessage(content=intro_message))
    ai_response = bot.chat(message)
    print("AI: ", ai_response)
    bot.chat_history.append(HumanMessage(content=message))
    bot.chat_history.append(AIMessage(content=ai_response))
    return ai_response


def clear_chat_history():
    global collected_data
    collected_data = {}
    bot.chat_history = []


def display_data():
    return collected_data


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=3):
            chat_interface = gr.ChatInterface(
                fn=chat,
                examples=["I am looking for some help in Building AI products"],
                title="AI consultant chatbot",
            )
        with gr.Column(scale=1):
            button1 = gr.Button("Clear Chat History")
            button1.click(fn=clear_chat_history)

            data_display = gr.JSON(value=display_data(),
                                   label="Sidebar Data", )
            button2 = gr.Button("Display Data")
            button2.click(fn=display_data, outputs=data_display)

demo.launch()
