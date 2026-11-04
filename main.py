import os
import argparse
import json
from call_function import call_function
from call_function import available_functions
from prompts import system_prompt
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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
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
    for i in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
        )

        #Response handling and output
        if response.usage is None:
            raise RuntimeError("API request failed")
            
        if response.choices[0].message.tool_calls is not None:
            for tool_call in response.choices[0].message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] is None:
                    raise Exception("Empty tool response detected")
                elif args.verbose:
                    print(f"-> {result_message["content"]}")
        elif response.choices[0].message.content is not None:
            print(response.choices[0].message.content)
            if args.verbose == True:
                print_metadata(response.usage.prompt_tokens, response.usage.completion_tokens, args.user_prompt)
            return
           
        message = response.choices[0].message
        messages.append(message)
        messages.append(result_message)
    print("Maximum number of opperations exceeded, stopping agent")
    exit(1)

if __name__ == "__main__":
    main()
