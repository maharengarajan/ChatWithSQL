from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from urllib.parse import quote
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

llm=ChatGroq(api_key=GROQ_API_KEY,model="Llama3-8b-8192",streaming=True)


def connectDatabase(username, port, host, password, database):
    encoded_password = quote(password)
    mysql_uri = f"mysql+mysqlconnector://{username}:{encoded_password}@{host}:{port}/{database}" 
    db = SQLDatabase(create_engine(mysql_uri))
    return db

def generate_response(db,query_text,llm):
    toolkit=SQLDatabaseToolkit(db=db,llm=llm)

    agent=create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    response=agent.invoke(query_text)
    return response



if __name__=="__main__":
    db=connectDatabase(username="root",host="localhost",port=3306,password="M18ara10@",database="chatbot")
    query_text="Tell me the available table names?"
    response=generate_response(db=db,query_text=query_text)
    print(response)