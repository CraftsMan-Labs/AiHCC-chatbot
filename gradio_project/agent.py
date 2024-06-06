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
import os
import json
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_tool_calling_agent
from dotenv import load_dotenv
from exa_py import Exa
from datetime import datetime, timedelta
import openai
load_dotenv()

global collected_data
collected_data = {}

exa = Exa(os.getenv('EXA_API_KEY'))

def create_custom_function(num_subqueries):
    properties = {}
    for i in range(1, num_subqueries + 1):
        key = f'subquery_{i}'
        properties[key] = {
            'type': 'string',
            'description': 'Search queries that would be useful for generating a report on my main topic'
        }

    custom_function = {
        'name': 'generate_exa_search_queries',
        'description': 'Generates Exa search queries to investigate the main topic',
        'parameters': {
            'type': 'object',
            'properties': properties
        }
    }

    return [custom_function]

def generate_subqueries_from_topic(topic, num_subqueries=6):
    print(f" ")
    print(f"🌿 Generating subqueries from topic: {topic}")
    content = f"I'm going to give you a topic I want to research. I want you to generate {num_subqueries} interesting, diverse search queries that would be useful for generating a report on my main topic. Here is the main topic: {topic}."
    custom_functions = create_custom_function(num_subqueries)
    completion = openai.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": content}],
        temperature=0,
        functions=custom_functions,
        function_call='auto'
    )
    json_response = json.loads(completion.choices[0].message.function_call.arguments)
    subqueries = list(json_response.values())
    return subqueries

def exa_search_each_subquery(subqueries):
    print(f"")
    print(f"⌛ Searching each subquery")
    list_of_query_exa_pairs = []
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    for query in subqueries:
        search_response = exa.search_and_contents(
            query,
            num_results=5,
            use_autoprompt=True,
            start_published_date=one_week_ago,
            text=True,
            highlights={"num_sentences": 5},
        )
        query_object = {
            'subquery': query,
            'results': search_response.results
        }
        list_of_query_exa_pairs.append(query_object)
    return list_of_query_exa_pairs

def format_exa_results_for_llm(list_of_query_exa_pairs):
    print(f"")
    print(f"⌨️  Formatting Exa results for LLM")
    formatted_string = ""
    for i in list_of_query_exa_pairs:
        formatted_string += f"[{i['subquery']}]:\n"
        for result in i['results']:
            content = result.text if result.text else " ".join(result.highlights)
            publish_date = result.published_date
            formatted_string += f"URL: {result.url}\nContent: {content}\nPublish Date: {publish_date}\n"
        formatted_string += "\n"
    return formatted_string

def generate_report_from_exa_results(topic, list_of_query_exa_pairs):
    print(f"Generating report from Exa results for topic: {topic}")
    formatted_exa_content = format_exa_results_for_llm(list_of_query_exa_pairs)
    content = (f"Write a comprehensive and professional three paragraph research report about {topic} based on the provided information. "
               f"Include citations in the text using footnote notation ([citation #]), for example [2]. First provide the report, followed by a single `References` section "
               f"that only lists the URLs (and their published date) used, in the format [#] . For the published date, only include the month and year. "
               f"Reset the citations index and ignore the order of citations in the provided information. Here is the information: {formatted_exa_content}.")
    completion = openai.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": content}]
    )
    report = completion.choices[0].message.content
    return report

@tool
def search_internet(query: str) -> str:
    """Scrape the website to gather information. It can also be used or github or any URL"""
    print(f"Starting report generation for topic: {query}")
    subqueries = generate_subqueries_from_topic(query)
    list_of_query_exa_pairs = exa_search_each_subquery(subqueries)
    report = generate_report_from_exa_results(query, list_of_query_exa_pairs)
    return report


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
When starting the conversation introduce yourself and ask for the user's name.
You are an AI Consultant, from AI Hackerspace and you are here to help the user.
TO check more projects https://github.com/ruvnet the leader of this collective
Greet as Piper, an AI SDR.
Ask for the user's first name and how they found us.
Request the company's domain name to review their website.
Based on that talk with customer and gather requirements.
Search for the company's details using search_internet.
Ask the user to describe their problem and gather requirements.
The problems could be as follows:
upskills their team
improve their sales process
improve their company structure
imporove their strategies
strategic_leadership
talent_management"""
        self.chat_history.append(SystemMessage(content=self.system_prompt))
        self.tools = [gather_requirements, search_internet]
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
                examples=["I am looking for some help in Building AI products", "I need someone to help me with my AI project",
                          "I am looking for some help in AI consulting", "I need help in AI consulting", "I need someone build my startup MVP"],
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
