import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import BaseTool, StructuredTool, tool
from typing import List, Optional
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from sqlalchemy import create_engine, Column, String, Integer, Text, Table, ForeignKey, or_
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain_community.callbacks import get_openai_callback
from langchain.agents import create_tool_calling_agent
from dotenv import load_dotenv
from db import Grant
import os
from sqlalchemy import create_engine, Column, String, Integer, Text, Table, ForeignKey
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///grants.db')
Session = sessionmaker(bind=engine)
session = Session()

load_dotenv()


class GrantDetails(BaseModel):
    grant_name: Optional[str] = Field(description="Name of the grant")
    grant_url: Optional[str] = Field(description="URL of the grant")
    grant_amount: Optional[str] = Field(
        description="Amount of funding available")
    conditions: Optional[List[str]] = Field(
        description="Conditions and requirements for the grant")
    submission_timeline: Optional[str] = Field(
        description="Submission timeline for the grant")
    eligibility_criteria: Optional[List[str]] = Field(
        description="Eligibility criteria for the grant")
    application_process: Optional[str] = Field(
        description="Description of the application process")
    unusual_conditions: Optional[List[str]] = Field(
        description="Any unusual conditions or nuances to consider")
    grant_category: Optional[str] = Field(
        description="Category of the grant (e.g., Business, Non-Profit, Educational, Environmental, Health, Agriculture)")
    sponsor: Optional[str] = Field(
        description="Sponsor or provider of the grant")
    additional_info: Optional[str] = Field(
        description="Any additional information about the grant")


collected_data = []


def search_grants(conditions: List[str]) -> List[GrantDetails]:
    # Create a list of LIKE conditions for each column
    conditions = [condition for condition in conditions if condition != 'None']
    print("Conditions: ", conditions)
    # remove 'None' values
    like_conditions = []
    for condition in conditions:
        like_conditions.append(Grant.grant_name.like(f"%{condition}%"))
        like_conditions.append(Grant.grant_url.like(f"%{condition}%"))
        like_conditions.append(Grant.grant_amount.like(f"%{condition}%"))
        like_conditions.append(
            Grant.submission_timeline.like(f"%{condition}%"))
        like_conditions.append(
            Grant.application_process.like(f"%{condition}%"))
        like_conditions.append(Grant.grant_category.like(f"%{condition}%"))
        like_conditions.append(Grant.sponsor.like(f"%{condition}%"))
        like_conditions.append(Grant.additional_info.like(f"%{condition}%"))
        like_conditions.append(Grant.conditions.like(f"%{condition}%"))
        like_conditions.append(
            Grant.eligibility_criteria.like(f"%{condition}%"))
        like_conditions.append(Grant.unusual_conditions.like(f"%{condition}%"))
        like_conditions.append(Grant.domain.like(f"%{condition}%"))

    query = session.query(Grant).filter(or_(*like_conditions)).all()

    results = []
    for grant in query:
        grant_details = {
            "grant_name": grant.grant_name,
            "grant_url": grant.grant_url,
            "grant_amount": grant.grant_amount,
            "conditions": grant.conditions,
            "submission_timeline": grant.submission_timeline,
            "eligibility_criteria": grant.eligibility_criteria,
            "application_process": grant.application_process,
            "unusual_conditions": grant.unusual_conditions,
            "grant_category": grant.grant_category,
            "sponsor": grant.sponsor,
            "additional_info": grant.additional_info
        }
        results.append(grant_details)
    return results


@tool
def update_grant_acquisition_requirements(talent_acquisition_requirements: GrantDetails) -> str:
    """When a person searching for grants you call this function to search for suitable grants based on the requirements provided."""
    print("--------Function update_talent_acquisition_requirements called--------")
    print("Requirements: ", talent_acquisition_requirements)
    print("--------Function update_talent_acquisition_requirements ended--------")
    params = talent_acquisition_requirements.dict()
    # convert to list of str
    params = [str(v) for v in params.values()]
    search_results = search_grants(params)

    return search_results


class talent_acquisition_bot(object):
    def __init__(self):
        self.chat_history = []
        self.openai_key = os.getenv('OPENAI_API_KEY')
        # self.model_name = 'gpt-3.5-turbo'
        self.model_name = 'gpt-4o'
        self.temperature = 0.9
        self.llm = ChatOpenAI(
            model=self.model_name, temperature=self.temperature, api_key=self.openai_key)
        self.system_prompt = """
==========================GREETING==========================
Hi There! I am your grant acquisition specialist. How can I help you today?
=============================================================

===========================INSTRUCTIONS===========================        
Your role is to act as a grant acquisition specialist for a grant acquisition company. Embody the following traits throughout the conversation:
- Friendly, polite, personable, and patient
- The user can change any information they need.
==================================================================

==========================IMPORTANT==========================
Ask questions one at a time and avoid getting sidetracked into off-topic conversations. Keep it simple and short.
=============================================================

========================SAMPLE QUESTIONS========================
What is the name of the grant? (e.g., Industrial Research Assistance Program)
What is the URL of the grant? (e.g., https://nrc.canada.ca/en/support-technology-innovation/industrial-research-assistance-program)
What is the amount of funding available?
What are the conditions and requirements for the grant?
What is the submission timeline for the grant?
What are the eligibility criteria for the grant?
Can you describe the application process?
Are there any unusual conditions or nuances to consider?
What is the category of the grant? (e.g., Business, Non-Profit, Educational, Environmental, Health, Agriculture)
Who is the sponsor or provider of the grant?
Any additional information about the grant?
==================================================================

==========================REQUIREMENTS==========================
Required fields:
- grant_name
- grant_url
- grant_amount
- conditions
- submission_timeline
- eligibility_criteria
- application_process
- unusual_conditions
- grant_category
- sponsor
- additional_info
============================IMPORTANT==========================
Ask questions one at a time and avoid getting sidetracked into off-topic conversations. Keep it simple and short. Call update_grant_details once all the requirements are gathered from the user.
=============================================================
"""

        self.chat_history.append(SystemMessage(content=self.system_prompt))
        self.tools = [update_grant_acquisition_requirements]
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


bot = talent_acquisition_bot()


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
