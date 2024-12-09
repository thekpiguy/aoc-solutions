import click
import re
from aocd import get_data
from collections import Counter

TEST_DATA = """3   4
4   3
2   5
1   3
3   9
3   3"""


def parse_data(data: str) -> tuple[list[int]]:

    lines = data.split("\n")
    nums1, nums2 = list(), list()
    for ln in lines:
        tmp_nums = re.findall(r'(\d+)', ln)
        tmp_num1, tmp_num2 = int(tmp_nums[0]), int(tmp_nums[1])
        nums1.append(tmp_num1)
        nums2.append(tmp_num2)

    nums1, nums2 = sorted(nums1), sorted(nums2)

    return nums1, nums2


def get_total_distance(nums1: list[int], nums2: list[int]) -> int:

    total_dist = 0

    for i in range(len(nums1)):
        tmp_diff = abs(nums1[i] - nums2[i])
        total_dist += tmp_diff

    return total_dist


def get_similarity_score(nums1: list[int], nums2: list[int]) -> int:

    similarity = 0
    nums2_ctr = Counter(nums2)
    
    for _, el in enumerate(nums1):
        similarity += (el * nums2_ctr[el])

    return similarity


@click.command()
@click.option('--test', is_flag=True)
def day1(test: bool) -> None:
    if test:
        raw_data = TEST_DATA

    else:
        raw_data = get_data(day=1, year=2024)
    
    num_list1, num_list2 = parse_data(data=raw_data)

    if test:
        print(num_list1)
        print()
        print(num_list2)

    part1 = get_total_distance(nums1=num_list1, nums2=num_list2)
    part2 = get_similarity_score(nums1=num_list1, nums2=num_list2)
    print(f"PART1 = {part1}")
    print(f"PART2 = {part2}")


if __name__ == "__main__":
    day1()
