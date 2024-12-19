import click
from aocd import get_data
from collections import Counter
from time import time

TEST_DATA = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def get_parsed_data(raw_data: str):
    return [list(row) for row in raw_data.split("\n")]


def find_starting_loc(data: list[str]):
    rows, cols = len(data), len(data[0])
    for r in range(rows):
        for c in range(cols):
            if data[r][c] == "^":
                return r, c
    return None


class GuardMapper(object):

    def __init__(self, data: list[list[str]], test: bool):
        self.data = data
        self.test = test
        self.rows = None
        self.cols = None
        self.starting_loc = None
        self.prev_loc = None
        self.cur_loc = None
        self.cur_char = None
        self.guard = None
        self.leaving_map = False
        self.next_loc_adj_map = {
            "^": (-1, 0),
            ">": (0, 1),
            "v": (1, 0),
            "<": (0, -1)
        }
        self.visited = set()

    def set_rows_cols(self):
        self.rows = len(self.data)
        self.cols = len(self.data[0])

    def set_starting_loc(self):
        print("Finding starting location...")
        self.starting_loc = find_starting_loc(data=self.data)
        self.visited.add(self.starting_loc)
        print(f"Starting location found at {self.starting_loc}")

    def set_starting_char(self):
        self.guard = self.data[self.starting_loc[0]][self.starting_loc[1]]
        print(f"Guard = {self.guard}")

    def setup(self):
        self.set_rows_cols()
        self.set_starting_loc()
        self.set_starting_char()

    def get_next_loc(self):
        adj_r, adj_c = self.next_loc_adj_map[self.guard]
        self.prev_loc = (self.cur_loc[0], self.cur_loc[1])
        self.cur_loc = (self.cur_loc[0] + adj_r, self.cur_loc[1] + adj_c)

    def is_out_of_map(self):
        if (
            (self.cur_loc[0] < 0 and self.guard == "^") or
            (self.cur_loc[0] >= self.rows and self.guard == "v") or
            (self.cur_loc[1] < 0 and self.guard == "<") or
            (self.cur_loc[1] >= self.cols and self.guard == ">")
        ):
            return True
    
    def is_obstacle(self):
        if self.cur_char == "#":
            return True
    
    def update_visited(self):
        self.visited.add(self.prev_loc)
    
    def rotate_guard(self):
        if self.guard == "^":
            self.guard = ">"
        elif self.guard == ">":
            self.guard = "v"
        elif self.guard == "v":
            self.guard = "<"
        elif self.guard == "<":
            self.guard = "^"
    
    def check_next_loc(self):
        # first check if next loc is out of map
        if self.is_out_of_map():
            self.leaving_map = True
        else:
            # set next char
            self.cur_char = self.data[self.cur_loc[0]][self.cur_loc[1]]
            if self.is_obstacle():
                # rotate guard 90 degrees and reset cur loc to prev
                self.rotate_guard()
                self.cur_loc = (self.prev_loc[0], self.prev_loc[1])
    
    def traverse_map(self):
        self.cur_loc = (self.starting_loc[0], self.starting_loc[1])
        while not self.leaving_map:
            if self.test:
                print(f"PREV={self.prev_loc}, CUR={self.cur_loc}, VISITED={self.visited}")
            self.get_next_loc()
            self.check_next_loc()
            self.update_visited()

    def get_distinct_visited(self):
        return len(self.visited)
    
    def 


def part1_find_guard_positions(data: list[str], test: bool) -> int:
    guard_mapper = GuardMapper(data=data, test=test)
    guard_mapper.setup()
    guard_mapper.traverse_map()
    return guard_mapper.get_distinct_visited()


@click.command()
@click.option("--test", "-t", is_flag=True)
def day6(test: bool):
    if test:
        print("Running with TEST data...")
        raw_data = TEST_DATA
    else:
        print("Running with PROD data...")
        raw_data = get_data(day=6, year=2024)
    
    tm_logs = dict()

    parse_start_tm = time()
    parsed_data = get_parsed_data(raw_data=raw_data)
    parse_end_tm = time()
    parse_dur = parse_end_tm - parse_start_tm
    tm_logs['parse'] = parse_dur

    if test:
        print(f"PARSED DATA = {parsed_data}")

    part1_start_tm = time()
    part1 = part1_find_guard_positions(data=parsed_data, test=test)
    part1_end_tm = time()
    part1_dur = part1_end_tm - part1_start_tm
    tm_logs['part1'] = part1_dur

    part2_start_tm = time()

    part2_end_tm = time()
    part2_dur = part2_end_tm - part2_start_tm
    tm_logs['part2'] = part2_dur

    print(f"PART 1 = {part1}")
    # print(f"PART 2 = {}")
    # print(f"TIME LOGS = {tm_logs}")


if __name__ == "__main__":
    day6()
