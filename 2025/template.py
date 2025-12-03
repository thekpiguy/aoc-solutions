import click

from aocd import get_data
from time import time

TEST_DATA = """"""


def part1():
    return None


def part2():
    return None


@click.command()
@click.option("--test", "-t", is_flag=True)
def dayN(test):
    start_tm = time()

    if test:
        raw_data = TEST_DATA
    else:
        raw_data = get_data(day=1, year=2025)

    print("=" * 75)
    print("Part 1")
    part1_start_tm = time()

    part1_solution = part1()

    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    print(f"Part 1 solution = {part1_solution}")
    print(f"Part 1 duration = {part1_dur:,.0f} seconds")
    print("=" * 75)

    print("Part 2")
    part2_start_tm = time()

    part2_solution = part2()

    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    print(f"Part 2 solution = {part2_solution}")
    print(f"Part 2 duration = {part2_dur:,.0f} seconds")
    print("=" * 75)

    end_tm = time()
    total_dur = end_tm - start_tm
    print(f"Total time = {total_dur:,.0f} seconds")

if __name__ == "__main__":
    dayN()
