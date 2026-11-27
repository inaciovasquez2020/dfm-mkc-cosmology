"""Exact arithmetic checks accompanying RADION_SPECTRAL_CHECKPOINT.md."""
from fractions import Fraction as Q
from math import factorial


def verify_two_power_witness():
    coefficients = {1: Q(-1, 10), 3: Q(1), 6: Q(-2), 7: Q(13, 10)}
    value = sum(coefficients.values())
    slope = -sum(power * coefficient for power, coefficient in coefficients.items())
    curvature = sum(
        power * (power + 1) * coefficient
        for power, coefficient in coefficients.items()
    )
    assert (value, slope, curvature) == (Q(1, 5), 0, Q(3, 5))
    assert (Q(2) / Q(8, 5)) ** 4 > Q(13, 10) ** 3


def verify_massive_witness_bound():
    # Positive Taylor tail gives exp(3) > 20. At x=3, the coefficients
    # of the numerator of R's nth summand sum to 47.
    assert sum(Q(3**j, factorial(j)) for j in range(9)) > 20
    coefficients = (5, 15, 18, 9)
    assert sum(coefficients) == 47
    assert 8 * Q(47, 19) + 2 * Q(1, 100) * 3**3 < 30


def verify_pair_threshold():
    # Compare squared square-root sums without floating-point arithmetic.
    for mass in (Q(1, 10), Q(1), Q(7, 3)):
        for level in range(-12, 13):
            center = level // 2
            gap = 4 * mass**2 + level**2
            for split in range(-20, 21):
                left = mass**2 + split**2
                right = mass**2 + (level - split)**2
                # A positive residual permits squaring the inequality.
                residual = gap - left - right
                assert residual <= 0 or 4 * left * right >= residual**2
                # Even levels attain equality at the central split.
                if split == center and level % 2 == 0:
                    assert residual >= 0 and 4 * left * right == residual**2


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("INCOMPLETE: Python assertions disabled")
    verify_two_power_witness()
    verify_massive_witness_bound()
    verify_pair_threshold()
    print("TWO_POWER_WITNESS := PASS")
    print("MASSIVE_THRESHOLD_BOUND := PASS")
    print("FLAT_PRODUCT_PAIR_GAP := PASS")
    print("COUPLED_NONZERO_BOSONIC_KK := OPEN")
