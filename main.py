import os
import argparse
from functions.call_function import available_functions
from functions.call_function import call_function
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key not found")
client = genai.Client(api_key=api_key)


def main():
    def vprint(*a,**kw):
        if args.verbose:
            print(*a, **kw)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    prompt = args.user_prompt

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    for _ in range(20):
        model = "gemini-2.5-flash"
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
                )
        )

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("usage_metadata is None")

        vprint(f"User prompt: {prompt}")
        vprint(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        vprint(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)

                if function_call_result.parts is None:
                    raise Exception(f"{function_call} returned empty parts list")

                if function_call_result.parts[0].function_response is None:
                    raise Exception(f"{function_call} returned None function response")

                function_results.append(function_call_result.parts[0])

                vprint(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(f"Response:\n{response.text}")
            return 0

    print(f"Maximum iterations reached")
    return 1


if __name__ == "__main__":
    main()
