from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# =======================
# CONFIG
# =======================
MODEL_NAME = "gpt-4o-mini"
SYSTEM_PROMPT = "You are a helpful assistant."

MAX_TURNS = 3
SUMMARY_TRIGGER = 12

# =======================
# SETUP
# =======================
load_dotenv(find_dotenv())

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=api_key)

# =======================
# UTILITIES
# =======================
def get_project_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(script_dir)


def save_chat(messages):
    project_root = get_project_root()
    log_dir = os.path.join(project_root, "chat_logs")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"chat_{timestamp}.txt"
    file_path = os.path.join(log_dir, log_filename)

    with open(file_path, "w", encoding="utf-8") as file:
        for msg in messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            file.write(f"{role}: {content}\n\n")

    print(f"\nChat saved to {file_path}")

# =======================
# MEMORY
# =======================
def summarize_conversation(messages):
    conversation_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in messages[1:]]
    )

    summary_prompt = [
        {"role": "system", "content": "Summarize this conversation briefly."},
        {"role": "user", "content": conversation_text}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=summary_prompt,
        temperature=0
    )

    conversation_summary = response.choices[0].message.content

    new_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Conversation summary so far: {conversation_summary}"}
    ]

    return new_messages, conversation_summary


def trim_messages(messages):
    return [messages[0]] + messages[-(MAX_TURNS * 2):]

# =======================
# AI RESPONSE
# =======================
def get_ai_reply(messages):
    print("\nAI: ", end="", flush=True)

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0,
        stream=True
    )

    reply = ""

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            reply += delta

    print()
    return reply

# =======================
# COMMAND HANDLER
# =======================
def handle_command(user_input, messages):
    command = user_input.lower()

    if command == "exit":
        print("\nGoodbye!")
        return "exit", messages

    if command == "reset":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        print("\nChat history cleared.")
        return "reset", messages

    if command == "clear":
        os.system("cls" if os.name == "nt" else "clear")
        return "clear", messages

    if command == "save":
        save_chat(messages)
        return "save", messages

    return "chat", messages

# =======================
# MAIN LOOP
# =======================
def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    conversation_summary = ""

    while True:
        user_input = input("\nYou: ")

        action, messages = handle_command(user_input, messages)

        if action == "exit":
            break

        if action in ["reset", "clear", "save"]:
            if action == "reset":
                conversation_summary = ""
            continue

        messages.append({"role": "user", "content": user_input})

        if len(messages) > SUMMARY_TRIGGER:
            messages, conversation_summary = summarize_conversation(messages)

        messages = trim_messages(messages)

        reply = get_ai_reply(messages)

        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()