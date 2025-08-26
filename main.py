from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Let's define a calculator tool
@tool
def calculator(a: float, b: float) -> str:
    """ Useful for performing basic arithmetic calculations with numbers"""
    print("Calculator tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"


# Tool for greeting
@tool
def say_hello(name: str) -> str:
    """ Useful for greeting a user"""
    print("Greeting tool has been called.")
    return f"Hello, {name}, I hope you are well today!"


def main():
    model = ChatOpenAI(temperature=0) # no random model

    tools = [calculator, say_hello]
    agent_executor = create_react_agent(model, tools)

    print(f"Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print(f"You can ask me to perform calculations or chat with me.")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content= user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()