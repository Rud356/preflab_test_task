import math
import statistics
import sys
from collections import Counter
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

listed_values.sort()


def calculate_optimal_average_value(values: list[int]) -> int:
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

def calculate_min_max_avg_value(values: list[int]) -> int:
    # Calculating min and max values average assuming the optimal value is between those two
    average_value: float = 0
    sub_average_count: int = 0
    above_average_count: int = 0

    for val in values:
        if val < average_value:
            sub_average_count += 1

        else:
            above_average_count += 1

    average_value = (min(values) + max(values)) / len(values)

    # If there are more numbers below average - it makes sense to get closer to them
    # and round down instead of up
    if sub_average_count > above_average_count:
        return math.floor(average_value)

    else:
        return math.ceil(average_value)


def calculate_best_value_by_mean(values: list[int]) -> int:
    return int(statistics.median(values))


def calculate_steps_count_for_average(values: list[int], average: int) -> int:
    return sum(
        # we only do steps in 1 in each direction, so distance to average is modulus of (value - average)
        map(lambda val: abs(val-average), values)
    )


def statistics_counter_optimized_steps(values: list[int]) -> int:
    # Finding most common value to optimize all other to be that number
    counter: Counter[int] = Counter(values)
    most_common_number, most_common_count = counter.most_common(1)[0]
    return most_common_number


optimized_variants_step_count: list[int] = [
    calculate_steps_count_for_average(
        listed_values,
        # Works for cases when values have bell curve distribution
        calculate_optimal_average_value(listed_values)
    ),
    calculate_steps_count_for_average(
        listed_values,
        # Assuming for event distribution
        calculate_min_max_avg_value(listed_values)
    ),
    calculate_steps_count_for_average(
        listed_values,
        # Assuming lots of same values are same, and one or two outliers present
        statistics_counter_optimized_steps(listed_values)
    ),
    calculate_steps_count_for_average(
        listed_values,
        # Assuming mean value is least affected and is middle of the values list
        calculate_best_value_by_mean(listed_values)
    )
]
print(min(optimized_variants_step_count))
