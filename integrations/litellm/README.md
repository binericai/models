# Bineric with LiteLLM

[LiteLLM](https://github.com/BerriAI/litellm) is an open-source SDK and gateway that calls many model providers through one
OpenAI-style interface. Bineric trains its own European models: Zuse, a decision model trained on European languages, and Lynx, a
European general model. Bineric also makes NorskGPT, a Norwegian AI assistant. The same EU-hosted API, with one key, also serves
Borealis 2 from the National Library of Norway, Claude through Amazon Bedrock, GPT through Azure, and open models. The API is
OpenAI-compatible, so LiteLLM can call every Bineric chat model today.

You need a Bineric API key from [platform.bineric.com](https://platform.bineric.com). Set it as `BINERIC_API_KEY`.

## Python SDK

```python
import os

import litellm

response = litellm.completion(
    model="openai/lynx-30b",
    api_base="https://api.bineric.com/v1",
    api_key=os.environ["BINERIC_API_KEY"],
    messages=[{"role": "user", "content": "Say hello in Norwegian."}],
)
print(response.choices[0].message.content)
```

The `openai/` prefix tells LiteLLM to use its OpenAI-compatible client. The part after it is the Bineric model id.
[`example.py`](example.py) is the same call as a script.

## LiteLLM proxy

[`config.yaml`](config.yaml) serves four Bineric models (Lynx, Borealis 2, Claude Sonnet 5.5 and GPT-5.4) through a LiteLLM
proxy and sets their prices, so the proxy's spend tracking shows what each call cost:

```bash
pip install 'litellm[proxy]'
export BINERIC_API_KEY=...
export LITELLM_MASTER_KEY=sk-local-test
litellm --config config.yaml

curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "lynx-30b", "messages": [{"role": "user", "content": "Say hello"}]}'
```

Add more models the same way. `GET https://api.bineric.com/v1/models` lists every model with its id, context length, price per
million tokens and where it is hosted (`EU` or `US`). It needs no key.

## Which models

| model id | what it is | hosted |
|---|---|---|
| `zuse-27b`, `zuse-9b` | Zuse, Bineric's European decision model (see [Zuse](#zuse) below) | EU |
| `lynx-30b` | Lynx, Bineric's European general model | EU |
| `borealis-2` | The National Library of Norway's Norwegian model, 16,384-token context | EU |
| `claude-sonnet-5.5`, `claude-opus-5.5`, `claude-haiku-5.5` and older Claude models | Anthropic's Claude through Amazon Bedrock | EU |
| `gpt-5.4`, `gpt-5.5`, `gpt-4o`, `o3-mini` and more | OpenAI's GPT through Azure | EU |

Some models in the list are hosted in the US (the Gemini models, for example). Check the `hosting` field if your data has to stay
in the EU.

## Zuse

Zuse, Bineric's European decision model, does not use chat completions. It has its own endpoint, `POST /v1/zuse`, and is not
reachable through LiteLLM's chat interface in current LiteLLM releases. A `bineric` provider that also serves Zuse on LiteLLM's
`/v1/systemone` route is in review ([BerriAI/litellm#51621](https://github.com/BerriAI/litellm/pull/51621)). Until then, see
[zuse/](../../zuse/) and the [API documentation](https://bineric.com/zuse/docs).

Support: support@bineric.com
