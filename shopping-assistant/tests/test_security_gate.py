from app.agent import REDEEMED_CODES, redeem_discount_code


def test_redeem_discount_success() -> None:
    REDEEMED_CODES.clear()
    res = redeem_discount_code("user_123", "WELCOME50")
    assert "Success" in res
    assert "WELCOME50" in REDEEMED_CODES


def test_redeem_discount_unregistered_user() -> None:
    REDEEMED_CODES.clear()
    res = redeem_discount_code("unregistered_user_id", "WELCOME50")
    assert "Error" in res
    assert "not registered" in res


def test_redeem_discount_invalid_code() -> None:
    REDEEMED_CODES.clear()
    res = redeem_discount_code("user_123", "INVALIDCODE")
    assert "Error" in res
    assert "invalid" in res


def test_redeem_discount_single_use() -> None:
    REDEEMED_CODES.clear()
    res1 = redeem_discount_code("user_123", "WELCOME50")
    assert "Success" in res1

    res2 = redeem_discount_code("user_123", "WELCOME50")
    assert "Error" in res2
    assert "already been redeemed" in res2
