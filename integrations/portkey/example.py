"""Call a Bineric chat model through a self-hosted Portkey gateway.

npx @portkey-ai/gateway          # in another terminal, listens on http://localhost:8787
pip install portkey-ai
BINERIC_API_KEY=... python example.py [model-id]

For hosted Portkey, drop base_url and pass api_key="PORTKEY_API_KEY" instead.
"""

import os
import sys

from portkey_ai import Portkey

model = sys.argv[1] if len(sys.argv) > 1 else "lynx-30b"

portkey = Portkey(
    base_url="http://localhost:8787/v1",
    provider="openai",
    custom_host="https://api.bineric.com/v1",
    Authorization=f"Bearer {os.environ['BINERIC_API_KEY']}",
)

response = portkey.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Say hello in Norwegian, in one short sentence."}],
)

print(response.choices[0].message.content)
print(f"tokens: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")
