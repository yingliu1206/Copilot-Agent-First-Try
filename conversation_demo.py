from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # Load environment variables from a .env file if present.

client = OpenAI()
conversation = [
	{
		"role": "developer",
		"content": "You are a helpful assistant. Keep your responses clear and concise.",
	}
]

print("Chatbot ready. Type 'quit' or 'exit' to end the conversation.")
while True:
	try:
		user_input = input("You: ").strip()
	except (EOFError, KeyboardInterrupt):
		print("\nGoodbye!")
		break

	if user_input.lower() in {"quit", "exit"}:
		print("Goodbye!")
		break
	if not user_input:
		continue

	conversation.append({"role": "user", "content": user_input})
	response = client.responses.create(
		model="gpt-4.1-mini",
		input=conversation,
	)
	answer = response.output_text
	print(f"Assistant: {answer}")
	conversation.append({"role": "assistant", "content": answer})


