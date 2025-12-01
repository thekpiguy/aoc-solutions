import click
import re
from aocd import get_data
from time import time


TEST_DATA = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""


def parse_rotation(rot_str):
    d, amt = re.match(r"(\w)(\d+)", rot_str).groups()
    amt = int(amt)
    adj = amt
    if d == "L":
        adj = -1 * adj
    return d, amt, adj


def part1(start_pos, modulus, data, test):
    position = start_pos
    password = 0
    for tmp_rot_str in data.split("\n"):
        tmp_d, tmp_amt, tmp_adj = parse_rotation(rot_str=tmp_rot_str)
        if test:
            print(f"D={tmp_d}, A={tmp_amt}, Adj={tmp_adj}")
        position = (position + tmp_adj) % modulus
        if position == 0:
            if test:
                print("...updating password...")
            password += 1
    return password


# def part2(start_pos, modulus, data, test):
#     position = start_pos
#     password = 0
#     for tmp_rot_str in data.split("\n"):
#         tmp_d, tmp_amt, tmp_adj = parse_rotation(rot_str=tmp_rot_str)
#         old_position = position
#         new_position_no_mod = old_position + tmp_adj
#         k = abs(new_position_no_mod // 100)
#         position = new_position_no_mod % modulus

#         # if test:
#         #     print(f"D={tmp_d}, A={tmp_amt}, Adj={tmp_adj}, P={old_position}, Diff={new_position_no_mod}, New P={position}, K={k}")
#         print(f"D={tmp_d}, A={tmp_amt}, Adj={tmp_adj}, P={old_position}, Diff={new_position_no_mod}, New P={position}, K={k}")
        
#         # NOTE: old position should always be positive since we are doing mod arithmetic
#         #       but we should make sure old position was strictly positive so that we are
#         #       counting only when we cross 0.
#         # Case 1: from positive to negative and old posit, then crossed 0
#         if 0 < old_position and new_position_no_mod < 0:
#             if test:
#                 print("...updating password...")
#             password += k
        
#         # Case 2: from positive to greater than 100, then crossed 0
#         if 0 < old_position and 100 < new_position_no_mod:
#             if test:
#                 print("...updating password...")
#             password += k
        
#         # Case 3: land exactly on 0
#         if position == 0:
#             if test:
#                 print("...updating password...")
#             password += 1
    
#     return password
def part2(start_pos, modulus, data, test):
    position = start_pos
    password = 0
    for tmp_rot_str in data.split("\n"):
        tmp_d, tmp_amt, tmp_adj = parse_rotation(rot_str=tmp_rot_str)
        new_position_no_mod = position
        if test:
            print(f"D={tmp_d}, A={tmp_amt}, Adj={tmp_adj}, N={new_position_no_mod}, PW={password}")
        for i in range(tmp_amt):
            if tmp_d == "L":
                new_position_no_mod -= 1
            else:
                new_position_no_mod += 1
            if (new_position_no_mod % modulus == 0) and (i < tmp_amt - 1):
                if test:
                    print("...crossed 0, updating password...")
                password += 1
            if test:
                print(f"i={i}, D={tmp_d}, A={tmp_amt}, Adj={tmp_adj}, N={new_position_no_mod}, PW={password}")
            
        
        position = (position + tmp_adj) % modulus
        if position == 0:
            if test:
                print("...end position 0, updating password...")
            password += 1
    
    return password


@click.command()
@click.option("--test", "-t", is_flag=True)
def day1(test):
    start_tm = time()

    if test:
        raw_data = TEST_DATA
    else:
        raw_data = get_data(day=1, year=2025)
    
    start_pos = 50
    modulus = 100

    print("=" * 75)
    print("Part 1")
    part1_start_tm = time()

    part1_solution = part1(
        start_pos=start_pos,
        modulus=modulus,
        data=raw_data,
        test=test
    )

    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    print(f"Part 1 solution = {part1_solution}")
    print(f"Part 1 duration = {part1_dur:,.0f} seconds")
    print("=" * 75)

    print("Part 2")
    part2_start_tm = time()

    part2_solution = part2(
        start_pos=start_pos,
        modulus=modulus,
        data=raw_data,
        test=test
    )

    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    print(f"Part 2 solution = {part2_solution}")
    print(f"Part 2 duration = {part2_dur:,.0f} seconds")
    print("=" * 75)

    end_tm = time()
    total_dur = end_tm - start_tm
    print(f"Total time = {total_dur:,.0f} seconds")


if __name__ == "__main__":
    day1()
