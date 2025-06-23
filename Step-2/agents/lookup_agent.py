from dotenv import load_dotenv
load_dotenv()

import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

from langchain_community.llms import Ollama
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.tools import (
    get_profile_url_tavily,
    get_twitter_profile,
    get_github_profile
)
from langchain.prompts.prompt import PromptTemplate

def lookup(name: str) -> str:
    llm = Ollama(model="llama3", base_url="http://192.168.1.17:11434")

    # Strong ReAct-style prompt to guide LLM behavior
    template = """
    You are a helpful assistant that finds profile URLs.
    
    Given a name or search query: {query}, you must:
    1. Use the tool to search for the profile.
    2. Once a result is found, respond ONLY with:
    
    Final Answer: <profile-url>
    
    Do NOT say 'Action: None' or any extra commentary. Only use tools, and when you're confident, output the final answer.
    
    Query: {query}
    """.strip()

    prompt_template = PromptTemplate(
        template=template, input_variables=["query"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="Useful for finding a LinkedIn profile from a name or search phrase"
        ),
        Tool(
            name="Twitter User Lookup",
            func=get_twitter_profile,
            description="Fetches Twitter user info based on name"
        ),
        Tool(
            name="GitHub User Lookup",
            func=get_github_profile,
            description="Retrieves GitHub user info from a name or username"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
        handle_parsing_errors=True  # handles LLM formatting issues
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(query=name)}
    )

    # formatted_input = template.format(query=name)
    # result = agent_executor.invoke({"input": formatted_input})

    return result["output"]

