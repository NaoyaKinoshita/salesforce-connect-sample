import time
import requests
import jwt  # PyJWT


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

    with open(private_key_file) as f:
        private_key = f.read()
    assertion = jwt.encode(payload, private_key, algorithm="RS256")

    response = requests.post(
        token_endpoint,
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        },
        timeout=30,
    )
    response.raise_for_status()

    token_data = response.json()
    return token_data["access_token"], token_data["instance_url"]
