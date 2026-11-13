"""Call a Bineric chat model through LiteLLM.

pip install litellm
BINERIC_API_KEY=... python example.py [model-id]
"""

import os
import sys

import litellm

model = sys.argv[1] if len(sys.argv) > 1 else "lynx-30b"

response = litellm.completion(
    model=f"openai/{model}",
    api_base="https://api.bineric.com/v1",
    api_key=os.environ["BINERIC_API_KEY"],
    messages=[{"role": "user", "content": "Say hello in Norwegian, in one short sentence."}],
)

print(response.choices[0].message.content)
print(f"tokens: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")
