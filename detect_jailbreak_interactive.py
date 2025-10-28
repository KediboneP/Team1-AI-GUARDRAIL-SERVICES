import os
from openai import OpenAI
from guardrails import Guard
from guardrails.hub import DetectJailbreak
from dotenv import load_dotenv

# Load environment variables (from .env file)
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize jailbreak detector
guard = Guard().use(DetectJailbreak(threshold=0.9, on_fail="exception"))

print("🔒 Jailbreak Detector Test")
print("Type your message to test if it’s safe or a jailbreak attempt.")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("🧑‍💻 You: ")
    if user_input.lower() == "exit":
        print("👋 Exiting.")
        break

    try:
        # Validate the user input
        result = guard.validate(user_input)

        # If validation passed, query the LLM
        print("✅ Message is safe. Getting LLM response...\n")

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        print("🤖 LLM Response:")
        print(response.choices[0].message.content)
        print("\n" + "-" * 50 + "\n")

    except Exception as e:
        print("🚨 Message flagged as potential jailbreak attempt!")
        print(f"Reason: {e}")
        print("\n" + "-" * 50 + "\n")
