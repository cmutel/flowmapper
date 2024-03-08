from flowmapper.utils import extract_country_code


def test_with_valid_country_code():
    assert extract_country_code("ammonia, nl") == ("ammonia", "nl")


def test_with_no_country_code():
    assert extract_country_code("ammonia") == ("ammonia", None)


def test_with_additional_text():
    assert extract_country_code("ammonia, nl something") == (
        "ammonia, nl something",
        None,
    )


def test_with_space_before_country_code():
    assert extract_country_code("ammonia,   nl") == ("ammonia", "nl")
