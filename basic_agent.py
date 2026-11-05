from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()  # Load environment variables from a .env file if present.

def get_genai_response(dev_prompt, user_prompt):
    client = OpenAI()
    conversation = [
        {
            "role": "developer",
            "content": dev_prompt,
        }
    ]

    
    conversation.append({"role": "user", "content": user_prompt})
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=conversation,
    )
    answer = response.output_text
    return answer


