# aws-idc-import

## 概要

このプロジェクトは、AWS IAM Identity Center（旧AWS SSO）を使用して、CSVファイルからユーザーとグループを作成し、ユーザーをグループに追加するスクリプトです。

## ファイル構成

- `settings.yml`: IAM Identity CenterのIdentity Store IDおよびSSOプロファイル名を設定するための設定ファイル。
- `main.py`: メインのスクリプトファイル。ユーザーとグループの作成、ユーザーのグループへの追加を行います。
- `users.csv`: ユーザー情報を含むCSVファイル。ユーザー名、氏名、メールアドレス、グループ情報が含まれます。

## 事前準備 AWS SSO 設定手順

1. AWS CLIをインストールしていない場合は、インストールします：

    ```bash
    pip install awscli
    ```

2. AWS SSOを設定します：

    ```bash
    aws configure sso
    ```

3. プロンプトに従って、SSOの設定を完了します。 

## 使い方

1. `settings.yml`ファイルを作成し、以下の内容を設定します：

    ```yaml
    IDENTITY_STORE_ID: 'your-identity-store-id'
    SSO_PROFILE: 'your-sso-profile'
    ```

2. `users.csv`ファイルを作成し、以下の形式でユーザー情報を入力します：

    ```csv
    username,first_name,last_name,email,groups
    johndoe,John,Doe,johndoe@example.com,group1;group2
    ```

3. `requirements.txt`ファイルに記載されたパッケージをインストールします：

    ```bash
    pip install -r requirements.txt
    ```

4. スクリプトを実行します：

    ```bash
    python main.py
    ```

## 注意事項

- `settings.yml`ファイルには、適切なIdentity Store IDおよびSSOプロファイル名を設定してください。
- `users.csv`ファイルには、ユーザー情報を正確に入力してください。
- AWS CLIが設定されている必要があります。

## ライセンス

このプロジェクトはMITライセンスの下で提供されます。

## バージョン情報

- Python: 3.x
- boto3: 最新バージョン