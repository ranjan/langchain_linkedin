from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

information = """
    Elon Reeve Musk (born June 28, 1971) is a businessman. He is known for his leadership of Tesla, SpaceX, X (formerly Twitter), and the Department of Government Efficiency (DOGE). Musk has been considered the wealthiest person in the world since 2021; as of May 2025, Forbes estimates his net worth to be US$424.7 billion.

    Born to a wealthy family in Pretoria, South Africa, Musk emigrated in 1989 to Canada. He received bachelor's degrees from the University of Pennsylvania in 1997 before moving to California, United States, to pursue business ventures. In 1995, Musk co-founded the software company Zip2. Following its sale in 1999, he co-founded X.com, an online payment company that later merged to form PayPal, which was acquired by eBay in 2002. That year, Musk also became an American citizen.

    Neuralink has conducted animal testing on macaques at the University of California, Davis. In 2021, the company released a video in which a macaque played the video game Pong via a Neuralink implant. The company's animal trials—which have caused the deaths of some monkeys—have led to claims of animal cruelty. The Physicians Committee for Responsible Medicine has alleged that Neuralink violated the Animal Welfare Act.[163] Employees have complained that pressure from Musk to accelerate development has led to botched experiments and unnecessary animal deaths. In 2022, a federal probe was launched into possible animal welfare violations by Neuralink.

    In early 2017, Musk expressed interest in buying Twitter and had questioned the platform's commitment to freedom of speech. By 2022, Musk had reached 9.2% stake in the company,[177] making him the largest shareholder. Musk later agreed to a deal that would appoint him to Twitter's board of directors and prohibit him from acquiring more than 14.9% of the company. Days later, Musk made a $43 billion offer to buy Twitter. By the end of April Musk had successfully concluded his bid for approximately $44 billion.[183] This included approximately $12.5 billion in loans and $21 billion in equity financing. Having back tracked on his initial decision, Musk bought the company on October 27, 2022.[187]

    Immediately after the acquisition, Musk fired several top Twitter executives including CEO Parag Agrawal; Musk became the CEO instead.[189] Under Elon Musk, Twitter instituted monthly subscriptions for a "blue check", and laid off a significant portion of the company's staff.[193][194] Musk lessened content moderation and hate speech also increased on the platform after his takeover. In late 2022, Musk released internal documents relating to Twitter's moderation of Hunter Biden's laptop controversy in the lead-up to the 2020 presidential election. Musk also promised to step down as CEO after a Twitter poll, and five months later, Musk stepped down as CEO and transitioned his role to executive chairman and chief technology officer (CTO).[202]

    Despite Musk stepping down as CEO, X continues to struggle with challenges such as viral misinformation, hate speech, and antisemitism controversies. Musk has been accused of trying to silence some of his critics[206] by removing their accounts' blue checkmarks, which hinders visibility and is considered a form of shadow banning,[207][208] or suspending their accounts without justification.

    Musk supported Barack Obama in 2008 and 2012, Hillary Clinton in 2016, Joe Biden in 2020,[245] and Donald Trump in 2024.[246] In the 2020 Democratic Party presidential primaries, Musk endorsed candidate Andrew Yang and expressed support for Yang's proposed universal basic income,[247] and endorsed Kanye West's 2020 presidential campaign.[248] In 2021, Musk publicly expressed opposition to the Build Back Better Act, a $3.5 trillion legislative package endorsed by Joe Biden that ultimately failed to pass due to unanimous opposition from congressional Republicans and several Democrats. In 2022, Musk said he would start supporting Republican Party candidates, and gave over $50 million to Citizens for Sanity, a conservative political action committee.[251] In 2023, he supported Republican Ron DeSantis for the 2024 U.S. presidential election, giving $10 million to his campaign, and hosted DeSantis's campaign announcement on a Twitter Spaces event. From June 2023 to January 2024, Musk hosted a bipartisan set of X Spaces with Republican and Democratic candidates, including Robert F. Kennedy Jr., Vivek Ramaswamy, and Dean Phillips.
"""

if __name__ == "__main__":
    load_dotenv()
    print(" Hello Ranjank ")
    print(os.environ['COOL_API_KEY'])
    print(os.environ['OPENAI_API_KEY'])

    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting fact about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables="information", template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    # llm = ChatOllama(model="llama3")
    chain = summary_prompt_template | llm
    res = chain.invoke(input={"information": information})
    print(res)
