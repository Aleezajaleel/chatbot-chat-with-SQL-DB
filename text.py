import os
import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType

# Streamlit App Config
st.set_page_config(
    page_title="LangChain: Advanced AI SQL App",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 LangChain: Advanced AI SQL App (Professional Demo)")

# Sidebar: Database Selection
with st.sidebar:
    st.header("Database Connection Setup", divider="rainbow")
    st.markdown("Select your data source below. Database credentials are handled **securely**.")

    DB_MODE = st.radio(
        "Database Type",
        [
            "SQLite3 (.db file: quick, demo, local analysis)",
            "MySQL (remote, enterprise, production)"
        ]
    )

# SQLite Option
if DB_MODE.startswith("SQLite"):
    st.markdown("""
        - Upload your own SQLite `.db` file
        - Useful if you receive files from clients or offices
        - File remains local — never sent to any third party
    """)

    uploaded_db = st.file_uploader("Upload .db file", type=["db"])
    if uploaded_db:
        db_path = f"temp_{uploaded_db.name}"
        with open(db_path, "wb") as f:
            f.write(uploaded_db.getbuffer())
        st.success(f"✅ Database uploaded: {uploaded_db.name}")

        # Create SQLite connection
        engine = create_engine(f"sqlite:///{db_path}")
        db = SQLDatabase(engine)
        st.info("Connected to SQLite database successfully!")

# MySQL Option
elif DB_MODE.startswith("MySQL"):
    st.subheader("MySQL Connection Details")
    mysql_host = st.text_input("Host", placeholder="e.g. localhost or remote IP")
    mysql_user = st.text_input("Username")
    mysql_password = st.text_input("Password", type="password")
    mysql_db = st.text_input("Database Name")

    if st.button("Connect to MySQL"):
        try:
            engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
            db = SQLDatabase(engine)
            st.success("✅ Connected to MySQL database successfully!")
        except Exception as e:
            st.error(f"Connection failed: {e}")
else:
    st.warning("Please select a database type to proceed.")
