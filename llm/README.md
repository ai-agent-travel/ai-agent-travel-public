# ai-agent-travel-llm

## セットアップ

```
make login
```
- プロジェクトが適切なものであるか確認
  - `gcloud config get-value project`
  - 変更が必要な場合は `gcloud config set project <PROJECT_ID>`

- terraform のインストール
  - https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli
  - `terraform --version` で確認
  - `terraform` でリソースを展開する前に、GCPのAPIを有効化する

## デプロイ

```
# インフラ構築後、cloud runデプロイ時に実行
make build
make push
make deploy

# 初回およびインフラ変更時に実行
make terraform
- GCP のプロジェクト ID の入力が求められるので、対象のものを入力
- 初回適用時は、AR に image がないので、cloud run の起動部分のみエラーがでる
```
