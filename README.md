# Mastodon初投稿ブーストBot
Mastodon上で、まだフォロワーの少ない新規アカウントの最初の公開投稿をブーストするBotです。  
ローカルタイムライン上に流れた初投稿をその場でブーストするほか、投稿から一定期間(デフォルトでは2日間)の間、決まった時刻に初投稿をブーストします。  
ローカルアカウント同士のフォロー関係が密接になることを想定されたクローズドコミュニティのインスタンス等での利用を想定し、ブーストされた投稿を通じて他の一般アカウントから新規アカウントを見付けやすくします。  

## Usage
1. リポジトリを`git clone`等で複製します。  
2. settingsディレクトリ内の設定サンプルをコピーします。  
   ```bash
   cp settings/.env.sample settings/.env
   cp settings/config.yaml.sample settings/config.yaml
   ```
3. .envの`BASE_URL`にBotを稼働させたいインスタンスのURL(`https`のようなスキームを含む)を設定し、`ACCESS_TOKEN`にBotの認証に用いるアクセストークンを設定します。その他の項目も必要に応じて書き換えてください。  
4. Docker Composeが利用できる環境であれば、以下のコマンドでコンテナを作成、起動します。  
   ```bash
   docker compose up -d
   ```
   あるいは、[uv](https://docs.astral.sh/uv/)が利用できる環境であれば、以下のコマンドでコンテナなし(ホストOS上)でBotを起動します。  
   ```bash
   uv sync
   uv run main.py
   ```
   いずれも利用できない環境では、いずれかお好みのツールをインストールして利用してください。  
