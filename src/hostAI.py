from openai import OpenAI
import sys, os

# # Try to load the API key from an environment variable first
# openai_key = os.getenv('OPENAI_API_KEY')

# # If the API key is not set in the environment, try to import it from config.py
# if not openai_key:
#     try:
#         print("didn't get the environment variable")
#         sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#         import config
#         openai_key = config.OPENAI_KEY
#     except ImportError:
#         pass

# if not openai_key:
#     raise EnvironmentError("API key not found. Set the OPENAI_API_KEY environment variable or provide it in a config.py file.")

# client = OpenAI(
# api_key = openai_key
# )

# def chatbot(prompt): # example usage of GPT (in terminal)
#     response = client.chat.completions.create(
#         messages=[{"role":"user", "content":prompt}],
#         model="gpt-3.5-turbo",
#     )
#     return response.choices[0].message.content.strip()

def get_commentary(q, ans, is_correct, streak):
   """
   q (str): The current question that user just answered
   ans (str): Answer to corresponding question, q.
   is_correct (bool): True if user answered correctly, False o.w.
   streak (int): Represents the number of q's the user has answered <is_correct>
   """

   if is_correct:
       return f'to {q['question']} you answered {ans} and you are correct! your streak is {streak}'
   else:
       return f'to {q['question']}. you are incorrect :( the correct answer was {ans}. your streak is {streak}'

#    correctness = "right" if is_correct else "wrong"
#    correctness2 = "correctly" if correctness=="right" else "incorrectly"

#    context = f"""Chat, you are a gameshow host tasked with providing short, 
#    personalized commentary/feedback after every question a player answers right
#    or wrong. There are 10 questions in the game: the user was tasked with answering 
#    the question: {q} and got it {correctness}. This is question {streak} in a row that 
#    the contestant has picked {correctness2}. Your first sentence is short, revealing whether
#    the player answered correctly, along with short context about the right answer. The
#    second sentence is short words of encouragement based on their streak. You should
#    simulate a direct communication with the player."""

#    response = client.chat.completions.create(
#         messages=[{"role":"user", "content":context}],
#         model="gpt-3.5-turbo",
#     )
#    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower() in ["quit", "exit", "bye"]:
    #         break
    #     response = chatbot(user_input)
    #     print("Chatbot: ", response)
    
    # q = "What color is a polar bear's skin?"
    # ans = "Black"
    # is_correct = True
    # streak = 4
    # print(get_commentary(q, ans, is_correct, streak))
    pass