import pytest
import grade_utils as gu


def test_average_high_low():
    s = [80, 90, 100]
    assert gu.calculate_average(s) == 90
    assert gu.highest_score(s) == 100
    assert gu.lowest_score(s) == 80


def test_pass_fail():
    assert gu.pass_fail([60, 70]) == "Pass"
    assert gu.pass_fail([20, 30]) == "Fail"


@pytest.mark.parametrize("bad", [[-1, 50], [101], [50, "x"], [], [True]])
def test_invalid_scores(bad):
    with pytest.raises(gu.InvalidScoreError):
        gu.calculate_average(bad)
