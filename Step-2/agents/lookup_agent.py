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


def lookup(query: str) -> tuple[str, str]:
    llm = Ollama(model="llama3", base_url="http://192.168.1.17:11434", temperature=0)
    # template = """
    # You are a helpful assistant that finds profile URLs.
    #
    # Given a name or search query: {query}, you must:
    # 1. Use the tool to search for the profile.
    # 2. Once a result is found, respond ONLY with:
    #
    # Final Answer: <profile-url>
    #
    # Do NOT say 'Action: None' or any extra commentary. Only use tools, and when you're confident, output the final answer.
    #
    # Query: {query}
    # """

    template = """given a search query {query} I want you to get it me a link to their profile url.
                              Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["query"]
    )

    tools_for_agent = [
        Tool(
            name="LinkedIn Finder",
            func=get_profile_url_tavily,
            description="Useful for finding a LinkedIn profile from a name or search phrase"
        ),
        Tool(
            name="Twitter Finder",
            func=get_twitter_profile,
            description="Fetches Twitter user info based on name"
        ),
        Tool(
            name="GitHub Finder",
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
        handle_parsing_errors=True,
        return_intermediate_steps=True,
        ** {
            "early_stopping_method": "generate",
        }
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(query=query)}
    )
    print("**********************************")
    print(result)
    output = result.get("output")
    steps = result.get("intermediate_steps", [])
    print(steps)
    print("**********************************")
    used_tool_name = None
    for action, _observation in steps:
        if hasattr(action, "tool"):
            used_tool_name = action.tool
            break

    return output, used_tool_name


