from flowmapper.extraction.ecospold2 import remove_conflicting_synonyms


def test_remove_conflicting_synonyms_no_conflicts():
    """Test that synonyms are kept when there are no conflicts."""
    data = [
        {"name": "flow_a", "context": ["ground"], "synonyms": ["water", "h2o"]},
        {"name": "flow_b", "context": ["ground"], "synonyms": ["soil", "earth"]},
    ]

    result = remove_conflicting_synonyms(data)

    assert result[0]["synonyms"] == ["water", "h2o"]
    assert result[1]["synonyms"] == ["soil", "earth"]


def test_remove_conflicting_synonyms_with_conflicts():
    """Test that conflicting synonyms are removed."""
    data = [
        {"name": "flow_a", "context": ["ground"], "synonyms": ["water", "h2o"]},
        {
            "name": "water",  # This conflicts with the synonym in flow_a
            "context": ["ground"],
            "synonyms": ["aqua"],
        },
    ]

    result = remove_conflicting_synonyms(data)

    # "water" should be removed from flow_a's synonyms
    assert result[0]["synonyms"] == ["h2o"]
    assert result[1]["synonyms"] == ["aqua"]


def test_remove_conflicting_synonyms_different_contexts():
    """Test that synonyms are kept when conflicts exist in different contexts."""
    data = [
        {"name": "flow_a", "context": ["ground"], "synonyms": ["water", "h2o"]},
        {
            "name": "water",  # This conflicts but is in different context
            "context": ["air"],
            "synonyms": ["aqua"],
        },
    ]

    result = remove_conflicting_synonyms(data)

    # "water" should be kept since contexts are different
    assert result[0]["synonyms"] == ["water", "h2o"]
    assert result[1]["synonyms"] == ["aqua"]


def test_remove_conflicting_synonyms_multiple_conflicts():
    """Test removal of multiple conflicting synonyms."""
    data = [
        {"name": "flow_a", "context": ["ground"], "synonyms": ["water", "soil", "h2o"]},
        {"name": "water", "context": ["ground"], "synonyms": ["aqua"]},
        {"name": "soil", "context": ["ground", "deep"], "synonyms": ["earth"]},
    ]

    result = remove_conflicting_synonyms(data)

    # Both "water" and "soil" should be removed from flow_a's synonyms
    assert result[0]["synonyms"] == ["h2o"]
    assert result[1]["synonyms"] == ["aqua"]
    assert result[2]["synonyms"] == ["earth"]


def test_remove_conflicting_synonyms_no_synonyms():
    """Test handling of flows without synonyms."""
    data = [
        {
            "name": "flow_a",
            "context": ["ground"],
            # No synonyms
        },
        {"name": "flow_b", "context": ["ground"], "synonyms": ["water"]},
    ]

    result = remove_conflicting_synonyms(data)

    # Should not raise error and flow_b should keep its synonym
    assert "synonyms" not in result[0]
    assert result[1]["synonyms"] == ["water"]


def test_remove_conflicting_synonyms_no_context():
    """Test handling of flows without context."""
    data = [
        {
            "name": "flow_a",
            "synonyms": ["water", "h2o"],
            # No context
        },
        {"name": "water", "context": ["ground"], "synonyms": ["aqua"]},
    ]

    result = remove_conflicting_synonyms(data)

    # flow_a should keep its synonyms since it has no context
    assert result[0]["synonyms"] == ["water", "h2o"]
    assert result[1]["synonyms"] == ["aqua"]


def test_remove_conflicting_synonyms_empty_synonyms_list():
    """Test handling of empty synonyms list."""
    data = [
        {"name": "flow_a", "context": ["ground"], "synonyms": []},
        {"name": "water", "context": ["ground"], "synonyms": ["aqua"]},
    ]

    result = remove_conflicting_synonyms(data)

    # Empty synonyms list should remain empty
    assert result[0]["synonyms"] == []
    assert result[1]["synonyms"] == ["aqua"]


def test_remove_conflicting_synonyms_case_insensitive():
    """Test that synonym removal is case insensitive."""
    data = [
        {"name": "flow_a", "context": ["ground"], "synonyms": ["Water", "H2O"]},
        {
            "name": "water",  # Lowercase, different from "Water"
            "context": ["ground"],
            "synonyms": ["aqua"],
        },
    ]

    result = remove_conflicting_synonyms(data)

    assert result[0]["synonyms"] == ["H2O"]
    assert result[1]["synonyms"] == ["aqua"]


def test_remove_conflicting_synonyms_self_conflict():
    """Test that a flow's own name doesn't conflict with its synonyms."""
    data = [
        {"name": "water", "context": ["ground"], "synonyms": ["h2o", "aqua", "water"]}
    ]

    result = remove_conflicting_synonyms(data)

    # All synonyms should be kept since they don't conflict with other flows
    assert result[0]["synonyms"] == ["h2o", "aqua"]


def test_remove_conflicting_synonyms_preserves_original_data():
    """Test that the function doesn't modify other fields in the data."""
    data = [
        {
            "name": "flow_a",
            "context": ["ground"],
            "synonyms": ["water", "h2o"],
            "unit": "kg",
            "identifier": "123",
        },
        {
            "name": "water",
            "context": ["ground"],
            "synonyms": ["aqua"],
            "unit": "m3",
            "identifier": "456",
        },
    ]

    result = remove_conflicting_synonyms(data)

    # Check that other fields are preserved
    assert result[0]["name"] == "flow_a"
    assert result[0]["context"] == ["ground"]
    assert result[0]["unit"] == "kg"
    assert result[0]["identifier"] == "123"
    assert result[0]["synonyms"] == ["h2o"]  # Only "water" removed

    assert result[1]["name"] == "water"
    assert result[1]["context"] == ["ground"]
    assert result[1]["unit"] == "m3"
    assert result[1]["identifier"] == "456"
    assert result[1]["synonyms"] == ["aqua"]
