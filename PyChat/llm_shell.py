import os
import openai

# Read API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set.")
    exit(1)

openai.api_key = api_key

def ask_llm(prompt):
    try:
        response = openai.responses.create(
            model="gpt-4o",
            instructions="You are a general advisor",
            input=prompt
        )
        return response.output_text.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("Welcome to the LLM Shell! Type 'exit' or 'quit' to leave.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        reply = ask_llm(user_input)
        print(f"LLM: {reply}\n")

if __name__ == "__main__":
    main() 