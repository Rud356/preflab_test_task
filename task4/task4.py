import math
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise ValueError(
        "Invalid number of arguments supplied "
        f"(must get 1 path, got {len(sys.argv) - 1} args)"
    )

try:
    args: list[Path] = [Path(arg) for arg in sys.argv[1:]]

except ValueError as err:
    raise ValueError("Must get only paths as arguments") from err


list_path: Path = args[0]
listed_values: list[int] = []

with list_path.open(encoding="utf-8") as f:
    while len((read_number := f.readline())) != 0:
        listed_values.append(int(read_number))


def calculate_optimal_middle_value(values: list[int]) -> int:
    # List probably should come down to single value, and least distance
    # from the biggest number to smallest is average of all numbers
    average_value: float = 0
    sub_average_count: int = 0
    above_average_count: int = 0

    for val in values:
        if val < average_value:
            sub_average_count += 1

        else:
            above_average_count += 1

        average_value += val
    average_value /= len(values)

    # If there are more numbers below average - it makes sense to get closer to them
    # and round down instead of up
    if sub_average_count > above_average_count:
        return math.floor(average_value)

    else:
        return math.ceil(average_value)


def calculate_steps_count(values: list[int], average: int) -> int:
    return sum(
        # we only do steps in 1 in each direction, so distance to average is modulus of (value - average)
        map(lambda val: abs(val-average), values)
    )



best_average: int = calculate_optimal_middle_value(listed_values)
steps_count: int = calculate_steps_count(listed_values, best_average)
print(steps_count)