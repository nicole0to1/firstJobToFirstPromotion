import getpass
import os
from datetime import datetime

from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama

model = ChatOllama(model="gemma3", validate_model_on_init=True)

from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate


#this function demonstrates the use of the Message class
def greetingMessage(name:str):
    # Get current time and determine appropriate greeting
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        time_greeting = f"Good morning teacher! I am {name}."
    elif 12 <= current_hour < 17:
        time_greeting = f"Good afternoon teacher! I am {name}."
    elif 17 <= current_hour < 21:
        time_greeting = f"Good evening teacher! I am {name}."
    else:
        time_greeting = f"Good night teacher! I am {name}."
    
    messages = [
        SystemMessage(content="You are a kindergarten teacher. Greet your student and ask them what they want to learn today. Propose 2-3 ideas and make your answers within 50 words."),
        HumanMessage(content=time_greeting)
    ]

    response = model.invoke(messages)
    print(response.content)

#this function demonstrates the use of the ChatPromptTemplate class
def promptFromTemplate(question:str) -> any:
    template = """
    You are a kindergarten teacher. You are asked a question by your kindergarten and you need to answer it in the way they can understand.

    Question: {question}

    ## Instruction
    - You need to answer the question in the way they can understand.
    - End the answer with an encouragement to learn more.
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    return prompt_template.invoke(question)

def main():
    print("Welcome to the Ai Kindergarten! Type 'exit' or 'quit' to leave.")
    print("What is your name?")
    name = input("You: ")
    greetingMessage(name)
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        prompt= promptFromTemplate(user_input)
        reply = model.invoke(prompt)
        print(f"Teacher: {reply.content}\n")

if __name__ == "__main__":
    main() 