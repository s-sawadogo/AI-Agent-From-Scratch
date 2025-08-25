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

@tool
def full_calculator(a: float, b: float) -> str:
    """ Useful for performing basic arithmetic calculations with numbers"""
    text = input(" Which operation do you want to perform ?")
    print("Full Calculator tool has been called.")
    if text.lower() == "sum":
        a, b = map(float, input(" Enter two numbers separated by space: ").split())
        return f"The sum of {a} and {b} is {a + b}"
    elif text.lower() == "difference":
        a = float(input(" Enter the greater number: "))
        b = float(input(" Enter the smaller number: "))
        return f"The difference between {a} and {b} is {a - b}"
    elif text.lower() == "product":
        a = float(input(" Enter the first number: "))
        b = float(input(" Enter the second number: "))
        return f"The product of {a} and {b} is {a * b}"
    elif text.lower() == "quotient":
        a = float(input(" Enter the numerator: "))
        b = float(input(" Enter the denominator: "))
        return f"The quotient of {a} and {b} is {a / b if b != 0 else 'Division by zero error'}"

# Tool for greeting
@tool
def say_hello(name: str) -> str:
    """ Useful for greeting a user"""
    print("Greeting tool has been called.")
    return f"Hello, {name}, I hope you are well today!"


def main():
    model = ChatOpenAI(temperature=0) # no random model

    tools = [calculator, full_calculator, say_hello]
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