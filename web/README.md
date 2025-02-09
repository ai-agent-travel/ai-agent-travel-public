# プロジェクトの概要

このプロジェクトはAIエージェントハッカソンに提出するレポジトリです。
Next.jsを使用しています。

# 起動方法

プロジェクトの.envに以下の値を設定します。

```
DATABASE_URL="file:./dev.db"
API_ENDPOINT=http://localhost:8083
NEXT_PUBLIC_API_KEY=FirebaseのAPI Key
NEXT_PUBLIC_AUTH_DOMAIN=FirebaseのAuth Domain
NEXT_PUBLIC_PROJECT_ID=FirebaseのProject ID
NEXT_PUBLIC_STORAGE_BUCKET=FirebaseのStorage Bucket
NEXT_PUBLIC_MESSAGING_SENDER_ID=FirebaseのMessage Sender ID
NEXT_PUBLIC_APP_ID=FirebaseのAPI Key
NEXTAUTH_SECRET=ランダムなUUID
```

API_KEYなどはご自身でFirebaseのプロジェクトを作成し、環境変数を設定してください。

上記の設定後に以下のコマンドで起動ができます。

```
pnpm install
```

```
pnpm prisma:db:push
```

```
pnpm dev
```