from util import *
import aoc

submit = aoc.for_day(8)


@click.group()
def cli():
    pass


class JunctionBox(NamedTuple):
    x: int
    y: int
    z: int


def process_line(line):
    return JunctionBox(*ints(line))


def find_clique(start, graph):
    clique = set()
    q = [start]
    while q:
        curr = q.pop(0)
        clique.add(curr)
        for connection in graph[curr]:
            if connection not in clique:
                q.append(connection)
    return clique


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    N = 10 if "ex" in input.name else 1000
    jbs = [process_line(l) for l in read_file(input)]

    dists = [(dist(a, b), a, b) for a in jbs for b in jbs if a < b]
    dists.sort()
    dists = dists[:N]

    graph = defaultdict(set)
    for _, a, b in dists:
        graph[a].add(b)
        graph[b].add(a)

    cliques = []
    for jb in jbs:
        if any(jb in c for c in cliques):
            continue
        cliques.append(find_clique(jb, graph))

    clique_sizes = sorted([len(c) for c in cliques])

    return submit.part(1, prod(clique_sizes[-3:]))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    jbs = [process_line(l) for l in read_file(input)]

    dists = [(dist(a, b), a, b) for a in jbs for b in jbs if a < b]
    dists.sort()

    cliques = [{jb} for jb in jbs]

    for _, a, b in dists:
        next_cliques = []
        to_merge = []
        for clique in cliques:
            if a in clique or b in clique:
                to_merge.append(clique)
            else:
                next_cliques.append(clique)

        merged = set()
        for clique in to_merge:
            merged.update(clique)
        next_cliques.append(merged)

        if len(next_cliques) == 1:
            return submit.part(2, a.x * b.x)

        cliques = next_cliques


if __name__ == "__main__":
    cli()
