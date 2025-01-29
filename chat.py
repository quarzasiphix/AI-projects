# deepseek_cli.py
import requests

def ask_deepseek(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-r1:1.5b",  # Your installed model name
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        answer = ask_deepseek(user_input)
        print(f"\nDeepSeek: {answer}")