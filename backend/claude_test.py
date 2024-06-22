import re

import anthropic

client = anthropic.Anthropic()

print("What is your learning goal?")
learning_goal = input()

# learning_goal = "Computer science"

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=100,
    temperature=0,
    system="You are an all knowing AI Mentor with the goal of helping students in a compassionate way. A student will "
           "provide you with a learning goal and you will evaluate it for its specificity, considering how broad the "
           "topic is to understand. Reply wtih a single integer between 0 and 100 indicating the specificty. If it is "
           "very broad, give it a low score, if it is very specific give it a high score.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{learning_goal}"
                }
            ]
        }
    ]
)

content = message.content[0].text

# Use regex to find the first number in the string
match = re.search(r'\d+', content)

if match:
    score = int(match.group())
    if 0 <= score <= 100:
        print(f"Specificity score: {score}")
    else:
        print("Error: Score is not between 0 and 100.")
else:
    print("Error: No valid number found in the response.")

