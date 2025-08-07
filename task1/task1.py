import copy
import itertools
import sys
from typing import Generator

if len(sys.argv) != 3:
    raise ValueError(
        "Invalid number of arguments supplied "
        f"(must get 2 numbers, got {len(sys.argv) - 1} args)"
    )

try:
    args: list[int] = [int(arg) for arg in sys.argv[1:]]

except ValueError as err:
    raise ValueError("Must get only integer numbers as arguments") from err

n: int = args[0]
m: int = args[1]

if n < 1:
    raise ValueError("Invalid length for array provided as n")

initial_chain: list[int] = [i for i in range(1, n + 1)]


def generate_subchains_in_chain(
    input_chain: list[int], run_length: int
) -> Generator[list[int], None, None]:
    current_subset: list[int] = []

    for number in itertools.cycle(input_chain):
        current_subset.append(number)

        if len(current_subset) == run_length:
            yield copy.copy(current_subset)
            new_first_value: int = current_subset[-1]
            current_subset.clear()
            current_subset.append(new_first_value)


def calculate_chains_path(
    input_chain: list[int], run_length: int
) -> list[int]:
    subchains: list[list[int]] = []

    for subchain in generate_subchains_in_chain(input_chain, run_length):
        if len(subchains) != 0:
            if subchain == subchains[0]:
                break

            else:
                subchains.append(subchain)

        else:
            subchains.append(subchain)

    return [chain_parts[0] for chain_parts in subchains]


calculated_path: list[int] = calculate_chains_path(initial_chain, m)
path: str = "".join(map(str, calculated_path))
print(path)
