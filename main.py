#!/usr/bin/env python3
import csv
import boto3
import yaml
import codecs

# settings.yml を読み込む
with open('settings.yml', 'r') as file:
    settings = yaml.safe_load(file)

IDENTITY_STORE_ID = settings['IDENTITY_STORE_ID']
SSO_PROFILE = settings['SSO_PROFILE']

# boto3 のセッションを SSO 用プロファイルで作成
session = boto3.Session(profile_name=SSO_PROFILE)
identity_client = session.client('identitystore')

def get_group_id(group_name):
    """
    指定したグループ名で既存のグループを検索し、あれば GroupId を返す
    """
    try:
        response = identity_client.list_groups(
            IdentityStoreId=IDENTITY_STORE_ID,
            Filters=[
                {
                    'AttributePath': 'DisplayName',
                    'AttributeValue': group_name
                }
            ]
        )
        groups = response.get('Groups', [])
        if groups:
            return groups[0]['GroupId']
    except Exception as e:
        print(f"グループ検索中にエラーが発生しました: {e}")
    return None

def create_group(group_name):
    """
    グループが存在しない場合、新規にグループを作成し、その GroupId を返す
    """
    try:
        response = identity_client.create_group(
            IdentityStoreId=IDENTITY_STORE_ID,
            DisplayName=group_name
        )
        group_id = response['GroupId']
        print(f"グループ '{group_name}' を作成しました。GroupId: {group_id}")
        return group_id
    except Exception as e:
        print(f"グループ作成中にエラーが発生しました: {e}")
        return None

def get_user_id(username):
    """
    指定したユーザー名で既存のユーザーを検索し、あれば UserId を返す
    """
    try:
        response = identity_client.list_users(
            IdentityStoreId=IDENTITY_STORE_ID,
            Filters=[
                {
                    'AttributePath': 'UserName',
                    'AttributeValue': username
                } 
            ]
        )
        users = response.get('Users', [])
        if users:
            return users[0]['UserId']
    except Exception as e:
        print(f"ユーザー検索中にエラーが発生しました: {e}")
        return None

def create_user(user_data):
    """
    CSVの1行分のデータからユーザーを作成し、その UserId を返す
    ※user_data は辞書で、username, first_name, last_name, email のキーがあることを想定
    """
    try:
        response = identity_client.create_user(
            IdentityStoreId=IDENTITY_STORE_ID,
            UserName=user_data['username'],
            Name={
                'GivenName': user_data['first_name'],
                'FamilyName': user_data['last_name']
            },
            DisplayName=user_data['display_name'],
            Emails=[
                {
                    'Value': user_data['email'],
                    'Type': 'work',
                    'Primary': True
                }
            ]
        )
        user_id = response['UserId']
        print(f"ユーザー '{user_data['username']}' を作成しました。UserId: {user_id}")
        return user_id
    except Exception as e:
        print(f"ユーザー作成中にエラーが発生しました: {e}")
        return None

def add_user_to_group(user_id, group_id):
    """
    ユーザーを指定したグループに追加する
    """
    try:
        response = identity_client.create_group_membership(
            IdentityStoreId=IDENTITY_STORE_ID,
            GroupId=group_id,
            MemberId={
                'UserId': user_id
            }
        )
        print(f"UserId: {user_id} を GroupId: {group_id} に追加しました。")
        return response
    except Exception as e:
        print(f"グループメンバーシップ追加中にエラーが発生しました: {e}")
        return None

def main():
    csv_file = 'users.csv'  # CSVファイルのパス。必要に応じて変更してください。

    try:
        with codecs.open(csv_file, 'r', 'utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # ユーザーが存在する場合はスキップ
                if get_user_id(row['username']):
                    print(f"ユーザー '{row['username']}' は既に存在します。")
                    continue

                # ユーザー作成
                user_id = create_user(row)
                if not user_id:
                    continue

                # groups カラムが存在する場合、セミコロン区切りで複数指定できる想定
                groups_str = row.get('groups', '')
                if groups_str:
                    group_names = [g.strip() for g in groups_str.split(';') if g.strip()]
                    for group_name in group_names:
                        group_id = get_group_id(group_name)
                        if not group_id:
                            # 該当グループがない場合は新規作成
                            group_id = create_group(group_name)
                        if group_id:
                            add_user_to_group(user_id, group_id)
    except FileNotFoundError:
        print(f"ファイル '{csv_file}' が見つかりません。ファイルパスを確認してください。")
    except Exception as e:
        print(f"CSVの読み込み中にエラーが発生しました: {e}")

if __name__ == '__main__':
    main()
