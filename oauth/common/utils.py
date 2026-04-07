import base64
import time

import requests
import jwt  # PyJWT


def decode_valid_for(valid_for: str, controller_values: list[str]) -> list[str]:
    """validFor（Base64ビットマスク）をデコードして有効な親の値リストを返す。

    Args:
        valid_for: Salesforce describe の validFor フィールド（Base64文字列）
        controller_values: 親フィールドの選択リスト値のリスト

    Returns:
        この子の値が有効になる親の値のリスト
    """
    if not valid_for:
        return list(controller_values)

    bits = base64.b64decode(valid_for)
    result = []
    for i, ctrl_value in enumerate(controller_values):
        byte_idx = i // 8
        bit_idx = 7 - (i % 8)
        if byte_idx < len(bits) and (bits[byte_idx] >> bit_idx) & 1:
            result.append(ctrl_value)
    return result


def escape_soql(value: str) -> str:
    """SOQL インジェクション対策のためのエスケープ処理。"""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def get_access_token(
    client_id: str,
    username: str,
    private_key: str,
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
