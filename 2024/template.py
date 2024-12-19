import click
from aocd import get_data
from time import time

TEST_DATA = """"""


@click.command()
@click.option("--test", "-t", is_flag=True)
def dayN(test: bool):
    if test:
        print("Running with TEST data...")
    else:
        print("Running with PROD data...")
    
    tm_logs = dict()

    parse_start_tm = time()

    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parse'] = parse_dur

    part1_start_tm = time()

    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()

    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    # print(f"PART 1 = {}")
    # print(f"PART 2 = {}")
    # print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    dayN()
