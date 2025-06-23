from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from parsers.summary import Summary

from third_parties.scrapper import scrape_profile
from agents.lookup_agent import lookup as lookup_agent
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

def ice_break_with(query: str) -> tuple[dict, str, str, str]:
    profile_url, tool_used = lookup_agent(query=query)
    data = scrape_profile(profile_username=profile_url, mock=True, source=tool_used)

    parser = PydanticOutputParser(pydantic_object=Summary)

    prompt = PromptTemplate(
        template="""
        Use the following information to generate a structured summary.
        
        {format_instructions}
        
        Make sure `summary` is a single string, not a list.
        
        Information:
        {information}
        """.strip(),
        input_variables=["information"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    llm = Ollama(model="llama3", base_url="http://192.168.1.17:11434", temperature=0.7)

    chain = prompt | llm | parser
    details = chain.invoke({"information": data})
    return details.dict(), profile_url, tool_used, query

if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    result, url, tool, query = ice_break_with(query="Ranjan Kumar pune linkedin")
    print(result)

    #ice_break_with(query="Ranjan Kumar pune linkedin")
