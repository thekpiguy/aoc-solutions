import click
from aocd import get_data


@click.command()
@click.option("--test", "-t", is_flag=True)
def dayN():
    pass

if __name__ == "__main__":
    dayN()
