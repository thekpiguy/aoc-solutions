import click

from aocd import get_data
from time import time

TEST_DATA = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


def parse_data(raw):
    fresh_id_rngs = list()
    ids_to_check = list()
    for ln in raw.split("\n"):
        if "-" in ln:
            tmp_st, tmp_ed = ln.split("-")
            fresh_id_rngs.append((int(tmp_st), int(tmp_ed)))
        elif ln == "":
            pass
        else:
            ids_to_check.append(int(ln))
    return fresh_id_rngs, ids_to_check


def is_id_fresh(id_ranges, item_id, test):
    for tmp_start, tmp_end in id_ranges:
        tmp_cond = tmp_start <= item_id <= tmp_end
        if test:
            print(f"Range: {tmp_start} - {tmp_end}, In Range: {tmp_cond}")
        if tmp_cond:
            return True
    return False


def get_merged_ranges(id_ranges, test):
    """
    Reference: https://stackoverflow.com/questions/15273693/union-of-multiple-ranges
    """
    id_ranges_srt = sorted(id_ranges)
    merged_ranges = list()
    for tmp_start, tmp_end in id_ranges_srt:
        if len(merged_ranges) != 0 and merged_ranges[-1][1] >= tmp_start - 1:
            tmp_replace = (merged_ranges[-1][0], max(merged_ranges[-1][1], tmp_end))
            merged_ranges[-1] = tmp_replace
        else:
            merged_ranges.append((tmp_start, tmp_end))
        if test:
            print(f"Rng={(tmp_start, tmp_end)}, Unioned={merged_ranges}")
    return merged_ranges


def get_num_fresh_ids_from_merged(merged_ranges):
    num_fresh_ids = 0
    for tmp_rng in merged_ranges:
        num_fresh_ids += (tmp_rng[1] - tmp_rng[0] + 1)
    return num_fresh_ids


def part1(id_ranges, ids_to_check, test):
    fresh_ids = set()
    for tmp_id in ids_to_check:
        tmp_cond = is_id_fresh(id_ranges=id_ranges, item_id=tmp_id, test=test)
        if test:
            print(f"Id={tmp_id}, Fresh={tmp_cond}")
        if tmp_cond:
            fresh_ids.add(tmp_id)
    return len(fresh_ids)


def part2(id_ranges, test):
    merged_ranges = get_merged_ranges(id_ranges=id_ranges, test=test)
    return get_num_fresh_ids_from_merged(merged_ranges=merged_ranges)


@click.command()
@click.option("--test", "-t", is_flag=True)
def day5(test):
    start_tm = time()

    if test:
        raw_data = TEST_DATA
    else:
        raw_data = get_data(day=5, year=2025)
    
    fresh_id_ranges, ids_to_check = parse_data(raw=raw_data)
    if test:
        print("DATA")
        print("=" * 75)
        print(f"Ranges={fresh_id_ranges}")
        print(f"Ids={ids_to_check}")

    print("=" * 75)
    print("Part 1")
    part1_start_tm = time()

    part1_solution = part1(id_ranges=fresh_id_ranges, ids_to_check=ids_to_check, test=test)

    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    print(f"Part 1 solution = {part1_solution}")
    print(f"Part 1 duration = {part1_dur:,.0f} seconds")
    print("=" * 75)

    print("Part 2")
    part2_start_tm = time()

    part2_solution = part2(id_ranges=fresh_id_ranges, test=test)

    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    print(f"Part 2 solution = {part2_solution}")
    print(f"Part 2 duration = {part2_dur:,.0f} seconds")
    print("=" * 75)

    end_tm = time()
    total_dur = end_tm - start_tm
    print(f"Total time = {total_dur:,.0f} seconds")

if __name__ == "__main__":
    day5()
