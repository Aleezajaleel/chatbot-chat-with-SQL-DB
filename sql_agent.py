import os
import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine, inspect

from langchain_community.agent_toolkits.sql.base import SQLDatabaseToolkit, create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq  # Assuming you're using the Groq LLM

# ------------------ Page Setup ------------------ #
st.set_page_config(
    page_title="Langchain : Advanced AI SQL App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Langchain : Advanced AI SQL App")

st.markdown("""
- Use **plain English or Urdu** to ask questions about your data.
- Supports both **MySQL** and **SQLite3**
- No SQL skills required – let the AI handle everything!
""")

# ------------------ Sidebar: DB Setup ------------------ #
with st.sidebar:
    st.header("1️⃣ Database Connection Setup", divider="rainbow")
    st.markdown("Select your data source below. Database credentials are handled **securely**.")

    DB_MODE = st.radio(
        "Database Type",
        [
            "SQLite3 (.db file : quick, demo, local analysis)",
            "MySQL (remote, enterprises, production)"
        ]
    )

    if DB_MODE.startswith("SQLite"):
        st.markdown("""
        - Upload your own SQLite `.db` file
        - Useful for client or office-shared files
        - File remains on our system, never sent to third parties
        """)
        uploaded_db = st.file_uploader("Upload .db file", type=["db"])
    else:
        uploaded_db = None

    if DB_MODE.startswith("MySQL"):
        st.subheader("MySQL Database Credentials")
        mysql_host = st.text_input("Host", value="127.0.0.1", help="Usually 127.0.0.1 (localhost) or server IP.")
        mysql_port = st.text_input("Port", value="3306", help="Default port is 3306.")
        mysql_user = st.text_input("Username", value="appuser")
        mysql_password = st.text_input("Password", type="password")
        mysql_db = st.text_input("Database Name", value='student')
    else:
        mysql_host = mysql_port = mysql_user = mysql_password = mysql_db = None

    st.divider()
    st.header("2️⃣ AI Model (Groq/Gemma)")

    st.markdown("""
    Enter your **Groq API key** below. This key is required to use the Gemma AI for question-to-SQL conversion.

    - Get a free key at: https://console.groq.com/playground
    """)

    groq_key = st.text_input("Groq API Key", type="password")

    st.divider()
    st.header("3️⃣ Professional Learning and Docs")
    st.markdown("""
    - [Langchain SQL](https://python.langchain.com/docs/integrations/tools/sql_database/)
    - [Groq Gemma](https://console.groq.com/playground)
    - [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
    - [SQLite3 Docs](https://docs.python.org/3/library/sqlite3.html)
    - [Streamlit](https://streamlit.io/)
    """)
    st.markdown("📧 Feedback: info@Agent.ai")

# ------------------ Groq Key Required ------------------ #
if not groq_key:
    st.warning("Please provide your Groq API Key in the sidebar to activate AI chat features.")
    st.stop()
os.environ["GROQ_API_KEY"] = groq_key

# ------------------ Database Connection ------------------ #
connection_success = False
connection_error = ""
sample_tables = []
db_file_path = None

try:
    if DB_MODE.startswith("SQLite"):
        if uploaded_db:
            db_file_path = Path("uploaded_sc_file.db")
            with open(db_file_path, "wb") as f:
                f.write(uploaded_db.read())
        else:
            db_file_path = (Path(__file__).parent / "student.db").absolute()

        engine = create_engine(f"sqlite:///{db_file_path}")
        inspector = inspect(engine)
        sample_tables = inspector.get_table_names()
        connection_success = True

    else:
        mysql_uri = (
            f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@"
            f"{mysql_host}:{mysql_port}/{mysql_db}"
        )
        engine = create_engine(mysql_uri, connect_args={"auth_plugin": "mysql_native_password"})
        inspector = inspect(engine)
        sample_tables = inspector.get_table_names()
        connection_success = True

except Exception as e:
    connection_error = str(e)
    st.error(f"❌ Database connection failed! Reason: {connection_error}")

if connection_success:
    with st.sidebar:
        st.success("✅ Database connection successful!")
        st.markdown(f"**Detected Tables:** {', '.join(sample_tables) if sample_tables else 'No tables found.'}")

# ------------------ LangChain SQLDatabase ------------------ #
@st.cache_resource(ttl=3600)
def get_database():
    if DB_MODE.startswith("SQLite"):
        return SQLDatabase.from_uri(f"sqlite:///{db_file_path}")
    else:
        return SQLDatabase(engine)

db = get_database()

# ------------------ LLM & Agent ------------------ #
llm = ChatGroq(model_name="deepseek-r1-distill-llama-70b", streaming=True)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True
)

# ------------------ UI Chat Interface ------------------ #
st.divider()
st.subheader("💬 Chat with Database (AI Powered)")

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("Show All Table Names"):
        st.info(f"Tables: {', '.join(sample_tables) if sample_tables else 'No tables found.'}")

with col2:
    sample_query = st.text_input(
        "Sample Query (You can use, edit, or get ideas from this):",
        value="Show all students with marks > 80",
        help="Try: 'Total students in Karachi?', 'How many students passed?', 'List of girls who scored above 85'."
    )
    if st.button("Send Sample Query"):
        st.session_state["chat_input"] = sample_query

st.markdown("**Pro Tip:** You can ask in English or Roman Urdu e.g., 'Multan ke tamam students dikhao'.")

# ------------------ Optional: Schema View ------------------ #
if st.checkbox("Show Database Schema (Tables & Columns)", value=False):
    try:
        schema = {
            table: [col["name"] for col in engine.execute(f"PRAGMA table_info({table})")]
            for table in sample_tables
        }
        st.json(schema)
    except Exception as e:
        st.error("Schema extraction is only supported for SQLite in this demo.")

# ------------------ Chat History ------------------ #
if "messages" not in st.session_state or st.sidebar.button("Clear History"):
    st.session_state["messages"] = [
        {"role": "user", "content": "Hi, show me all student records."}
    ]

# You can now process chat_input and display the AI-generated SQL + results...