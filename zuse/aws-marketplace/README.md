# Zuse on AWS Marketplace

Zuse is [Bineric](https://bineric.com)'s European decision model. It reads a document (an email, a ticket, a claim, a contract clause)
and answers fixed-choice questions about it in one pass, each with a calibrated probability. It is trained on 27 European languages and scores 85 % or more in 115
languages with the 27B, 83 with the 9B (Belebele and SIB-200). It does not
generate text, so it cannot answer outside the options you give it.

Zuse runs in your own AWS account through AWS Marketplace (Amazon SageMaker) with network isolation: your documents never leave it.

| model | GPU | instance types |
|---|---|---|
| Zuse 27B (4-bit) | one 24 GB or 48 GB GPU | ml.g5.2xlarge, ml.g5.4xlarge, ml.g6.2xlarge, ml.g6.4xlarge, ml.g6e.xlarge, ml.g6e.2xlarge |
| Zuse 9B (4-bit) | one 24 GB or 48 GB GPU | the above, plus ml.g5.xlarge and ml.g6.xlarge |

The 27B is the more accurate (87.4 % with these 4-bit weights on our 20,044-row, 27-language held-out suite); the 9B is cheaper and
faster (83.6 %).

## Contents

- [`zuse_sagemaker.ipynb`](zuse_sagemaker.ipynb): deploy from your subscription, real-time requests, batch transform, clean-up.
- [`samples/input.jsonl`](samples/input.jsonl): three requests (an English contract, a Norwegian bank message, a German insurance claim).
- `samples/output-zuse-27b.jsonl`, `samples/output-zuse-9b.jsonl`: the responses, recorded from SageMaker endpoints.

## Request and response

`POST` (SageMaker `InvokeEndpoint`, `Content-Type: application/json`) a `state` and a map of named questions:

```json
{"state": "Hei, jeg vil avslutte kredittkortet mitt og flytte boliglånet til en annen bank. Kan dere sende meg innfrielsesbeløpet?",
 "questions": {
   "intent": {"type": "choice", "instructions": "What does the customer want?",
              "criteria": {"a": "Close the customer relationship or move the loan", "b": "A question about a card transaction", "c": "Something else"}},
   "asks_for_document": {"type": "noul", "instructions": "Does the customer ask the bank to send them something?"}}}
```

| type | asks | criteria | answer |
|---|---|---|---|
| `noul` | yes/no | none | `noul`: probability of yes |
| `choice` | one option of up to 255 | `{"name": "description"}` | `choice`, `confidence`, `probabilities` |
| `score` | a position on an ordered scale (2-10 levels) | `["level 0", "level 1", ...]` | `score` (expected level), `legend`, `probabilities` |

Each answer carries probabilities: automate the confident ones and send the rest to a person. Documents up to 64k tokens.
This is the same request format as TypeSafe's Jev. The endpoint also accepts the OpenAI Decisions format (`input` plus a `questions` array).

## Support

support@bineric.com · [API documentation](https://bineric.com/zuse/docs)

The example code in this repository is MIT licensed. The Zuse model is licensed through AWS Marketplace.
