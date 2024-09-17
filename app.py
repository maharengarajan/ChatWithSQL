import streamlit as st
from langchain_groq import ChatGroq
from main import connectDatabase,generate_response

# Initialize Streamlit app
st.title("Conversational SQL Query Agent")

# Sidebar for user inputs
with st.sidebar:
    st.header("Database Connection")
    
    # Host, port, username, password, and API key inputs from user
    host = st.text_input("Host", value="localhost")
    port = st.number_input("Port", value=3306)
    username = st.text_input("Username", value="root")
    password = st.text_input("Password", type="password")
    database = st.text_input("Database", value="chatbot")
    
    st.header("Groq API Key")
    groq_api_key = st.text_input("GROQ API Key", type="password")
    
    # Button to connect to the database and initialize LLM
    if st.button("Connect and Initialize"):
        # Save inputs to session state
        st.session_state.host = host
        st.session_state.port = port
        st.session_state.username = username
        st.session_state.password = password
        st.session_state.database = database
        st.session_state.groq_api_key = groq_api_key

        # Initialize LLM
        st.session_state.llm = ChatGroq(api_key=groq_api_key, model="Llama3-8b-8192", streaming=True)
        
        # Connect to the database
        st.session_state.db = connectDatabase(
            username=username,
            port=port,
            host=host,
            password=password,
            database=database
        )
        
        st.success("Connected to the database and initialized the LLM!")

# Main area for user query input and responses
if "db" in st.session_state and "llm" in st.session_state:
    st.write("### Ask your SQL Query")
    
    # Input for the user to ask a SQL query
    query_text = st.text_input("Your Query", value="Tell me the available table names?")
    
    # Button to send the query
    if st.button("Run Query"):
        if query_text:
            # Generate a response from the LLM
            response = generate_response(
                db=st.session_state.db, 
                query_text=query_text, 
                llm=st.session_state.llm
            )
            
            # Store the conversation in session state for UI
            if "conversation" not in st.session_state:
                st.session_state.conversation = []
            
            # Append user query and response to the conversation
            st.session_state.conversation.append({"user": query_text, "assistant": response['output']})
        
    # Display conversation history
    if "conversation" in st.session_state:
        for entry in st.session_state.conversation:
            st.write(f"**User:** {entry['user']}")
            st.write(f"**Assistant:** {entry['assistant']}")
            st.write("---")
