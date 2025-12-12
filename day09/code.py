from util import *
import aoc

from PIL import Image, ImageColor

submit = aoc.for_day(9)


@click.group()
def cli():
    pass


def process_line(line):
    return Vector(ints(line))


def get_area(p1, p2):
    inclusive = Vector([1, 1])
    rect = abs(p1 - p2) + inclusive
    return rect[0] * rect[1]


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    poly = [process_line(l) for l in read_file(input)]
    areas = [get_area(x, y) for x in poly for y in poly if x != y]
    return submit.part(1, max(areas))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    # my input (zoomed out) looks like a big left-facing pacman
    """
    ......*******.......
    ....***.....****....
    ...**..........**...
    ..**............**..
    .**..............**.
    .*................*.
    **................**
    *..................*
    *..................*
    *****************..*
    *****************..*
    *..................*
    *..................*
    **................**
    .*................*.
    .**..............**.
    ..**............**..
    ...**..........**...
    ....***......***....
    ......********......
    """
    poly = [process_line(l) for l in read_file(input)]
    edges = get_edges(poly)

    # start by finding the middle two horiz line segments because they're longest
    sides = [sorted((p1, p2)) for p1, p2 in pairwise(poly)]
    long_sides = [s for s in sides if abs(s[0][0] - s[1][0]) > 10_000]

    mid_y = inf
    if long_sides:  # handle small example, too
        hi_jaw, lo_jaw = sorted(long_sides, key=lambda s: abs(s[0][0] - s[1][0]))[-2:]
        hi_y, lo_y = hi_jaw[0][1], lo_jaw[0][1]
        mid_y = (hi_y + lo_y) // 2

    best_area = 0
    best_coords = None

    for p1, p2 in combinations(poly, 2):
        if p1 == p2:
            continue

        # don't cross the middle
        if (p1[1] > mid_y) != (p2[1] > mid_y):
            continue

        # check corners
        corners = [
            Vector([p1[0], p1[1]]),
            Vector([p2[0], p1[1]]),
            Vector([p2[0], p2[1]]),
            Vector([p1[0], p2[1]]),
        ]
        if not all([poly_contains(edges, poly, c) for c in corners]):
            continue

        area = get_area(p1, p2)
        if area > best_area:
            best_area = area
            best_coords = (p1, p2)

    print(best_coords)
    print(best_area)


def close_loop(points):
    return list(points) + [points[0]]


def get_edges(poly):
    edges = set()
    for l1, l2 in pairwise(close_loop(poly)):
        diff = l2 - l1
        size = max(abs(diff))
        if size:
            d = diff // size
            for i in range(size):
                p = l1 + i * d
                edges.add(tuple(p))
    return edges


def poly_contains(edges, poly, p, CACHE={}):
    if tuple(p) in edges:
        return True
    px, py = p

    # CACHE stores hittable vertical walls for each line
    if py not in CACHE:
        # we can do a ton of work up front
        CACHE[py] = []
        for l1, l2 in pairwise(close_loop(poly)):
            if l1[1] == l2[1]:
                continue  # ignore horizontal lines
            ly1, ly2 = l1[1], l2[1]
            if ly1 > ly2:
                ly1, ly2 = ly2, ly1
            if ly1 < py <= ly2:
                CACHE[py].append(l1[0])

    c = 0
    for lx in CACHE[py]:
        if px <= lx:
            c += 1

    return c % 2 == 1


@cli.command()
@click.argument("input", type=click.File())
def drawpng(input):
    solution = ([10000, 10000], [50000, 50000])  # a solution to sketch
    FACTOR = 100  # zoom out!

    def process_line(line):
        return Vector(ints(line)) // FACTOR

    poly = [process_line(l) for l in read_file(input)]

    grid = GridN(default=".")

    for p1, p2 in pairwise(close_loop(poly)):
        for p in line_segment_points(p1, p2):
            grid.set(p, "*")

    a, b = solution
    corners = [
        Vector([a[0], a[1]]) // FACTOR,
        Vector([b[0], a[1]]) // FACTOR,
        Vector([b[0], b[1]]) // FACTOR,
        Vector([a[0], b[1]]) // FACTOR,
    ]
    for s1, s2 in pairwise(close_loop(corners)):
        for s in line_segment_points(s1, s2):
            grid.set(s, "#")

    bounds = grid.bounds()
    size = tuple(b.stop for b in bounds)
    with Image.new("RGBA", size, ImageColor.getcolor("white", "RGBA")) as im:
        pixels = im.load()
        colors = {
            ".": ImageColor.getcolor("white", im.mode),
            "#": ImageColor.getcolor("red", im.mode),
            "*": ImageColor.getcolor("blue", im.mode),
        }

        for p, c in grid.walk():
            pixels[p] = colors[c]

    im.save("out.png")


def line_segment_points(l1, l2):
    out = []

    diff = l2 - l1
    size = max(abs(diff))
    if size:
        step = diff // size
        for i in range(0, size + 1):
            out.append(l1 + i * step)

    return out


if __name__ == "__main__":
    cli()
