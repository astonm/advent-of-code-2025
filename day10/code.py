from util import *
import aoc
import networkx as nx

submit = aoc.for_day(10)


@click.group()
def cli():
    pass


@dataclass
class Machine:
    pattern: list
    buttons: list
    joltage: list


def process_line(line):
    pattern, rest = line.strip("[").split("]")
    rest, joltage = rest.rstrip("}").split("{")
    buttons = rest.strip().split(" ")

    return Machine(
        pattern=[c == "#" for c in pattern],
        buttons=[tuple(ints(b)) for b in buttons],
        joltage=ints(joltage),
    )


@cli.command()
@click.argument("input", type=click.File())
def part1(input):
    data = [process_line(l) for l in read_file(input)]

    def fewest_presses(machine):
        for button_presses in powerset(range(len(machine.buttons))):
            light_count = [0 for _ in range(len(machine.pattern))]
            for b in button_presses:
                for l in machine.buttons[b]:
                    light_count[l] += 1

            if machine.pattern == [c % 2 == 1 for c in light_count]:
                return len(button_presses)

    return submit.part(1, sum(fewest_presses(machine) for machine in data))


@cli.command()
@click.argument("input", type=click.File())
def part2(input):
    # this is so slow...
    data = [process_line(l) for l in read_file(input)]

    def min_presses(machine):
        joltage = tuple(machine.joltage)

        @cache
        def inner(target):
            # easy case, everything zero
            nonzero_inds = tuple(i for i, t in enumerate(target) if t != 0)
            if not nonzero_inds:
                return 0  # yay

            # next easy case, every nonzero thing the same and aligns with a button
            if len(set(target)) == 2 and nonzero_inds in machine.buttons:
                return max(target)

            # convert buttons to 1-hot encoding and check on bail-out cases
            max_presses = {}
            hot_buttons = defaultdict(list)
            for button in machine.buttons:
                min_target = min(t for i, t in enumerate(target) if i in button)
                if min_target == 0:  # can't press this button anymore
                    continue
                one_hot = tuple(int(i in button) for i in range(len(target)))
                max_presses[one_hot] = min_target
                for ind in button:
                    hot_buttons[ind].append(one_hot)

            # look for non-zero target value where all button options have been eliminated
            if any(not hot_buttons[i] for i in nonzero_inds):
                return inf

            # look for cases where pressing all possible buttons still isn't enough
            for i, t in enumerate(target):
                up_to = sum(max_presses[b] for b in hot_buttons[i])
                if up_to < t:
                    return inf

            # look for cases where pressing any combination of buttons is too much
            for i, button_set in hot_buttons.items():
                overlap = tuple(int(all(x)) for x in zip(*button_set))
                if any(t < target[i] for (o, t) in zip(overlap, target) if o == 1):
                    return inf

            combos = [
                (num_stars_n_bars(target[i], len(hot_buttons[i])), i)
                for i in nonzero_inds
            ]
            _, best_ind = min((n, i) for n, i in combos if i in nonzero_inds)
            n_presses = target[best_ind]
            to_press = hot_buttons[best_ind]

            out = inf
            for button_press_counts in stars_n_bars(n_presses, len(to_press)):
                next_target = target
                for n, button in zip(button_press_counts, to_press):
                    next_target = tuple(t - n * b for t, b in zip(next_target, button))

                if any(t < 0 for t in next_target):
                    continue
                assert next_target[best_ind] == 0

                out = min(out, n_presses + inner(next_target))

            return out

        return inner(joltage)

    out = 0
    for machine in tqdm(data):
        t0 = time.time()
        res1 = min_presses(machine)
        dt = time.time() - t0
        if dt > 1:
            print(
                "{" + ",".join(str(j) for j in machine.joltage) + "}",
                res1,
                dt,
                file=sys.stderr,
            )
        out += res1
    print(out)


def stars_n_bars(items, bins):
    # a la https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)
    dividers = bins - 1
    for inds in combinations(range(1, items + dividers + 1), dividers):
        pts = (0,) + inds + (items + dividers + 1,)
        gaps = tuple(b - a - 1 for a, b in pairwise(pts))
        yield gaps


def num_stars_n_bars(items, bins):
    dividers = bins - 1
    return comb(items + dividers, dividers)


if __name__ == "__main__":
    cli()
