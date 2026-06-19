import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key not found")
client = genai.Client(api_key=api_key)

def main():
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    model = "gemini-2.5-flash"
    response = client.models.generate_content(model=model, contents=prompt)


    if response.usage_metadata is None:
        raise RuntimeError("usage_metadata is None")

    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.total_token_count}")
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
