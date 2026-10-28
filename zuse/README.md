# Zuse

Zuse is Bineric's decision model for European companies. Give it a document, such as an email, a ticket, a claim or a contract
clause, and the questions you want answered. For each question it picks from the options you set and returns how sure it is, so you
can act automatically on the confident answers and send the rest to a person. It does not generate text, so it cannot answer outside
the options you give it. It uses the same request format as TypeSafe's Jev.

| model | accuracy (4-bit, 20,044 held-out questions, 27 languages) | languages at 85 % or more | GPU |
|---|---|---|---|
| Zuse 27B | 87.4 % | 115 | one 24 GB GPU |
| Zuse 9B | 83.6 % | 83 | one 24 GB GPU, down to the smallest instances |

Both are trained on 27 European languages. Documents up to 64k tokens.

## Where to get it

- [AWS Marketplace](aws-marketplace/): runs in your AWS account on Amazon SageMaker with network isolation.
  [Zuse 27B listing](https://aws.amazon.com/marketplace/pp/prodview-p4pgjmsbglf76)
- [Azure Marketplace](azure-marketplace/): coming.
- Hosted API: [API documentation](https://bineric.com/zuse/docs).

Support: support@bineric.com
