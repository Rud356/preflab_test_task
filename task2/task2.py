import sys
from enum import IntEnum
from dataclasses import dataclass
from pathlib import Path

if len(sys.argv) != 3:
    raise ValueError(
        "Invalid number of arguments supplied "
        f"(must get 2 paths, got {len(sys.argv) - 1} args)"
    )

try:
    args: list[Path] = [Path(arg) for arg in sys.argv[1:]]

except ValueError as err:
    raise ValueError("Must get only paths as arguments") from err

circle_path, points_path = args


class RelativePosition(IntEnum):
    ON_CIRCLE = 0
    INSIDE = 1
    OUTSIDE = 2


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Circle:
    center: Point
    radius: int

    def check_relative_position(self, other_point: Point) -> RelativePosition:
        r_squared_real: int = self.radius ** 2
        r_squared_actual: int = (
            (other_point.x - self.center.x) ** 2 +
            (other_point.y - self.center.y) ** 2
        )

        if r_squared_real == r_squared_actual:
            return RelativePosition.ON_CIRCLE

        elif r_squared_real > r_squared_actual:
            return RelativePosition.INSIDE

        else:
            return RelativePosition.OUTSIDE


def parse_point(text: str) -> Point:
    x: int
    y: int
    x, y = map(int, text.strip().split())

    return Point(x, y)


center_point_line: str
radius_line: str
center_point_line, radius_line, *_ = circle_path.read_text("utf-8").split("\n")

circle: Circle = Circle(
    parse_point(center_point_line),
    int(radius_line)
)


with points_path.open(encoding="utf-8") as f:
    while len(line := f.readline()) > 0:
        current_point: Point = parse_point(line)
        print(circle.check_relative_position(current_point))
