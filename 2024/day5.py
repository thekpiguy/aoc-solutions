import click
from aocd import get_data
from collections import defaultdict
from time import time

TEST_DATA = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def get_ordering_rules(raw_rules: str):
    rules = defaultdict(list)
    for ln in raw_rules.split("\n"):
        pg1, pg2 = ln.split("|")
        pg1, pg2 = int(pg1), int(pg2)
        rules[pg1].append(pg2)
    return rules


def get_updates(raw_updates: str):
    updates = list()
    for ln in raw_updates.split("\n"):
        updates.append([int(x) for x in ln.split(",")])
    return updates


def get_parsed_data(raw_data: str):
    raw_rules, raw_updates = raw_data.split("\n\n")
    ordering_rules = get_ordering_rules(raw_rules=raw_rules)
    updates = get_updates(raw_updates=raw_updates)
    return ordering_rules, updates


def validate_update(update: list[int], rules: dict):
    checks = list()
    for i in range(0, len(update) - 1):
        cur_pg, nex_pg = update[i], update[i + 1]
        checks.append(nex_pg in rules[cur_pg])
    return all(checks)


def get_middle_page(update: list[int]) -> int:
    update_size = len(update)
    return update[update_size // 2]


def get_corrected_update(update: list[int], rules: dict) -> list[int]:
    """
    Idea is to stay on first position and let right index iterate to the end
    to ensure rules are met. Then increase the left index and repeat.
    Ex that helped: https://github.com/RD-Dev-29/advent_of_code_24/blob/main/code_files/day5.py
    """
    cur_i, nex_i, upd_size = 0, 1, len(update)
    corr_upd = [x for x in update]
    while nex_i < upd_size:
        #print(f"CUR_I={cur_i}, NEX_I={nex_i}")
        if corr_upd[nex_i] not in rules[corr_upd[cur_i]]:
            corr_upd[cur_i], corr_upd[nex_i] = corr_upd[nex_i], corr_upd[cur_i]
            #print(f"CORR ITER ({cur_i},{nex_i})= {corr_upd}")
        nex_i += 1
        if nex_i == upd_size:
            cur_i += 1
            nex_i = cur_i + 1
    return corr_upd


def part1_sum_of_middle_page_valid_updates(updates: list[int], rules: dict) -> int:
    total = 0
    for upd in updates:
        if validate_update(update=upd, rules=rules):
            total += get_middle_page(update=upd)
    return total


def part2_sum_of_middle_page_corrected_updates(updates: list[int], rules: dict) -> int:
    total = 0
    for upd in updates:
        if not validate_update(update=upd, rules=rules):
            print("Correcting update...")
            corrected_upd = get_corrected_update(update=upd, rules=rules)
            total += get_middle_page(update=corrected_upd)
            print(f"ORIG={upd}, CORRECTED={corrected_upd}")
    return total


@click.command()
@click.option("--test", "-t", is_flag=True)
def day5(test: bool):
    if test:
        print(f"Running with TEST data...")
        raw_data = TEST_DATA
    else:
        print(f"Running with PROD data...")
        raw_data = get_data(day=5, year=2024)
    
    tm_logs = dict()

    parse_start_tm = time()
    ordering_rules, updates = get_parsed_data(raw_data=raw_data)
    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parse'] = parse_dur
    if test:
        print(f"ORDERING RULES = {ordering_rules}")
        print(f"UPDATES = {updates}")

    part1_start_tm = time()
    part1 = part1_sum_of_middle_page_valid_updates(updates=updates, rules=ordering_rules)
    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()
    part2 = part2_sum_of_middle_page_corrected_updates(updates=updates, rules=ordering_rules)
    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    print(f"PART1 = {part1}")
    print(f"PART2 = {part2}")
    print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    day5()
