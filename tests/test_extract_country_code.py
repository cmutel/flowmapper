from flowmapper.utils import extract_country_code


def test_with_lowercase():
    assert extract_country_code("ammonia, nl") == ("ammonia", "nl")


def test_with_uppercase():
    assert extract_country_code("ammonia, NL") == ("ammonia", "NL")


def test_with_no_country_code():
    assert extract_country_code("ammonia") == ("ammonia", None)


def test_with_additional_text():
    assert extract_country_code("ammonia, NL something") == (
        "ammonia, NL something",
        None,
    )


def test_with_space_before_country_code():
    assert extract_country_code("ammonia,   NL") == ("ammonia", "NL")
