import os
import sys
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
# from icebreak.tools.tool import get_profile_url_tevily
from langchain.tools import Tool

load_dotenv()


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]


def lookup(name) -> str:

    llm = ChatOpenAI(temperature=0)

    summary_temp = """Given a full name of a person: {name}. 
                        You have to search for that person's LinkedIn profile page.
                        Your answer should only contain URL of the linkedIn.
                        
                        Example: "https://www.linkedin.com/in/aryan-tyagi-3b57101b9/" """
    prompt_templete = PromptTemplate(
        template=summary_temp, input_variables=['name'])

    tools_for_agents = [
        Tool(
            name='Crawl Google 4 find linkedin profile',
            func=get_profile_url_tavily,
            description="Use it when you need to find URL for the linkedin profile"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm, tools=tools_for_agents, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agents, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_templete.format_prompt(name=name)}
    )

    linkedin_profile_URL = result['output']

    return linkedin_profile_URL


if __name__ == "__main__":
    linkedin_url = lookup(name="Aryan Tyagi drdo")
    print(linkedin_url)
