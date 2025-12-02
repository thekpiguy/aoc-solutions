import click
from aocd import get_data
from functools import reduce

TEST_DATA = """"""


def factors(n):
    """
    Reference: https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
    """
    return set(reduce(
        list.__add__,
        ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def part1():
    return None


def part2():
    return None


@click.command()
@click.option("--test", "-t", is_flag=True)
def day2():
    start_tm = time()

    for i in [4, 6, 8, 10, 20]:
        print(f"N={i}, F={factors(i)}")

    if test:
        raw_data = TEST_DATA
    else:
        raw_data = get_data(day=2, year=2025)

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
    day2()
