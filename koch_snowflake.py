"""
Task 2: Koch snowflake fractal with recursion.
"""
from __future__ import annotations
import argparse
import math
from typing import List, Tuple
import matplotlib.pyplot as plt

Point = Tuple[float, float]

def koch_segment(p1: Point, p2: Point, level: int) -> List[Point]:
    if level == 0:
        return [p1]
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = (x2 - x1) / 3.0, (y2 - y1) / 3.0
    a = (x1 + dx, y1 + dy)
    b = (x1 + 2*dx, y1 + 2*dy)
    angle = math.atan2(y2 - y1, x2 - x1) - math.pi/3
    length = math.hypot(dx, dy)
    c = (a[0] + length * math.cos(angle), a[1] + length * math.sin(angle))

    pts = []
    pts += koch_segment(p1, a, level - 1)
    pts += koch_segment(a, c, level - 1)
    pts += koch_segment(c, b, level - 1)
    pts += koch_segment(b, p2, level - 1)
    return pts

def koch_snowflake(level: int) -> List[Point]:
    size = 1.0
    h = math.sqrt(3) / 2 * size
    p1, p2, p3 = (0.0, 0.0), (size, 0.0), (size/2.0, h)

    points = []
    points += koch_segment(p1, p2, level)
    points += koch_segment(p2, p3, level)
    points += koch_segment(p3, p1, level)
    points.append(p1)
    return points

def plot_snowflake(level: int, save: str | None) -> None:
    pts = koch_snowflake(level)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, linewidth=1)
    plt.axis("equal")
    plt.axis("off")
    plt.title(f"Koch Snowflake (level={level})")
    if save:
        plt.savefig(save, bbox_inches="tight", dpi=200)
        print(f"Saved to {save}")
    else:
        plt.show()

def main() -> None:
    parser = argparse.ArgumentParser(description="Draw the Koch snowflake.")
    parser.add_argument("--level", "-l", type=int, default=3, help="recursion level (>=0)")
    parser.add_argument("--save", "-s", type=str, help="path to save image")
    args = parser.parse_args()
    if args.level < 0:
        raise SystemExit("Level must be >= 0")
    plot_snowflake(args.level, args.save)

if __name__ == "__main__":
    main()