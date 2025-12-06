from util import *
import aoc

submit = aoc.for_day(6)


@click.group()
def cli():
    pass


def process_line(line):
    nums = ints(line)
    if nums:
        return nums
    else:
        return line.split()


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    *transposed_nums, ops = [process_line(l) for l in read_file(input)]
    nums = list(zip(*transposed_nums))

    out = 0
    for op, vals in zip(ops, nums):
        if op == "+":
            out += sum(vals)
        else:
            out += prod(vals)

    return submit.part(1, out)


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    # . -> space hack because my editor strips trailing spaces
    *transposed_num_chars, ops = input.read().strip().replace(".", " ").split("\n")
    ops = ops.split()

    num_chars = list(zip(*transposed_num_chars))

    nums = []
    curr = []
    for line in num_chars:
        n = "".join(line).strip()
        if not n:
            nums.append(curr)
            curr = []
            continue
        curr.append(int(n))
    if curr:
        nums.append(curr)

    out = 0
    for op, vals in zip(ops, nums):
        if op == "+":
            out += sum(vals)
        else:
            out += prod(vals)

    return submit.part(2, out)


if __name__ == "__main__":
    cli()
