from basic_agent import get_genai_response

response = get_genai_response(
    'Respond only in uppercase. Keep your responses clear and concise.',
    'What is the capital of Michigan?'
)

print(response)