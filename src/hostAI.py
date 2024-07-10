from openai import OpenAI
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

client = OpenAI(
api_key = config.OPENAI_KEY
)

def chatbot(prompt):
    response = client.chat.completions.create(
        messages=[{"role":"user", "content":prompt}],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content.strip()

def question():
    pass

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        response = chatbot(user_input)
        print("Chatbot: ", response)