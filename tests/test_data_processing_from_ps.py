from utils import parse_ch_measures, prepare_ch_measures_data, prepare_condition_data

INVALID_RESPONSES = ('', '4.10466677,-3.13684184\n',
                     '4.10466677,-3.13684184,1.75743178,6.16397784\n')


def test_parse_measures_from_ps_response():
    """valid"""

    data = parse_ch_measures('4.10466677,-3.13684184,1.75743178\n')
    assert len(data) == 3
    assert data['current'] == 4.10466677
    assert data['voltage'] == -3.13684184
    assert data['power'] == 1.75743178

    """invalid"""

    for invalid_raw_data in INVALID_RESPONSES:
        data = parse_ch_measures(invalid_raw_data)
        assert not data


def test_prepare_ch_measures_data():
    channel_number = 1

    """valid"""

    data = prepare_ch_measures_data(channel_number, '4.10466677,-3.13684184,1.75743178\n')
    assert len(data) == 4
    assert data['channel'] == channel_number
    assert data['current'] == 4.10466677
    assert data['voltage'] == -3.13684184
    assert data['power'] == 1.75743178

    """invalid"""

    for invalid_raw_data in INVALID_RESPONSES:
        try:
            prepare_ch_measures_data(channel_number, invalid_raw_data)
        except ValueError:
            assert True


def test_get_json_all_ch_measures():
    """valid"""

    ch_measures_map = {
        1: '4.10466677,-3.13684184,1.75743178\n',
        2: '4.10466677,-3.13684184,1.75743178\n',
        3: '4.10466677,-3.13684184,1.75743178\n',
        4: '4.10466677,-3.13684184,1.75743178\n'
    }

    expected_data = {
        'conditions': [
            {
                'channel': 1,
                'current': 4.10466677,
                'voltage': -3.13684184,
                'power': 1.75743178
            },
            {
                'channel': 2,
                'current': 4.10466677,
                'voltage': -3.13684184,
                'power': 1.75743178
            },
            {
                'channel': 3,
                'current': 4.10466677,
                'voltage': -3.13684184,
                'power': 1.75743178
            },
            {
                'channel': 4,
                'current': 4.10466677,
                'voltage': -3.13684184,
                'power': 1.75743178
            }
        ]
    }

    data = prepare_condition_data(ch_measures_map)
    assert len(data['conditions']) == 4
    assert data == expected_data

    """invalid"""

    invalid_ch_measures_map = {1: '\n', 2: '', 3: ' ', 4: ''}
    try:
        prepare_condition_data(invalid_ch_measures_map)
    except ValueError:
        assert True
