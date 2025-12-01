from util import *
import aoc

submit = aoc.for_day(1)


@click.group()
def cli():
    pass


def process_line(line):
    return line[0], int(line[1:])


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    dial = 50
    c = 0
    for d, n in data:
        n *= -1 if d == "L" else 1
        dial = (dial + n) % 100
        c += dial == 0

    return submit.part(1, c)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    dial = 50
    c = 0
    for d, n in data:
        inc = -1 if d == "L" else 1
        for _ in range(n):
            dial = (dial + inc) % 100
            c += dial == 0

    return submit.part(2, c)


if __name__ == "__main__":
    cli()
