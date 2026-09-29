from tools.calculator import calculator


def test_calculator():
    assert calculator.invoke({"expression": "2+2"}) == "4"
