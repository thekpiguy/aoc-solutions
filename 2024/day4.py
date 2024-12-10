import click
from time import time
from aocd import get_data

TEST_DATA = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

XMAS = "XMAS"
MAS = "MAS"
SAM = "SAM"


def get_parsed_data(raw_data: str) -> list[str]:
    return [list(x) for x in raw_data.split("\n")]


def get_dims(data: list[str]) -> tuple[int]:
    rows = len(data)
    cols = len(data[0])
    return rows, cols


def check_n(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i - adj][cur_j])
    substr = "".join(elmts)
    return substr == XMAS


def check_ne(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i - adj][cur_j + adj])
    substr = "".join(elmts)
    return substr == XMAS


def check_e(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i][cur_j + adj])
    substr = "".join(elmts)
    return substr == XMAS


def check_se(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i + adj][cur_j + adj])
    substr = "".join(elmts)
    return substr == XMAS


def check_s(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i + adj][cur_j])
    substr = "".join(elmts)
    return substr == XMAS


def check_sw(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i + adj][cur_j - adj])
    substr = "".join(elmts)
    return substr == XMAS


def check_w(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i][cur_j - adj])
    substr = "".join(elmts)
    return substr == XMAS


def check_nw(data: list[str], cur_i: int, cur_j: int) -> bool:
    elmts = list()
    for adj in range(4):
        elmts.append(data[cur_i - adj][cur_j - adj])
    substr = "".join(elmts)
    return substr == XMAS


def get_block(data: list[str], cur_i: int, cur_j: int, n: int) -> list[str]:
    block = list()
    row_sub = data[cur_i:cur_i+n]
    for adj in range(n):
        block.append(row_sub[adj][cur_j:cur_j+n])
    return block


def check_block_for_x_mas(block: list[str]) -> bool:
    diag1_elmts = list()
    for adj in range(3):
        diag1_elmts.append(block[0 + adj][0 + adj])
    diag1_substr = "".join(diag1_elmts)

    diag2_elmts = list()
    for adj in range(3):
        diag2_elmts.append(block[0 + adj][2 - adj])
    diag2_substr = "".join(diag2_elmts)

    diag1_x_mas = (diag1_substr == MAS) or (diag1_substr == SAM)
    diag2_x_mas = (diag2_substr == MAS) or (diag2_substr == SAM)

    return diag1_x_mas and diag2_x_mas


def part1_how_many_xmas(data: list[str]) -> int:
    rows, cols = get_dims(data=data)
    total_xmas = 0

    for r in range(rows):
        for c in range(cols):
            if 3 <= r < rows:
                total_xmas += int(check_n(data=data, cur_i=r, cur_j=c))
            if 3 <= r < rows and 0 <= c < cols - 3:
                total_xmas += int(check_ne(data=data, cur_i=r, cur_j=c))
            if 0 <= c < cols - 3:
                total_xmas += int(check_e(data=data, cur_i=r, cur_j=c))
            if 0 <= r < rows - 3 and 0 <= c < cols - 3:
                total_xmas += int(check_se(data=data, cur_i=r, cur_j=c))
            if 0 <= r < rows - 3:
                total_xmas += int(check_s(data=data, cur_i=r, cur_j=c))
            if 0 <= r < rows - 3 and 3 <= c < cols:
                total_xmas += int(check_sw(data=data, cur_i=r, cur_j=c))
            if 3 <= c < cols:
                total_xmas += int(check_w(data=data, cur_i=r, cur_j=c))
            if 3 <= r < rows and 3 <= c < cols:
                total_xmas += int(check_nw(data=data, cur_i=r, cur_j=c))
    
    return total_xmas


def part2_how_many_x_mas(data: list[str]) -> int:
    rows, cols = get_dims(data=data)
    total_x_mas = 0

    for r in range(rows - 2):
        for c in range(cols - 2):
            cur_block = get_block(data=data, cur_i=r, cur_j=c, n=3)
            total_x_mas += int(check_block_for_x_mas(block=cur_block))
    
    return total_x_mas


@click.command()
@click.option("--test", "-t", is_flag=True)
def day4(test: bool) -> None:
    if test:
        print("Running with test data...")
        raw_data = TEST_DATA
    else:
        print("Running with PROD data...")
        raw_data = get_data(day=4, year=2024)
    
    tm_logs = dict()

    parse_start_tm = time()
    parsed_data = get_parsed_data(raw_data=raw_data)
    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parsing'] = parse_dur

    if test:
        print("**** DATA ****")
        print(parsed_data)

    part1_start_tm = time()
    part1_xmas = part1_how_many_xmas(data=parsed_data)
    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()
    part2_xmas = part2_how_many_x_mas(data=parsed_data)
    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    print(f"PART1 = {part1_xmas}")
    print(f"PART2 = {part2_xmas}")
    print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    day4()
