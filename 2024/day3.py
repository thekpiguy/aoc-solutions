import click
import math
import re
from time import time
from aocd import get_data


TEST_DATA1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
TEST_DATA2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def get_parsed_data(raw_data: str):
    # newlines will mess up the parsing for the second part
    # found after reading a few posts for the AoC reddit discussions
    # https://www.reddit.com/r/adventofcode/comments/1h5frsp/2024_day_3_solutions/
    raw_data = raw_data.replace('\n', ' ')
    pattern1 = re.compile(r"(mul\(\d+,\d+\))")
    pattern2 = re.compile(r"do\(\)(.*?)don't\(\)")
    part1_data = re.findall(pattern1, raw_data)

    # part 2 has blocks of commands sandwiched between do() and don't()
    # it is assumed at the start that there is a do()
    # and we can add a don't() at the end
    # this should help with using the regex pattern for parsing
    # after which we can go back to pattern1 to pull the commands
    new_raw_data = f"do(){raw_data}don't()"
    new_raw_data = "".join(re.findall(pattern2, new_raw_data))
    part2_data = re.findall(pattern1, new_raw_data)
    return part1_data, part2_data


def get_factors(command: str) -> list[int]:
    factors = re.findall(r"(\d+)", command)
    factors = [int(x) for x in factors]
    return factors


def get_part1_results(data: list[str]) -> int:
    total = 0
    for tmp_command in data:
        tmp_factors = get_factors(command=tmp_command)
        total += math.prod(tmp_factors)
    return total


@click.command()
@click.option("--test", is_flag=True)
@click.option("--part", "-p", type=click.Choice(['1', '2']))
def day3(test: bool, part: int) -> None:
    if test:
        print(f"Running with test data {part}...")
        if part == 1:
            raw_data = TEST_DATA1
        else:
            raw_data = TEST_DATA2
    else:
        print("Running with PROD data...")
        raw_data = get_data(day=3, year=2024)
    
    tm_logs = dict()

    parse_start_tm = time()
    part1_parsed_data, part2_parsed_data = get_parsed_data(raw_data=raw_data)
    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parsing_data'] = parse_dur

    if test:
        print(f"PART 1 DATA = {part1_parsed_data}")
        print(f"PART 2 DATA = {part2_parsed_data}")

    part1_start_tm = time()
    part1 = get_part1_results(data=part1_parsed_data)
    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()
    part2 = get_part1_results(data=part2_parsed_data)
    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    print(f"PART 1 = {part1}")
    print(f"PART 2 = {part2}")
    print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    day3()
