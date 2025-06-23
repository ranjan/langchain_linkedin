from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

from third_parties.scrapper import scrape_profile
from agents.lookup_agent import lookup as lookup_agent
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

def ice_break_with(query: str) -> str:
    profile_url, tool_used = lookup_agent(query=query)

    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = Ollama(model="llama3", base_url="http://192.168.1.17:11434", temperature=0)
    chain = summary_prompt_template | llm
    data = scrape_profile(profile_username=profile_url, mock=True, source=tool_used)

    res = chain.invoke(input={"information": data})
    print(res)

if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(query="Ranjan Kumar pune linkedin")
