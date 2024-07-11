import os
from typing import Tuple
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agents import lookup as linkedin_lookup
from output_parser import summary_parser, Summary
from langchain.chains import LLMChain


def ice_breaker(name: str) -> Tuple[Summary, str]:
    linkedin_url = linkedin_lookup(name)
    information = scrape_linkedin_profile(linkedin_url)

    print(information)

    summary_template = """
        Given the LinkedIn Profile information {information} about a person. Create the following :-
        1- A short summary about that person (3-4 lines).
        2- Interesting facts about that person.

        \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=['information'], template=summary_template, partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    llm = ChatOpenAI(temperature=0)
    # chain = LLMChain(llm=llm, prompt= summary_prompt_template)
    chain = summary_prompt_template | llm | summary_parser

    res: Summary = chain.invoke(input={"information": information})
    return res, information.get('profile_pic_url')


if __name__ == "__main__":
    pass
