"""Reusable grade-processing functions (import this module from other scripts)."""

from typing import Dict, List, Union

PASS_MARK = 50.0
MIN_SCORE = 0
MAX_SCORE = 100

Student = Dict[str, Union[str, List[float]]]


class InvalidScoreError(ValueError):
    """Raised when a score is not a number or is outside 0-100."""

    def __init__(self, score: object, message: str = "") -> None:
        self.score = score
        super().__init__(message or f"Invalid score {score!r}: must be a number "
                                    f"between {MIN_SCORE} and {MAX_SCORE}.")


def validate_score(score: object) -> float:
    """Return the score as a float, or raise InvalidScoreError."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise InvalidScoreError(score)
    if not MIN_SCORE <= score <= MAX_SCORE:
        raise InvalidScoreError(score)
    return float(score)


def validate_scores(scores: List[float]) -> List[float]:
    """Validate every score; raise InvalidScoreError on the first bad one."""
    if not scores:
        raise InvalidScoreError(scores, "Score list cannot be empty.")
    return [validate_score(s) for s in scores]


def calculate_average(scores: List[float]) -> float:
    valid = validate_scores(scores)
    return sum(valid) / len(valid)


def highest_score(scores: List[float]) -> float:
    return max(validate_scores(scores))


def lowest_score(scores: List[float]) -> float:
    return min(validate_scores(scores))


def pass_fail(scores: List[float], pass_mark: float = PASS_MARK) -> str:
    """Return 'Pass' if the average meets the pass mark, otherwise 'Fail'."""
    return "Pass" if calculate_average(scores) >= pass_mark else "Fail"


def process_student(student: Student) -> Dict[str, object]:
    """Build a result record for one student record {'name': ..., 'scores': [...]}."""
    scores = student["scores"]
    return {
        "name": student["name"],
        "average": round(calculate_average(scores), 2),
        "highest": highest_score(scores),
        "lowest": lowest_score(scores),
        "status": pass_fail(scores),
    }


def process_students(students: List[Student]):
    """Process many students; return (results, errors) so one bad record doesn't stop the rest."""
    results, errors = [], []
    for student in students:
        try:
            results.append(process_student(student))
        except InvalidScoreError as exc:
            errors.append((student.get("name", "?"), str(exc)))
    return results, errors
