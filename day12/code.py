from util import *
import aoc

submit = aoc.for_day(12)


@click.group()
def cli():
    pass


class Shape(frozenset):
    def rotate(self):
        shifted = self.translate(-1, -1)
        rotated = Shape((-y, x) for (x, y) in shifted)
        unshifted = rotated.translate(+1, +1)
        return unshifted

    def translate(self, dx, dy):
        return Shape((s[0] + dx, s[1] + dy) for s in self)


def get_shape_rotations(grid):
    shape = Shape(p for p, c in grid.walk() if c == "#")

    out = set()
    for _ in range(4):
        out.add(shape)
        shape = shape.rotate()
    return out


@dataclass
class Region:
    width: int
    length: int
    shape_spec: tuple

    def all_points(self):
        return tuple(product(range(self.width), range(self.length)))


def process_section(section):
    lines = section.split("\n")
    if res := parse("{index:d}:", lines[0]):
        return get_shape_rotations(Grid(lines[1:]))
    else:
        out = []
        for line in lines:
            width, length, *shape_counts = ints(line)
            out.append(
                Region(
                    width=width,
                    length=length,
                    shape_spec=tuple(s for s in enumerate(shape_counts) if s[1] > 0),
                )
            )
    return out


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    *shapes, regions = [process_section(l) for l in read_file(input, "\n\n")]
    shape_rotations = {i: s for i, s in enumerate(shapes)}

    return submit.part(1, sum(1 for r in regions if fast_can_fit(r, shape_rotations)))


def can_fit(region, shape_rotations):
    class State(NamedTuple):
        free: tuple
        placed: tuple
        unplaced: tuple

    region_points = set(region.all_points())

    def inner(start):
        seen = set()
        q = [start]
        while q:
            curr = q.pop(0)

            if not curr.unplaced:
                return True

            # make sure there's no vertical gap between pieces
            max_y = max((p[1] for p in curr.placed), default=0)

            for shape_ind, shape_count in curr.unplaced:
                for rotation in shape_rotations[shape_ind]:
                    for offset_y in range(max_y + 1):
                        for offset_x in range(region.width):
                            shape = rotation.translate(offset_x, offset_y)

                            if len(set(curr.free) & shape) == len(shape):
                                next_free = tuple(
                                    p for p in curr.free if p not in shape
                                )

                                next_placed = curr.placed + tuple(shape)

                                unplaced = dict(curr.unplaced)
                                unplaced[shape_ind] -= 1
                                next_unplaced = tuple(
                                    (i, n) for (i, n) in unplaced.items() if n > 0
                                )

                                next_state = State(
                                    free=next_free,
                                    placed=next_placed,
                                    unplaced=next_unplaced,
                                )

                                if next_state not in seen:
                                    q.append(next_state)
                                    seen.add(next_state)

                                # only worry about placing a piece with minimal horizonal gap
                                break

    return inner(
        State(
            free=region_points,
            placed=tuple(),
            unplaced=tuple(region.shape_spec),
        )
    )


def fast_can_fit(region, shape_rotations):
    # the real thing is crazy slow! can get lucky though...
    points_in_region = region.width * region.length

    # case 1: the region is not big enough to fit the shapes, even if they tesselate perfectly
    points_needed = 0
    for i, n in region.shape_spec:
        points_needed += n * len(first(shape_rotations[i]))

    if points_needed > points_in_region:
        return False

    # case 2: the region is big enough to fit the shapes, even if they had no holes
    fittable_wide = region.width // 3
    fittable_high = region.length // 3
    total_shapes = sum(n for _, n in region.shape_spec)

    if total_shapes <= fittable_high * fittable_wide:
        return True

    # case 3, hard to know other than to do the slow thing
    return can_fit(region, shape_rotations)


if __name__ == "__main__":
    cli()
