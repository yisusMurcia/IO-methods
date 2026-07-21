from model.M import M


def test_initialization_defaults():
    m = M()

    assert m.x == 1
    assert m.b == 0


def test_addition_and_right_addition():
    m = M()

    m + 2
    assert m.x == 1
    assert m.b == 2

    m + M()
    assert m.x == 2
    assert m.b == 2

    assert (3 + m).b == 5


def test_subtraction_and_right_subtraction():
    m = M()

    m - 2
    assert m.x == 1
    assert m.b == -2

    m - M()
    assert m.x == 0
    assert m.b == -2

    assert (3 - m).b == 5


def test_multiplication_and_right_multiplication():
    m = M()

    m * 3
    assert m.x == 3
    assert m.b == 0

    assert (4 * m).x == 12
    assert (4 * m).b == 0


def test_comparison_methods_with_numbers_and_objects():
    m = M()

    assert m >= 0
    assert m > 0
    assert not(m < 0)
    assert not(m <= 0)

    other = M()
    other - 5

    assert m >= other
    assert m > other
    assert not m < other
    assert not m <= other


def test_unary_negation():
    m = -M()

    assert m.x == -1
    assert m.b == 0
