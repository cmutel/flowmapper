from flowmapper.utils import normalize_str


def test_normalize_str():
    names = [
        "\u0075\u0308ber",
        "\u0055\u0308ber",
        "\u00FCber",
        "\u00DCber",
        "\u00DCber ",
        " \u00DCber",
        None,
    ]
    assert {normalize_str(name) for name in names} == {"über", "Über", ""}
