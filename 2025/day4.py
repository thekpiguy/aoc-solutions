import click
import copy

from aocd import get_data
from time import time

TEST_DATA = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


def parse_data(raw):
    data = list()
    for ln in raw.split("\n"):
        tmp_row = list(ln)
        tmp_row.insert(0, ".")
        tmp_row.append(".")
        data.append(tmp_row)
    num_cols = len(data[0])
    buffer_row = ["."] * num_cols
    data.insert(0, buffer_row)
    data.append(buffer_row)
    return data


def get_paper_locs(data):
    locs = list()
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == "@":
                locs.append((i, j))
    return locs


def get_neighbors(data, cur_pos):
    neighbors = list()
    cur_i, cur_j = cur_pos
    adjs = [-1, 0, 1]
    for tmp_r_adj in adjs:
        new_i = cur_i + tmp_r_adj
        for tmp_c_adj in adjs:
            new_j = cur_j + tmp_c_adj
            if (new_i, new_j) != cur_pos:
                yield (tmp_r_adj, tmp_c_adj), (new_i, new_j), data[new_i][new_j]


def is_roll_eligible(data, cur_pos, limit, test):
    neighboring_rolls = 0
    for tmp_adjs, tmp_neigh_loc, tmp_neigh in get_neighbors(data=data, cur_pos=cur_pos):
        if test:
            print(f"Cur={cur_pos}, Adj={tmp_adjs}, Neigh loc={tmp_neigh_loc}, Neigh={tmp_neigh}, Num={neighboring_rolls}")
        if tmp_neigh == "@":
            neighboring_rolls += 1
    return neighboring_rolls < limit


def find_eligible_rolls(data, locs, limit, test):
    eligible_roll_locs = list()
    for tmp_loc in locs:
        tmp_elig_check = is_roll_eligible(data=data, cur_pos=tmp_loc, limit=limit, test=test)
        if test:
            print(f"Cur={tmp_loc}, Eligible={tmp_elig_check}")
        if tmp_elig_check:
            eligible_roll_locs.append(tmp_loc)
    return eligible_roll_locs


def remove_paper_rolls(data, eligible_locs, test):
    new_data = copy.deepcopy(data)
    for tmp_row, tmp_col in eligible_locs:
        new_data[tmp_row][tmp_col] = "."
    return new_data


def part1(data, test):
    roll_locs = get_paper_locs(data=data)
    if test:
        print(f"Roll locs={roll_locs}")
    eligible_roll_locs = find_eligible_rolls(data=data, locs=roll_locs, limit=4, test=test)
    if test:
        print(f"Eligible locs={eligible_roll_locs}")
    return len(eligible_roll_locs)


def part2(data, test):
    new_data = copy.deepcopy(data)
    roll_locs = get_paper_locs(data=new_data)
    eligible_roll_locs = find_eligible_rolls(data=new_data, locs=roll_locs, limit=4, test=test)
    total_removed_rolls = len(eligible_roll_locs)
    new_data = remove_paper_rolls(data=new_data, eligible_locs=eligible_roll_locs, test=test)
    while len(eligible_roll_locs) != 0:
        roll_locs = get_paper_locs(data=new_data)
        eligible_roll_locs = find_eligible_rolls(data=new_data, locs=roll_locs, limit=4, test=test)
        total_removed_rolls += len(eligible_roll_locs)
        new_data = remove_paper_rolls(data=new_data, eligible_locs=eligible_roll_locs, test=test)
    return total_removed_rolls


@click.command()
@click.option("--test", "-t", is_flag=True)
def day4(test):
    start_tm = time()

    if test:
        raw_data = TEST_DATA
    else:
        raw_data = get_data(day=4, year=2025)
    
    clean_data = parse_data(raw=raw_data)

    if test:
        print(f"DATA")
        print("=" * 75)
        for r in clean_data:
            print(r)
        print("=" * 75)

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
    day4()
