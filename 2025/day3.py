import click

from aocd import get_data
from itertools import combinations
from time import time

TEST_DATA = """987654321111111
811111111111119
234234234234278
818181911112111"""


def parse_data(raw):
    data = [[int(v) for v in list(ln)] for ln in raw.split("\n")]
    return data


# def find_max_joltage(bank, n):
#     num_bats = len(bank)
#     idxs_to_check = combinations(range(num_bats), n)
#     max_jolts = -1
#     for tmp_idxs in idxs_to_check:
#         tmp_bank_sub = [str(bank[i]) for i in tmp_idxs]
#         tmp_jolts = int("".join(tmp_bank_sub))
#         if max_jolts < tmp_jolts:
#             max_jolts = tmp_jolts
#         if max_jolts == int("9" * n):
#             return max_jolts
#     return max_jolts


def find_max_joltage(bank, n, test):
    num_bats = len(bank)
    prev_max_idx = -1
    max_jolts = -1
    if test:
        print(f"BANK={bank}, N={n}")
    for i in range(n):
        tmp_start = prev_max_idx + 1
        tmp_limit = num_bats - (n - i)
        # tmp_factor = 10 ** (n - (i + 1))
        # max_jolts = max_jolts * tmp_factor
        for j in range(tmp_start, tmp_limit + 1):
            tmp_bat_jolts = bank[j]
            if i == 0:
                tmp_first_n = -1
                cand_jolts = tmp_bat_jolts
            else:
                tmp_first_n = max_jolts // 10
                cand_jolts = int(f"{tmp_first_n}{tmp_bat_jolts}")
            if test:
                print(f"i={i}, j={j}, l={tmp_limit}, b={tmp_bat_jolts}, m={max_jolts}, m_n={tmp_first_n}, c={cand_jolts}")
            if max_jolts < cand_jolts:
                max_jolts = cand_jolts
                prev_max_idx = j
                # if we see a 9 that is the first max and we can break early
                if tmp_bat_jolts == 9:
                    break
        max_jolts *= 10
    
    # because we are adding factors of 10 at the end of every outer loop
    # we end up higher by 1 factor of 10 at the end and so need to adjust
    # the return value
    return max_jolts // 10


def part1(data, test):
    total_joltage = 0
    for bank in data:
        max_jolts = find_max_joltage(bank=bank, n=2, test=test)
        total_joltage += max_jolts
        if test:
            print(f"Bank={bank}, Jolts={max_jolts}")
    return total_joltage


def part2(data, test):
    total_joltage = 0
    for bank in data:
        max_jolts = find_max_joltage(bank=bank, n=12, test=test)
        total_joltage += max_jolts
        if test:
            print(f"Bank={bank}, Jolts={max_jolts}")
    return total_joltage


@click.command()
@click.option("--test", "-t", is_flag=True)
def day3(test):
    start_tm = time()

    if test:
        raw_data = TEST_DATA
    else:
        raw_data = get_data(day=3, year=2025)
    
    clean_data = parse_data(raw=raw_data)

    if test:
        print(f"Data = {clean_data}")

    print("=" * 75)
    print("Part 1")
    part1_start_tm = time()

    part1_solution = part1(data=clean_data, test=test)

    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    print(f"Part 1 solution = {part1_solution}")
    print(f"Part 1 duration = {part1_dur:,.0f} seconds")
    print("=" * 75)

    print("Part 2")
    part2_start_tm = time()

    part2_solution = part2(data=clean_data, test=test)

    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    print(f"Part 2 solution = {part2_solution}")
    print(f"Part 2 duration = {part2_dur:,.0f} seconds")
    print("=" * 75)

    end_tm = time()
    total_dur = end_tm - start_tm
    print(f"Total time = {total_dur:,.0f} seconds")

if __name__ == "__main__":
    day3()
