import click
import re

from aocd import get_data
from functools import reduce
from time import time

TEST_DATA = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


def get_factors(n):
    """
    Reference: https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
    """
    first_pass = set(
        reduce(
            list.__add__,
            ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
        )
    )
    filtered = sorted([i for i in first_pass if i < n], reverse=True)
    return filtered


def parse_data(raw):
    pcs = [re.match(r"(\d+)-(\d+)", pc).groups() for pc in raw.split(",")]
    pcs = [(int(pc[0]), int(pc[1])) for pc in pcs]
    return pcs


def is_candidate(idval, part):
    if part == 1:
        return len(str(idval)) % 2 == 0
    else:
        return True


def get_candidates(start, end, part):
    cands = list()
    for tmp_c in range(start, end + 1):
        if is_candidate(idval=tmp_c, part=part):
            cands.append(tmp_c)
    return cands


def is_invalid_part1(idval, test):
    idval_str = str(idval)
    idval_len = len(idval_str)
    step = idval_len // 2
    pcs = [idval_str[i:i+step] for i in range(0, idval_len, step)]
    cond = len(set(pcs)) == 1
    if cond:
        if test:
            print(f"Id={idval_str}, Pcs={pcs}, Invalid={cond}")
        return True
    return False
    


def is_invalid_part2(idval, test):
    idval_str = str(idval)
    idval_len = len(idval_str)
    factors = get_factors(n=idval_len)
    for tmp_fctr in factors:
        pcs = [idval_str[i:i+tmp_fctr] for i in range(0, idval_len, tmp_fctr)]
        cond = len(set(pcs)) == 1
        if cond:
            if test:
                print(f"F={tmp_fctr}, ID={idval_str}, PCS={pcs}, Invalid={cond}")
            return True
    return False


def get_invalid_ids(start, end, test, part):
    invalid_ids = list()
    candidates = get_candidates(start=start, end=end, part=part)
    invalid_check_fn = is_invalid_part1 if part == 1 else is_invalid_part2
    for tmp_cand in candidates:
        if invalid_check_fn(idval=tmp_cand, test=test):
            invalid_ids.append(tmp_cand)
    return invalid_ids


def part1(data, test):
    invalid_ids = list()
    for tmp_start, tmp_end in data:
        invalid_ids += get_invalid_ids(start=tmp_start, end=tmp_end, test=test, part=1)
    return sum(invalid_ids)


def part2(data, test):
    invalid_ids = list()
    for tmp_start, tmp_end in data:
        invalid_ids += get_invalid_ids(start=tmp_start, end=tmp_end, test=test, part=2)
    return sum(invalid_ids)


@click.command()
@click.option("--test", "-t", is_flag=True)
def day2(test):
    start_tm = time()

    if test:
        raw_data = TEST_DATA
    else:
        raw_data = get_data(day=2, year=2025)
    
    clean_data = parse_data(raw=raw_data)

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
    day2()
