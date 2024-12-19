import click
from aocd import get_data
from collections import defaultdict
from copy import deepcopy
from pprint import pprint
from time import time

TEST_DATA = "2333133121414131402"


def get_parsed_data(raw_data: str) -> str:
    return raw_data.strip()


def get_inefficient_block_rep(data: str) -> str:
    file_id = 0
    block_rep = ""
    for idx, char in enumerate(data):
        if idx % 2 == 0:
            block_rep += (f"{file_id}" * int(char))
        else:
            block_rep += ("." * int(char))
            file_id += 1
    return block_rep


def get_efficient_block_rep(data: str):
    file_id = 0
    cur_pos = 0
    block_rep = defaultdict(list)
    for idx, char in enumerate(data):
        if idx % 2 == 0:
            for _ in range(int(char)):
                block_rep[file_id].append(cur_pos)
                cur_pos += 1
        else:
            for _ in range(int(char)):
                block_rep['free_spots'].append(cur_pos)
                cur_pos += 1
            file_id += 1
    return block_rep


def get_adjusted_blocks(block_rep: dict) -> dict:
    adj_block_rep = deepcopy(block_rep)
    done = False
    free_spot_idx = 0
    free_spot_len = len(adj_block_rep['free_spots'])
    file_ids_sorted = sorted(
        [k for k in adj_block_rep.keys() if k != 'free_spots'],
        reverse=True
    )
    while not done:
        for file_id in file_ids_sorted:
            for tmp_idx, fl_idx in reversed(list(enumerate(adj_block_rep[file_id]))):
                if free_spot_idx >= free_spot_len:
                    done = True
                    break
                else:
                    tmp_free_val = adj_block_rep['free_spots'][free_spot_idx]
                    if tmp_free_val > adj_block_rep[file_id][tmp_idx]:
                        done = True
                        break
                    else:
                        adj_block_rep['free_spots'][free_spot_idx] = fl_idx
                        adj_block_rep[file_id][tmp_idx] = tmp_free_val
                        free_spot_idx += 1
            adj_block_rep[file_id] = sorted(adj_block_rep[file_id])
    adj_block_rep['free_spots'] = sorted(adj_block_rep['free_spots'])
    return adj_block_rep


def get_filesystem_checksum(block_rep: dict) -> int:
    checksum = 0
    for k in [tmp_k for tmp_k in block_rep.keys() if tmp_k != 'free_spots']:
        for v in block_rep[k]:
            checksum += (k * v)
    return checksum


def get_part1_solution(data: str, test: bool) -> int:
    block_rep = get_efficient_block_rep(data=data)
    adj_block_rep = get_adjusted_blocks(block_rep=block_rep)
    if test:
        print("DATA")
        print(data)
        print()
        print("BLOCK REPRESENTATION")
        pprint(block_rep)
        print()
        print("ADJUSTED BLOCK REPRESENTATION")
        pprint(adj_block_rep)
    checksum = get_filesystem_checksum(block_rep=adj_block_rep)
    return checksum


@click.command()
@click.option("--test", "-t", is_flag=True)
def day9(test: bool):
    if test:
        print("Running with TEST data...")
        raw_data = TEST_DATA
    else:
        print("Running with PROD data...")
        raw_data = get_data(day=9, year=2024)
    
    tm_logs = dict()

    parse_start_tm = time()
    parsed_data = get_parsed_data(raw_data=raw_data)
    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parse'] = parse_dur

    part1_start_tm = time()
    part1 = get_part1_solution(data=parsed_data, test=test)
    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()

    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    print(f"PART 1 = {part1}")
    # print(f"PART 2 = {}")
    print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    day9()
