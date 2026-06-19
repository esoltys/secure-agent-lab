from app.agent import REDEEMED_CODES, redeem_discount_code


def test_redeem_discount_code_success() -> None:
    # Reset redeemed codes
    REDEEMED_CODES.clear()

    # Success case
    res = redeem_discount_code("user_123", "WELCOME50")
    assert "Success" in res
    assert "WELCOME50" in res
    assert "WELCOME50" in REDEEMED_CODES


def test_redeem_discount_code_invalid_user() -> None:
    REDEEMED_CODES.clear()

    # Invalid user case
    res = redeem_discount_code("invalid_user", "WELCOME50")
    assert "Error" in res
    assert "not registered" in res


def test_redeem_discount_code_invalid_code() -> None:
    REDEEMED_CODES.clear()

    # Invalid code case
    res = redeem_discount_code("user_123", "INVALIDCODE")
    assert "Error" in res
    assert "invalid" in res


def test_redeem_discount_code_already_redeemed() -> None:
    REDEEMED_CODES.clear()

    # First redemption succeeds
    res1 = redeem_discount_code("user_123", "WELCOME50")
    assert "Success" in res1

    # Second redemption fails
    res2 = redeem_discount_code("user_456", "WELCOME50")
    assert "Error" in res2
    assert "already been redeemed" in res2
