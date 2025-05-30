from dotenv import load_dotenv
import json
from openai import OpenAI
from HiteshSir import SYSTEM_PROMPT
from Hitesh_gemini import get_self_consistent_answers

load_dotenv()
client = OpenAI()

messages = [
    { "role": "system", "content": SYSTEM_PROMPT }
]

print("Type 'exit' to quit.")

while True:
    query = input("> ")
    if query.lower() in ["exit", "quit"]:
        print("Bye! Chai pe milte hain!")
        break

    messages.append({ "role": "user", "content": query })
    final_response = None

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        assistant_msg = response.choices[0].message.content
        messages.append({ "role": "assistant", "content": assistant_msg })
        parsed_response = json.loads(assistant_msg)

        step = parsed_response.get("step")
        content = parsed_response.get("content")

        
        if step in ("explore", "compute"):
            gemini_suggestions = get_self_consistent_answers(query)
            validation_content = "Validated with Gemini suggestions: " + "; ".join(gemini_suggestions)
            messages.append({
                "role": "assistant",
                "content": json.dumps({"step": "crosscheck", "content": validation_content})
            })
            continue

        if step == "wrap_up":
            final_response = content
            break

    print("🤖:", final_response)
