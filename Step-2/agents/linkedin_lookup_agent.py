from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools.tools import get_profile_url_tavily
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

def lookup(name: str) -> str:
    # llm = ChatOpenAI(
    #     temperature=0,
    #     model_name="gpt-3.5-turbo",
    # )
    # template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
    #                           Your answer should contain only a URL"""

    llm = Ollama(model="llama3", base_url="http://192.168.1.17:11434")
    template = """Given a query like a name or title (e.g. {name_of_person}), return only a LinkedIn profile URL that best matches it.
                        Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    # result = agent_executor.invoke(
    #     input={"input": prompt_template.format_prompt(name_of_person=name)}
    # )

    formatted_input = template.format(name_of_person=name)
    result = agent_executor.invoke({"input": formatted_input})

    linked_profile_url = result["output"]
    return linked_profile_url
