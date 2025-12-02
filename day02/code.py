from util import *
import aoc

submit = aoc.for_day(2)


@click.group()
def cli():
    pass


def process_line(line):
    start, end = [int(x) for x in line.split("-")]
    return range(start, end + 1)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input, delim=",")]
    out = 0
    for rng in data:
        for n in rng:
            ns = str(n)
            middle = len(ns) // 2
            if ns[:middle] == ns[middle:]:
                out += n
    return submit.part(1, out)


def get_splits(s, n_splits):
    s = str(s)
    l = len(s)
    if l % n_splits != 0:
        return None

    split_size = l // n_splits
    parts = ["".join(g) for g in grouper(s, split_size)]
    return parts


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = [process_line(l) for l in read_file(input, delim=",")]

    out = 0
    for rng in data:
        for n in rng:
            ns = str(n)
            for i in range(2, len(ns) + 1):
                splits = get_splits(n, i)
                if splits and all(s == splits[0] for s in splits):
                    out += n
                    break

    return submit.part(2, out)


if __name__ == "__main__":
    cli()
