import click
import re
from time import time
from aocd import get_data


TEST_DATA = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def get_parsed_data(raw_data: str, test: bool) -> list[list[int]]:
    parsed_data = list()
    lines = raw_data.split("\n")
    for ln in lines:
        tmp_nums = re.findall(r'(\d+)', ln)
        tmp_nums = [int(n) for n in tmp_nums]
        parsed_data.append(tmp_nums)
    return parsed_data


def get_report_diffs(report: list[int]) -> list[int]:
    report_diffs = list()
    for i in range(1, len(report)):
        report_diffs.append(report[i] - report[i - 1])
    return report_diffs


def check_monotonicity(report_diffs: list[int]) -> bool:
    return all([x > 0 for x in report_diffs]) or all([x < 0 for x in report_diffs])


def check_magnitude(report_diffs: list[int]) -> bool:
    return all([1 <= abs(x) <= 3 for x in report_diffs])


def is_safe_report(report_diffs: list[int]) -> bool:
    tmp_mono_chk = check_monotonicity(report_diffs=report_diffs)
    tmp_mag_chk = check_magnitude(report_diffs=report_diffs)
    return tmp_mono_chk & tmp_mag_chk


def is_almost_safe_report(report: list[int]) -> bool:
    for i in range(len(report)):
        tmp_new_report = [x for x in report]
        tmp_new_report.pop(i)
        tmp_new_report_diffs = get_report_diffs(report=tmp_new_report)
        if is_safe_report(report_diffs=tmp_new_report_diffs):
            return True
    return False


def how_many_safe_reports(reports: list[list[int]]) -> int:
    num_safe = 0
    for rpt in reports:
        tmp_report_diffs = get_report_diffs(report=rpt)
        if is_safe_report(report_diffs=tmp_report_diffs):
            num_safe += 1
    return num_safe


def how_many_almost_safe_reports(reports: list[list[int]], test: bool) -> int:
    num_safe = 0
    for rpt in reports:
        # first check is with all elements
        tmp_report_diffs = get_report_diffs(report=rpt)
        if is_safe_report(report_diffs=tmp_report_diffs):
            num_safe += 1
        else:
            # second check is by testing the removal of one element
            if is_almost_safe_report(report=rpt):
                num_safe += 1
    return num_safe


@click.command()
@click.option("--test", is_flag=True)
def day2(test: bool) -> None:
    tm_logs = dict()
    if test:
        print("Running with test data...")
        raw_data = TEST_DATA
    else:
        print("Running with PROD data...")
        raw_data = get_data(day=2, year=2024)
    
    parse_start_tm = time()
    parsed_data = get_parsed_data(raw_data=raw_data, test=test)
    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parsing_data'] = parse_dur
    if test:
        print(parsed_data)
    
    part1_start_tm = time()
    part1 = how_many_safe_reports(reports=parsed_data)
    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()
    part2 = how_many_almost_safe_reports(reports=parsed_data, test=test)
    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    print(f"PART 1 = {part1}")
    print(f"PART 2 = {part2}")
    print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    day2()
