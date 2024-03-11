import math

from flowmapper.unit import Unit


def test_equals():
    u1 = Unit("M2A")
    u2 = Unit("m2*year")

    assert u1 == u2


def test_equals_mass():
    u1 = Unit("kg")
    u2 = Unit("kilogram")

    assert u1 == u2


def test_energy():
    u1 = Unit("kilowatt hour")
    u2 = Unit("MJ")
    assert u1.compatible(u2)
    assert u1.conversion_factor(u2) == 3.6


def test_enrichment():
    u1 = Unit("SWU")
    u2 = Unit("tonne * SW")
    assert u1.compatible(u2)
    assert u1.conversion_factor(u2) == 1e-3


def test_natural_gas():
    u1 = Unit("nm3")
    u2 = Unit("sm3")
    assert u1.compatible(u2)


def test_livestock():
    u1 = Unit("LU")
    u2 = Unit("livestock unit")
    assert u1 == u2


def test_freight():
    u1 = Unit("kilogram * km")
    u2 = Unit("tkm")
    assert u1.conversion_factor(u2) == 1e-3


def test_vehicular_travel():
    u1 = Unit("vehicle * m")
    u2 = Unit("vkm")
    assert u1.conversion_factor(u2) == 1e-3


def test_person_travel():
    u1 = Unit("person * m")
    u2 = Unit("pkm")
    assert u1.conversion_factor(u2) == 1e-3


def test_conversion_factor():
    u1 = Unit("mg")
    u2 = Unit("kg")
    actual = u1.conversion_factor(u2)
    assert actual == 1e-06


def test_nan_conversion_factor():
    u1 = Unit("bq")
    u2 = Unit("kg")
    actual = u1.conversion_factor(u2)
    assert math.isnan(actual)


def test_complex_conversions():
    u1 = Unit("square_meter_year / t")
    u2 = Unit("(meter ** 2 * month) / kg")
    assert u1.conversion_factor(u2) == 0.012
