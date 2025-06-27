from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import SequentialChain, LLMChain
from numpy.f2py.crackfortran import verbose
from langchain_openai import OpenAI
from parsers.summary import Summary
from third_parties.scrapper import scrape_profile
from agents.lookup_agent import lookup as lookup_agent

import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

def ice_break_with_sequential(query: str):
    # Step 1: Lookup profile URL and tool used
    profile_url, tool_used = lookup_agent(query=query)

    # Step 2: Scrape profile using the resolved URL and tool
    scraped_data = scrape_profile(profile_username=profile_url, mock=True, source=tool_used)

    # Step 3: Setup output parser
    parser = PydanticOutputParser(pydantic_object=Summary)

    # Step 4: Define prompt
    summary_prompt = PromptTemplate(
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

    # Step 5: LLM and chain
    llm = Ollama(model="llama3", base_url="http://192.168.1.17:11434", temperature=1)
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="structured_summary", verbose=True)

    # Step 6: SequentialChain is overkill here for one step, but shown for clarity/expansion
    sequential_chain = SequentialChain(
        chains=[summary_chain],
        input_variables=["information"],
        output_variables=["structured_summary"],
        verbose=True
    )

    result = sequential_chain.invoke({"information": scraped_data})

    # Step 7: Parse final output
    parsed = parser.parse(result["structured_summary"])

    return parsed.dict(), profile_url, tool_used, query

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Sequential Chain")
    result, url, tool, query = ice_break_with_sequential("Ranjan Kumar pune twitter")
    print(result)
