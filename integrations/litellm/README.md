# Bineric with LiteLLM

[LiteLLM](https://github.com/BerriAI/litellm) is an open-source SDK and gateway that calls many model providers through one
OpenAI-style interface. Bineric's API is OpenAI-compatible, so LiteLLM can call every Bineric chat model today, including Claude and
GPT models hosted in the EU, Borealis 2 and Lynx.

You need a Bineric API key from [platform.bineric.com](https://platform.bineric.com). Set it as `BINERIC_API_KEY`.

## Python SDK

```python
import os

import litellm

response = litellm.completion(
    model="openai/claude-sonnet-5.5",
    api_base="https://api.bineric.com/v1",
    api_key=os.environ["BINERIC_API_KEY"],
    messages=[{"role": "user", "content": "Say hello in Norwegian."}],
)
print(response.choices[0].message.content)
```

The `openai/` prefix tells LiteLLM to use its OpenAI-compatible client. The part after it is the Bineric model id.
[`example.py`](example.py) is the same call as a script.

## LiteLLM proxy

[`config.yaml`](config.yaml) serves four Bineric models through a LiteLLM proxy and sets their prices, so the proxy's spend tracking
shows what each call cost:

```bash
pip install 'litellm[proxy]'
export BINERIC_API_KEY=...
export LITELLM_MASTER_KEY=sk-local-test
litellm --config config.yaml

curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-sonnet-5.5", "messages": [{"role": "user", "content": "Say hello"}]}'
```

Add more models the same way. `GET https://api.bineric.com/v1/models` lists every model with its id, context length, price per
million tokens and where it is hosted (`EU`, `US` or `Both`). It needs no key.

## Which models

| model id | what it is | hosted |
|---|---|---|
| `claude-sonnet-5.5`, `claude-opus-5.5`, `claude-haiku-4-5` and older Claude models | Anthropic's Claude through Amazon Bedrock | EU |
| `gpt-5.4`, `gpt-5.5`, `gpt-4o`, `o3-mini` and more | OpenAI's GPT through Azure | EU |
| `borealis-2` | The National Library of Norway's Norwegian model, 16,384-token context | EU |
| `lynx-30b` | Bineric's own general model | EU |

Some models in the list are hosted in the US (the Gemini models, for example). Check the `hosting` field if your data has to stay
in the EU.

## Zuse

Zuse, Bineric's decision model, does not use chat completions. It has its own endpoint, `POST /v1/zuse`, and is not reachable through
LiteLLM's chat interface. See [zuse/](../../zuse/) and the [API documentation](https://bineric.com/zuse/docs).

Support: support@bineric.com
