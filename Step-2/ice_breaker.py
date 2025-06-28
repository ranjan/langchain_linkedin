from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import SequentialChain, LLMChain

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

    # Step 4: Define prompt for structured summary
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

    # Step 5: Define prompt for LinkedIn-style headline
    headline_prompt = PromptTemplate(
        template="""
        Based on this summary, write a catchy professional LinkedIn headline:

        {structured_summary}
        """.strip(),
        input_variables=["structured_summary"]
    )

    # Step 6: Set up LLM and individual chains
    llm = Ollama(model="llama3", base_url="http://192.168.1.17:11434", temperature=1)

    # First chain: summary
    summary_chain = LLMChain(
        llm=llm,
        prompt=summary_prompt,
        output_key="structured_summary"
    )

    # Second chain: headline
    headline_chain = LLMChain(
        llm=llm,
        prompt=headline_prompt,
        output_key="headline"
    )

    # Define a SequentialChain that connects the two steps
    chain = SequentialChain(
        chains=[summary_chain, headline_chain],
        input_variables=["information"],
        output_variables=["structured_summary", "headline"],
        verbose=True
    )

    # Run the chain
    result = chain({"information": scraped_data})

    # Parse summary output with Pydantic
    parsed = parser.parse(result["structured_summary"])

    return parsed.dict(), profile_url, tool_used, query, result["headline"]

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Sequential Chain")
    result, url, tool, query, headline = ice_break_with_sequential("Ranjan Kumar pune linkedin")
    print("\nResult Summary:")
    print(result)
    print("\nLinkedIn Headline Suggestion:")
    print(headline)
