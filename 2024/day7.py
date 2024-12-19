import click
import re
from aocd import get_data
from collections import defaultdict
from itertools import product
from pprint import pprint
from time import time

TEST_DATA = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

OPERATORS = [
    "+",
    "*"
]

OPERATORS2 = [
    "+",
    "*",
    "||"
]


def get_parsed_data(raw_data: str) -> dict:
    data = dict()
    for ln in raw_data.split("\n"):
        test_val, pcs = ln.split(": ")
        test_val = int(test_val)
        data[test_val] = pcs
    return data


def get_equations(data: dict, operators: list[str]) -> dict:
    eqs_dict = defaultdict(list)
    for test_val, pcs in data.items():
        num_spots = len(pcs.split(" ")) - 1
        for tmp_op in product(operators, repeat=num_spots):
            # print(f"OP={tmp_op}")
            new_pcs = str(pcs)
            for i in range(len(tmp_op)):
                new_pcs = new_pcs.replace(" ", f"{tmp_op[i]}", 1)
            tmp_eq_dict = {
                'orig': pcs,
                'new': new_pcs,
                'ops': tmp_op
            }
            eqs_dict[test_val].append(tmp_eq_dict)
    return eqs_dict


def evaluate_equation(eq: str, ops: tuple) -> int:
    pcs = [int(x) for x in eq.split(" ")]
    if len(pcs) == 1:
        return pcs[0]
    result = pcs[0]
    for i in range(1, len(pcs)):
        tmp_comp = pcs[i]
        tmp_op = ops[i - 1]
        if tmp_op == "+":
            result += tmp_comp
        elif tmp_op == "*":
            result *= tmp_comp
        else:
            print("WTH...")
    return result


def evaluate_equation_with_concat(eq: str, ops: tuple) -> int:
    pcs = [int(x) for x in eq.split(" ")]
    if len(pcs) == 1:
        return pcs[0]
    result = pcs[0]
    for i in range(1, len(pcs)):
        tmp_comp = pcs[i]
        tmp_op = ops[i - 1]
        if tmp_op == "+":
            result += tmp_comp
        elif tmp_op == "*":
            result *= tmp_comp
        elif tmp_op == "||":
            result = int(f"{result}{tmp_comp}")
        else:
            print("WTH...")
    return result


def filter_equations(equations: dict) -> dict:
    valid_eqs = defaultdict(list)
    for test_val, tmp_eqs in equations.items():
        for tmp_eq_dict in tmp_eqs:
            # tmp_rslt = evaluate_equation(eq=tmp_eq_dict['orig'], ops=tmp_eq_dict['ops'])
            tmp_rslt = evaluate_equation_with_concat(eq=tmp_eq_dict['orig'], ops=tmp_eq_dict['ops'])
            if test_val == tmp_rslt:
                valid_eqs[test_val].append(tmp_eq_dict)
    return valid_eqs


def part1_get_sum_test_values(data: dict) -> int:
    eqs_dict = get_equations(data=data, operators=OPERATORS)
    valid_eqs_dict = filter_equations(equations=eqs_dict)
    return sum(valid_eqs_dict.keys())


def part2_get_sum_test_values(data: dict, test: bool) -> int:
    eqs_dict = get_equations(data=data, operators=OPERATORS2)
    valid_eqs_dict = filter_equations(equations=eqs_dict)
    if test:
        print(f"VALID EQUATIONS")
        pprint(valid_eqs_dict)
    return sum(valid_eqs_dict.keys())


@click.command()
@click.option("--test", "-t", is_flag=True)
def day7(test: bool):
    if test:
        print("Running with TEST data...")
        raw_data = TEST_DATA
    else:
        print("Running with PROD data...")
        raw_data = get_data(day=7, year=2024)
    
    tm_logs = dict()

    parse_start_tm = time()
    parsed_data = get_parsed_data(raw_data=raw_data)
    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parse'] = parse_dur

    if test:
        print(f"DATA = {parsed_data}")

    part1_start_tm = time()
    part1 = part1_get_sum_test_values(data=parsed_data)
    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()
    part2 = part2_get_sum_test_values(data=parsed_data, test=test)
    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    print(f"PART 1 = {part1}")
    print(f"PART 2 = {part2}")
    print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    day7()
