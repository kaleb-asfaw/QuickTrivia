from openai import OpenAI
import os

openai_key = os.getenv('OPENAI_KEY')

if not openai_key:
    raise EnvironmentError("Environment variable for OpenAI key was not set")

client = OpenAI(
api_key = openai_key
)

def chatbot(prompt): # example usage of GPT (in terminal)
    response = client.chat.completions.create(
        messages=[{"role":"user", "content":prompt}],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content.strip()

def get_commentary(q, ans, is_correct, streak):
   """
   q (str): The current question that user just answered
   ans (str): Answer to corresponding question, q.
   is_correct (bool): True if user answered correctly, False o.w.
   streak (int): Represents the number of q's the user has answered <is_correct>
   """

   correctness = "right" if is_correct else "wrong"
   correctness2 = "correctly" if correctness=="right" else "incorrectly"

   context = f"""Chat, you are a gameshow host tasked with providing short, 
   personalized commentary/feedback after every question a player answers right
   or wrong. There are 10 questions in the game: the user was tasked with answering 
   the question: {q} and got it {correctness}. This is question {streak} in a row that 
   the contestant has picked {correctness2}. Your first sentence is short, revealing whether
   the player answered correctly, along with short context about the right answer. The
   second sentence is short words of encouragement based on their streak. You should
   simulate a direct communication with the player."""

   response = client.chat.completions.create(
        messages=[{"role":"user", "content":context}],
        model="gpt-3.5-turbo",
    )
   return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        response = chatbot(user_input)
        print("Chatbot: ", response)
    
    # q = "What color is a polar bear's skin?"
    # ans = "Black"
    # is_correct = True
    # streak = 4
    # print(get_commentary(q, ans, is_correct, streak))
    