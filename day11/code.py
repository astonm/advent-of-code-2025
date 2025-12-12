from util import *
import aoc

submit = aoc.for_day(11)


@click.group()
def cli():
    pass


def process_line(line):
    key, vals = line.split(": ")
    return key, vals.split()


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = dict(process_line(l) for l in read_file(input))

    @cache
    def count_ways(start, end):
        if start == end:
            return 1

        c = 0
        for child in data[start]:
            c += count_ways(child, end)
        return c

    return submit.part(1, count_ways("you", "out"))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    data = dict(process_line(l) for l in read_file(input))

    @cache
    def count_ways_avoid(start, end, avoid):
        if start == end:
            return 1

        if start in avoid:
            return 0

        c = 0
        for child in data[start]:
            c += count_ways_avoid(child, end, avoid)
        return c

    def assemble_path(path):
        start, mid1, mid2, end = path.split()
        return [
            count_ways_avoid(start, mid1, avoid=(mid2, end)),
            count_ways_avoid(mid1, mid2, avoid=(start, end)),
            count_ways_avoid(mid2, end, avoid=(mid1, start)),
        ]

    paths = ["svr dac fft out", "svr fft dac out"]
    return submit.part(2, sum(prod(assemble_path(p)) for p in paths))


if __name__ == "__main__":
    cli()
