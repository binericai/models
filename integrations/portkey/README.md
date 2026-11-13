# Bineric with Portkey

[Portkey](https://portkey.ai) is an AI gateway with routing, fallbacks, caching and observability. Bineric trains its own European
models: Zuse, a decision model trained on European languages, and Lynx, a European general model. Bineric also makes NorskGPT, a
Norwegian AI assistant. The same EU-hosted API, with one key, also serves Borealis 2 from the National Library of Norway, Claude
through Amazon Bedrock, GPT through Azure, and open models.

Bineric's API is OpenAI-compatible, so Portkey reaches every Bineric chat model through its `custom_host` setting, with the
`openai` provider format and `https://api.bineric.com/v1` as the host. You need a Bineric API key from
[platform.bineric.com](https://platform.bineric.com).

## Option 1: Portkey Model Catalog (hosted Portkey)

Store Bineric once in Portkey and call it by name. This follows Portkey's
[Bring Your Own LLM](https://portkey.ai/docs/integrations/llms/byollm) guide.

1. In Portkey, open **Model Catalog**, then **Add Provider**, and turn on **Local/Privately hosted provider**.
2. Choose **OpenAI** as the API specification and set **Custom Host** to `https://api.bineric.com/v1`.
3. Add the header `Authorization` with the value `Bearer <your Bineric API key>`.
4. Name the provider `bineric` and save.

Then call it with your Portkey key:

```python
from portkey_ai import Portkey

portkey = Portkey(api_key="PORTKEY_API_KEY", provider="@bineric")

response = portkey.chat.completions.create(
    model="lynx-30b",
    messages=[{"role": "user", "content": "Hva er hovedstaden i Norge?"}],
)
print(response.choices[0].message.content)
```

## Option 2: pass Bineric's details on each request

```python
import os

from portkey_ai import Portkey

portkey = Portkey(
    api_key="PORTKEY_API_KEY",                 # leave out when you run the gateway yourself
    provider="openai",
    custom_host="https://api.bineric.com/v1",
    Authorization=f"Bearer {os.environ['BINERIC_API_KEY']}",
)

response = portkey.chat.completions.create(
    model="lynx-30b",
    messages=[{"role": "user", "content": "Hva er hovedstaden i Norge?"}],
)
print(response.choices[0].message.content)
```

The same with cURL:

```bash
curl https://api.portkey.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "x-portkey-api-key: $PORTKEY_API_KEY" \
  -H "x-portkey-provider: openai" \
  -H "x-portkey-custom-host: https://api.bineric.com/v1" \
  -H "Authorization: Bearer $BINERIC_API_KEY" \
  -d '{"model": "lynx-30b", "messages": [{"role": "user", "content": "Hva er hovedstaden i Norge?"}]}'
```

## Self-hosted Portkey gateway

Portkey's open-source gateway takes the same headers. Start it with `npx @portkey-ai/gateway`, then send requests to
`http://localhost:8787/v1` without `x-portkey-api-key`, or pass `base_url="http://localhost:8787/v1"` to the Python SDK.
[`example.py`](example.py) does this.

## Which models

| model id | what it is | hosted |
|---|---|---|
| `lynx-30b` | Lynx, Bineric's European general model | EU |
| `borealis-2` | The National Library of Norway's Norwegian model, 16,384-token context | EU |
| `claude-sonnet-5.5`, `claude-haiku-5.5` and other Claude models | Anthropic's Claude through Amazon Bedrock | EU |
| `gpt-5.4`, `gpt-5.5` and other GPT models | OpenAI's GPT through Azure | EU |

`GET https://api.bineric.com/v1/models` lists every model with its context length, price and hosting (`EU` or `US`). It needs no
key. Some models are hosted in the US, the Gemini models for example, so check `hosting` if your data has to stay in the EU.

## Zuse

Zuse, Bineric's European decision model, answers typed questions with probabilities instead of generating text. It uses its own
endpoint, `POST /v1/zuse`, not chat completions, so it does not go through Portkey's chat interface. See [zuse/](../../zuse/) and
the [API documentation](https://bineric.com/zuse/docs).

## What was tested

On 13 Nov 2026, Option 2 and the cURL headers were run through a self-hosted gateway (`@portkey-ai/gateway` 1.15.2, Python SDK
`portkey-ai` 2.3.4) against Bineric's production API, and `lynx-30b` answered. Streaming through that npx-installed gateway failed
with `TypeError: immutable`, a known Portkey issue ([Portkey-AI/gateway#1389](https://github.com/Portkey-AI/gateway/issues/1389)).
Bineric's own streaming works when called directly. The hosted Portkey steps in Option 1 follow Portkey's documentation and were not
run with a Portkey account.

Support: support@bineric.com
