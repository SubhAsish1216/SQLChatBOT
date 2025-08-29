import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from urllib.parse import quote_plus  # ✅ for encoding special characters in password
from langchain_openai import ChatOpenAI  # ✅ OpenAI model

# 🎨 Page Config with custom theme colors
st.set_page_config(page_title="🦜 LangChain: Chat with SQL DB", page_icon="🦜", layout="wide")

# 🌸 Custom CSS for ivory, pink, and white aesthetic
st.markdown(
    """
    <style>
    body {
        background-color: #fffdf7; /* soft ivory */
        color: #333;
    }
    .stApp {
        background: linear-gradient(180deg, #fffdf7 0%, #ffe4ec 100%); /* ivory → pink gradient */
    }
    .stSidebar {
        background-color: #fffafc !important; /* white-pink for sidebar */
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 12px;
        margin: 6px 0;
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #ffeef5;
        color: #333;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #f9f9f9;
        color: #111;
    }
    h1 {
        color: #ff4b8b !important;
        text-align: center;
        font-family: "Trebuchet MS", sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🦜 Title with emoji
st.title("🦜 LangChain: Chat with SQL DB 💬")

# 🌟 Cute motivational quote
st.markdown(
    "<p style='text-align:center; font-size:16px; color:#ff4b8b;'><i>✨ Ask your database like a friend — every query tells a story! ✨</i></p>",
    unsafe_allow_html=True
)

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = ["📘 Use SQLLite 3 Database - Student.db", "🗄️ Connect to your MySQL Database"]

selected_opt = st.sidebar.radio(label="💾 Choose the DB which you want to chat with 🧐", options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("🌐 Provide MySQL Host")
    mysql_user = st.sidebar.text_input("👤 MySQL User")
    mysql_password = st.sidebar.text_input("🔑 MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("📂 MySQL Database")
else:
    db_uri = LOCALDB

# 🔑 OpenAI API Key
api_key = st.sidebar.text_input(label="🔐 OpenAI API Key", type="password")

if not db_uri:
    st.info("⚠️ Please enter the database information and URI")

if not api_key:
    st.info("⚠️ Please add the OpenAI API key")

## LLM model (OpenAI)
llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4o-mini", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("❌ Please provide all MySQL connection details.")
            st.stop()
        # ✅ Encode password to handle special characters like @, #, !
        safe_password = quote_plus(mysql_password)
        return SQLDatabase(
            create_engine(f"mysql+mysqlconnector://{mysql_user}:{safe_password}@{mysql_host}/{mysql_db}")
        )

# Create DB connection
if db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

## Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False,  # ⛔ hide SQL queries from logs
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Session state messages
if "messages" not in st.session_state or st.sidebar.button("🧹 Clear chat history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "👋 Hey there! How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_query = st.chat_input(placeholder="💭 Ask anything from the database...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        response = agent.run(user_query)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
