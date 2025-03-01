def match_object(received, expected):
    print("rec", type(received))
    print("exp", type(expected))
    assert type(received) is type(expected)

    if type(received) is dict:
        for expected_key, expected_value in expected.items():
            if type(expected_value) is list:
                received_value = received.get(expected_key)
                assert received_value is not None

                match_list(received_value, expected_value)

    else:
        assert received == expected


def match_list(received, expected):
    assert type(received) is type(expected)
    assert type(received) is list
    assert len(received) == len(expected)

    for index in range(len(expected)):
        match_object(received=received[index], expected=expected[index])
