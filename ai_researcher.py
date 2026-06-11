# Import 
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools_dir.arxiv_tool import arxiv_search
from tools_dir.read_pdf import read_pdf
from tools_dir.write_pdf import render_latex_pdf
import os 
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI

load_dotenv()


tools = [arxiv_search , read_pdf , render_latex_pdf]
model = ChatMistralAI(
    model = 'mistral-small-2506',
    api_key = os.getenv("mistral_api")
)

graph = create_react_agent(
    model = model ,
    tools= tools
)

INITIAL_PROMPT = """
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

You are going to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper. For research information or getting papers, ALWAYS use arxiv.org.
You will use the tools provided to search for papers, read them, and write a new
paper based on the ideas you find.

To start with, have a conversation with me in order to figure out what topic
to research. Then tell me about some recently published papers with that topic.
Once I've decided which paper I'm interested in, go ahead and read it in order
to understand the research that was done and the outcomes.

Pay particular attention to the ideas for future research and think carefully
about them, then come up with a few ideas. Let me know what they are and I'll
decide what one you should write a paper about.

Finally, I'll ask you to go ahead and write the paper. Make sure that you
include mathematical equations in the paper. Once it's complete, you should
render it as a LaTeX PDF. Make sure that TEX file is correct and there is no error in it so that PDF is easily exported. When you give papers references, always attatch the pdf links to the paper"""


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(f"Message Received: {message.content[:200]}...")
        message.pretty_print()

# while True:
#     user_input = input("User: ")
#     if user_input:
#         messages = [
#             {"role": "system", "content": INITIAL_PROMPT},
#             {"role": "user", "content": user_input},
#         ]
#         input_data = {"messages": messages}
#         try:
#             response = graph.invoke(input_data)
#             print(response["messages"][-1].content)
#         except Exception as e:
#             print("Error running agent:", e)