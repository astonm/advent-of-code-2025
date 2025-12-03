from util import *
import aoc

submit = aoc.for_day(3)


@click.group()
def cli():
    pass


def process_line(line):
    return list(line)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]
    out = 0
    for row in data:
        out += max(int(x + y) for i, x in enumerate(row) for y in row[i + 1 :])
    return submit.part(1, out)


def biggest_val(row, needed):
    if needed == 0:
        return ""

    for n in "987654321":
        if n not in row:
            continue

        first_idx, first_c = first((i, c) for i, c in enumerate(row) if c == n)
        if len(row) - first_idx >= needed:
            break

    return first_c + biggest_val(row[first_idx + 1 :], needed - 1)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input)]

    out = 0
    for i, row in enumerate(data):
        out += int(biggest_val(row, 12))
    return submit.part(2, out)


if __name__ == "__main__":
    cli()
