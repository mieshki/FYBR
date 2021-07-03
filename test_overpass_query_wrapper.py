from app import utilities


def test_set_radius():
    query = utilities.OverpassQuery(None)
    query.set_radius(15)
    assert query.around == 15


def test_add_key_value_tag():
    query = utilities.OverpassQuery(None)
    query.add_key_value_tag(('highway', 'cycleway'))
    assert query.list_of_key_values_tags[0] == ('highway', 'cycleway')
