import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

def print_metadata(prompt_tokens: str, completion_tokens: str, user_prompt: str) -> None:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")

def main():
    #Input handling
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #Adding conversation memory
    messages = [
        {"role": "user", "content": args.user_prompt}
    ]

    #Actual AI-Agent stuff
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API-Key not found")
    client = OpenAI(
        base_url ="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    #Response handling and output
    if response.usage is None:
        raise RuntimeError("API request failed")
        
    if args.verbose == True:
        print_metadata(response.usage.prompt_tokens, response.usage.completion_tokens, args.user_prompt)
        
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
