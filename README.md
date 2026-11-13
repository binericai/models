# Bineric

Public material for [Bineric](https://bineric.com)'s models: deployment guides, notebooks, sample requests and recorded responses
for the cloud marketplaces they are sold through. One folder per model, one subfolder per channel.

| model | what it does | channels |
|---|---|---|
| [Zuse](zuse/) | European decision model: reads a document and answers fixed-choice questions with calibrated probabilities | [AWS Marketplace](zuse/aws-marketplace/) · [Azure Marketplace](zuse/azure-marketplace/) (coming) |

## Integrations

| tool | what is there |
|---|---|
| [LiteLLM](integrations/litellm/) | Python SDK example and a proxy config for Bineric's chat models: Bineric's own Lynx, Borealis 2, and Claude and GPT hosted in the EU |
| [Portkey](integrations/portkey/) | Model Catalog setup and custom-host examples for Bineric's chat models through Portkey, hosted or self-hosted |

Support: support@bineric.com

The code and examples in this repository are MIT licensed. The models themselves are licensed through each marketplace's terms.
