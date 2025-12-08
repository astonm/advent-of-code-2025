from util import *
import aoc

submit = aoc.for_day(7)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    grid = Grid([list(l) for l in read_file(input)])
    start = first(p for p, c in grid.walk() if c == "S")

    splits = 0
    beams = {(start[0], start[1] + 1)}
    while beams:
        next_beams = set()
        for beam in beams:
            grid.set(beam, "|")
            next_beam = (beam[0], beam[1] + 1)
            if next_beam not in grid:
                continue
            if grid.get(next_beam) == "^":
                splits += 1
                next_beams.add((next_beam[0] - 1, next_beam[1]))
                next_beams.add((next_beam[0] + 1, next_beam[1]))
            else:
                next_beams.add(next_beam)
        beams = next_beams

    return submit.part(1, splits)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    grid = Grid([list(l) for l in read_file(input)])
    start = first(p for p, c in grid.walk() if c == "S")

    splits = 0
    beams = {(start[0], start[1] + 1): 1}
    while beams:
        next_beams = Counter()
        for beam, n in beams.items():
            next_beam = (beam[0], beam[1] + 1)
            if next_beam not in grid:
                continue
            if grid.get(next_beam) == "^":
                splits += 1
                next_beams[(next_beam[0] - 1, next_beam[1])] += n
                next_beams[(next_beam[0] + 1, next_beam[1])] += n
            else:
                next_beams[next_beam] += n

        if next_beams:
            beams = next_beams
        else:
            return submit.part(2, sum(beams.values()))


if __name__ == "__main__":
    cli()
