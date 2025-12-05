from util import *
import aoc

submit = aoc.for_day(5)


@click.group()
def cli():
    pass


def process_range(line):
    start, end = [int(x) for x in line.split("-")]
    assert start <= end
    return range(start, end + 1)


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    parts = input.read().split("\n\n")
    ranges = [process_range(l) for l in parts[0].split()]
    ingredients = [int(l) for l in parts[1].split()]

    return submit.part(1, sum(1 for i in ingredients if any(i in r for r in ranges)))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    parts = input.read().split("\n\n")
    ranges = [process_range(l) for l in parts[0].split()]

    class UnionSet:
        def __init__(self, sets=None):
            self.sets = []
            if sets:
                for s in sets:
                    self.add(s)

        def add(self, other):
            next_sets = []
            to_add = other
            for s in self.sets:
                overlap = (
                    # some end in the other
                    (to_add.start in s or (to_add.stop - 1) in s)
                    or (s.start in to_add or (s.stop - 1) in to_add)
                )

                if overlap:
                    to_add = range(
                        min(s.start, to_add.start),
                        max(s.stop, to_add.stop),
                    )
                else:
                    next_sets.append(s)
            next_sets.append(to_add)

            self.sets = next_sets

        def __len__(self):
            return sum(len(s) for s in self.sets)

    return submit.part(2, len(UnionSet(ranges)))


if __name__ == "__main__":
    cli()
