import base64


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
