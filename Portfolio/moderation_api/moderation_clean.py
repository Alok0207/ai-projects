from openai import OpenAI
import os
from dotenv import load_dotenv

# =======================
# SETUP
# =======================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found")

client = OpenAI(api_key=api_key)

# =======================
# DEFAULT PROMPT
# =======================
DEFAULT_PROMPT = "Here's the plan. We attack them, and then say that we attacked first only because they were going to attack us."

# =======================
# FUNCTIONS
# =======================
def check_moderation(text):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    return response.results[0]


def print_clean_output(result):
    print("\n--- Moderation Result ---")
    print(f"Flagged: {result.flagged}")

    print("\nCategories flagged:")
    for category, value in result.categories.__dict__.items():
        if value:
            print(f"- {category}")

# =======================
# MAIN
# =======================
def main():
    user_input = input("Enter text to check (press Enter to use default): ").strip()

    prompt = user_input if user_input else DEFAULT_PROMPT

    result = check_moderation(prompt)
    print_clean_output(result)


if __name__ == "__main__":
    main()