from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import streamlit as st


load_dotenv() # Load environment variables from .env file

# Let's define a calculator tool
@tool
def calculator(a: float, b: float) -> str:
    """ Useful for performing basic arithmetic calculations with numbers"""
    st.write("Calculator tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"


# Tool for greeting
@tool
def say_hello(name: str) -> str:
    """ Useful for greeting a user"""
    st.write("Greeting tool has been called.")
    return f"Hello, {name}, I hope you are well today!"


def main():
    ## Initialize the Streamlit app
    st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
    st.title("🤖 AI Assistant")
    
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Model + agent
    model = ChatOpenAI(temperature=0)  # deterministic model
    tools = [calculator, say_hello]
    agent_executor = create_react_agent(model, tools)

    st.markdown("## **Welcome! I'm your AI assistant. Type 'quit' to exit.**")
    st.markdown("## **You can ask me to perform calculations or chat with me.**")

    # Display chat history
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            st.markdown(f"**You:** {msg.content}")
        elif isinstance(msg, AIMessage):
            st.markdown(f"**Assistant:** {msg.content}")

    # User input
    user_input = st.text_input("You:", value="", key="user_input")
    btn = st.button("Submit !")

    if btn:
        if user_input.lower() == "quit":
            st.write("Goodbye!")
        else:
            # Save user message
            st.session_state.messages.append(HumanMessage(content=user_input))

            # Stream assistant response
            response_text = ""
            for chunk in agent_executor.stream({"messages": st.session_state.messages}):
                if "agent" in chunk and "messages" in chunk["agent"]:
                    for message in chunk["agent"]["messages"]:
                        response_text += message.content + " "

            # Save assistant message
            st.session_state.messages.append(AIMessage(content=response_text.strip()))

            # Force rerun to refresh chat display
            st.experimental_rerun()


if __name__ == "__main__":
    main()