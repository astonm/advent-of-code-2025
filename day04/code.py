from util import *
import aoc

submit = aoc.for_day(4)


@click.group()
def cli():
    pass


def process_line(line):
    return list(line)


def find_accessible(grid):
    out = []
    for p, c in grid.walk():
        num_rolls = sum(1 for q in grid.neighbors(p, diags=True) if grid.get(q) == "@")
        if c == "@" and num_rolls < 4:
            out.append(p)
    return out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid([process_line(l) for l in read_file(input)])
    return submit.part(1, ilen(find_accessible(grid)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid([process_line(l) for l in read_file(input)])

    removed = 0
    while to_remove := find_accessible(grid):
        for p in to_remove:
            grid.set(p, ".")
            removed += 1

    return submit.part(2, removed)


if __name__ == "__main__":
    cli()
