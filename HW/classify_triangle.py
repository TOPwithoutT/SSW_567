from __future__ import annotations
from typing import Union

Number = Union[int, float]

def classify_triangle(a: Number, b: Number, c: Number) -> str:
    """
    Classify a triangle given side lengths a, b, c.

    Returns one of:
      - "NotATriangle"
      - "equilateral"
      - "isosceles"
      - "scalene"
      - "right isosceles"
      - "right scalene"

    Notes:
      - Handles ints/floats.
      - Uses a small tolerance to compare floats.
    """
    # ---- input validation ----
    for x in (a, b, c):
        if not isinstance(x, (int, float)):
            return "NotATriangle"
        if x <= 0:
            return "NotATriangle"

    # sort sides so that x <= y <= z
    x, y, z = sorted([float(a), float(b), float(c)])

    # tolerance for float comparisons
    eps = 1e-9

    # ---- triangle inequality ----
    # For robustness with floats, allow small epsilon.
    if x + y <= z + eps:
        return "NotATriangle"

    # ---- basic type (equilateral / isosceles / scalene) ----
    def almost_equal(u: float, v: float, tol: float = eps) -> bool:
        return abs(u - v) <= tol * max(1.0, abs(u), abs(v))

    is_eq_xy = almost_equal(x, y)
    is_eq_yz = almost_equal(y, z)
    is_eq_xz = almost_equal(x, z)

    if is_eq_xy and is_eq_yz:  # all equal
        return "equilateral"

    # ---- right check (Pythagoras): x^2 + y^2 == z^2 ----
    # Scale-aware tolerance using the magnitude of z^2
    lhs = x * x + y * y
    rhs = z * z
    is_right = abs(lhs - rhs) <= (eps * max(1.0, abs(rhs)))

    if is_eq_xy or is_eq_yz or is_eq_xz:
        return "right isosceles" if is_right else "isosceles"
    else:
        return "right scalene" if is_right else "scalene"


if __name__ == "__main__":
    samples = [
        (3, 4, 5),       # right scalene
        (2, 2, 3),       # isosceles
        (1, 1, 1),       # equilateral
        (5, 12, 13),     # right scalene
        (1, 2, 3),       # NotATriangle
        (1.0, 1.0, 2**0.5),  # right isosceles (≈45-45-90)
    ]
    for a, b, c in samples:
        print((a, b, c), "->", classify_triangle(a, b, c))
