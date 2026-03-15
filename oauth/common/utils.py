import time

import requests
import jwt  # PyJWT


def escape_soql(value: str) -> str:
    """SOQL インジェクション対策のためのエスケープ処理。"""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def get_access_token(
    client_id: str,
    username: str,
    private_key_file: str,
    audience: str,
    token_endpoint: str,
) -> tuple[str, str]:
    """JWT Bearer Flow でアクセストークンと instance_url を取得する。"""
    now = int(time.time())
    payload = {
        "iss": client_id,
        "sub": username,
        "aud": audience,
        "exp": now + 300,  # 5分後に期限切れ
    }

    try:
        with open(private_key_file) as f:
            private_key = f.read()
    except OSError as e:
        raise RuntimeError(
            f"秘密鍵ファイルの読み込みに失敗しました: {private_key_file}"
        ) from e

    assertion = jwt.encode(payload, private_key, algorithm="RS256")

    response = requests.post(
        token_endpoint,
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        },
        timeout=30,
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(
            f"Salesforce 認証エラー: {response.status_code} {response.text}"
        ) from e

    try:
        token_data = response.json()
    except ValueError as e:
        raise RuntimeError("Salesforce 認証レスポンスのパースに失敗しました") from e

    try:
        return token_data["access_token"], token_data["instance_url"]
    except KeyError as e:
        raise RuntimeError(
            f"Salesforce 認証レスポンスに必要なキーが存在しません: {e}"
        ) from e
