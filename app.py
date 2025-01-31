#The plan is to use all the specific models and integrate them with langchain.
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

#import prompt templates

from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, ChatPromptTemplate

#add some CSS styles! taken from DeepSeek itself
# Custom CSS styling
st.markdown("""
<style>
    /* Existing styles */
    .main {
        background-color: #121212;  /* Darker background */
        color: #e0e0e0;  /* Lighter text color */
    }
    .sidebar .sidebar-content {
        background-color: #1e1e1e;  /* Slightly lighter sidebar */
    }
    .stTextInput textarea {
        color: #ffffff !important;  /* White text in text input */
        background-color: #2a2a2a !important;  /* Dark background for text input */
    }
    
    /* Styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;  /* White text */
        background-color: #4a4a4a !important;  /* Darker background */
        border: 1px solid #ffffff;  /* White border */
        border-radius: 5px;  /* Rounded corners */
    }
    
    .stSelectbox svg {
        fill: #ffffff !important;  /* White icon */
    }
    
    .stSelectbox option {
        background-color: #3d3d3d !important;  /* Darker option background */
        color: #ffffff !important;  /* White option text */
    }
    
    /* For dropdown menu items */
    div[role="listbox"] div {
        background-color: #3d3d3d !important;  /* Darker dropdown items */
        color: #ffffff !important;  /* White text */
    }

    /* Hover effects for dropdown items */
    div[role="listbox"] div:hover {
        background-color: #5a5a5a !important;  /* Lighter background on hover */
    }

    /* Styling for buttons */
    .stButton > button {
        background-color: #007bff;  /* Blue background for buttons */
        color: white;  /* White text */
        border: none;  /* No border */
        border-radius: 5px;  /* Rounded corners */
        padding: 10px 20px;  /* Padding */
    }

    .stButton > button:hover {
        background-color: #0056b3;  /* Darker blue on hover */
    }
</style>
""", unsafe_allow_html=True)

st.title('DeepSeek Code Companion!')
st.caption ('I Have Debugging Superpowers to Help You!')

#sidebar configuration
# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model Selection
    st.markdown("### Select Your Model")
    selected_model = st.selectbox(
        "Choose a Model:",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],
        index=0,
        format_func=lambda x: f"🔍 {x}"  # Adding an icon to the model names
    )
    
    st.divider()
    
    # Model Capabilities Section
    st.markdown("### Model Capabilities")
    st.markdown("""
    Here are some of the capabilities of the selected model:
    - 🐍 **Python Expert**: Provides insights and solutions for Python programming.
    - 🐞 **Debugging Assistant**: Helps identify and fix bugs in your code.
    - 📝 **Code Documentation**: Assists in generating and improving code documentation.
    - 💡 **Solution Design**: Offers design patterns and architectural guidance.
    """)
    
    st.divider()
    
    # Additional Information
    st.markdown("### Learn More")
    st.markdown("""
    This application is built with:
    - [Ollama](https://ollama.ai/) - A powerful tool for AI model management.
    - [LangChain](https://python.langchain.com/) - A framework for developing applications powered by language models.
    """)
    
    # Optional: Add a footer or contact information
    st.markdown("---")
    st.markdown("👤 Developed by Palak Prashant")
    st.markdown("📧 Contact: palakprashant01@gmail.com")

#Create chat engine - initiate the LLM engine to use chat Ollama
llm_engine = ChatOllama(
    model = selected_model,
    base_url = "http://localhost:11434",
    temperature=0.3
    )

#Provide system prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
        "You are an expert AI coding assistant. Please provide concise and correct solutions with strategic print statements for debugging. Always respond in English."
    )

#Manage the state of session
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today? :)"}]
    
#Create chat container
chat_container = st.container()

#Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

#Chat input and processing
user_query = st.chat_input("Type your coding question here")

#Create processing pipeline and then lcl expression
def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({}) #call all this chain in an order

#Take system prompt, update with respect to user, and return chat prompt template
def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

#whenever a user chat messages, we need to append with respect to role and content and build the prompt chain, build the Gen AI response, and append to message log

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    # Rerun to update chat display
    st.rerun()



