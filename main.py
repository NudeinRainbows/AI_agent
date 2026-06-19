import os
import argparse
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

    model = "gemini-2.5-flash"
    response = client.models.generate_content(
        model=model,
        contents=messages
    )


    if response.usage_metadata is None:
        raise RuntimeError("usage_metadata is None")

    vprint(f"User prompt: {prompt}")
    vprint(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    vprint(f"Response tokens: {response.usage_metadata.total_token_count}")
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
