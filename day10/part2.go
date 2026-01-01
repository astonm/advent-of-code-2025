package main

import (
    "bufio"
    "fmt"
    "iter"
    "math"
    "os"
    "slices"
    "strconv"
    "strings"
)

const IMPOSSIBLE int = math.MaxInt

type Machine struct {
    Buttons [][]int
    Joltage []int
}

func main() {
    out := 0
    scanner := bufio.NewScanner(os.Stdin)
    for scanner.Scan() {
        machine := processLine(scanner.Text())
        minPresses := getMinPresses(machine)

        fmt.Println(machine.Joltage, minPresses)
        out += minPresses
    }
    fmt.Println(out)
}

func processLine(line string) Machine {
    var r []string
    var rest string

    r = strings.Split(line, "]")
    rest = r[1]

    r = strings.Split(strings.Trim(rest, "}"), "{")
    rest, joltageDesc := r[0], r[1]

    buttonsDesc := strings.Split(strings.Trim(rest, " "), " ")

    atois := func(a []string) []int {
        is := make([]int, 0)
        for _, n := range a {
            i, err := strconv.Atoi(n)
            if err != nil {
                panic(err)
            }
            is = append(is, i)
        }
        return is
    }

    buttons := make([][]int, 0)
    for _, desc := range buttonsDesc {
        inds := strings.Split(desc[1:len(desc)-1], ",")
        buttons = append(buttons, atois(inds))
    }

    joltage := strings.Split(joltageDesc, ",")

    return Machine{
        Buttons: buttons,
        Joltage: atois(joltage),
    }
}

func getMinPresses(machine Machine) int {
    // cache?
    var inner func([]int) int
    inner = func(target []int) int {
        var nonZeroInds []int
        uniqueVals := make(map[int]struct{})

        for i, x := range target {
            if x != 0 {
                nonZeroInds = append(nonZeroInds, i)
            } else {
                uniqueVals[x] = struct{}{}
            }
        }

        if len(nonZeroInds) == 0 {
            return 0 // solved!
        }

        for _, b := range machine.Buttons {
            if slices.Equal(nonZeroInds, b) && len(uniqueVals) == 2 {
                // only need to press one button to solve
                return target[nonZeroInds[0]]
            }
        }

        maxPresses := make(map[int]int)
        pressable := make(map[int][]int)
        for buttonInd, button := range machine.Buttons {
            minTarget := IMPOSSIBLE
            for _, targetInd := range button {
                minTarget = min(minTarget, target[targetInd])
            }
            if minTarget == 0 { // can't press this button anymore
                continue
            }
            maxPresses[buttonInd] = minTarget
            for _, targetInd := range button {
                pressable[targetInd] = append(pressable[targetInd], buttonInd)
            }
        }

        // look for cases where pressing all possible buttons still isn't enough
        for _, targetInd := range nonZeroInds {
            if len(pressable[targetInd]) == 0 {
                return IMPOSSIBLE
            }

            var upTo int
            for _, buttonInd := range pressable[targetInd] {
                upTo += maxPresses[buttonInd]
            }
            if upTo < target[targetInd] {
                return IMPOSSIBLE
            }
        }

        // look for cases where pressing any combination of buttons is too much
        for targetInd, buttonInds := range pressable {
            for i := range len(target) {
                inAllButtons := true
                for _, buttonInd := range buttonInds {
                    if !slices.Contains(machine.Buttons[buttonInd], i) {
                        inAllButtons = false
                        break
                    }
                }

                if inAllButtons && target[i] < target[targetInd] {
                    return IMPOSSIBLE
                }
            }
        }

        // calculate combinations that can get us there and choose smallest to start
        bestInd, bestIndCombos := -1, int64(math.MaxInt64)
        for _, targetInd := range nonZeroInds {
            combos := numStarsAndBars(target[targetInd], len(pressable[targetInd]))
            if combos < bestIndCombos {
                bestIndCombos = combos
                bestInd = targetInd
            }
        }

        nPresses := target[bestInd]
        toPress := pressable[bestInd]

        // recurse after zeroing out one part of target
        out := IMPOSSIBLE
        for buttonPressCounts := range starsAndBars(nPresses, len(toPress)) {
            nextTarget := slices.Clone(target)
            for i := range len(buttonPressCounts) {
                nButtonPresses := buttonPressCounts[i]

                buttonInd := toPress[i]
                button := machine.Buttons[buttonInd]

                for _, targetInd := range button {
                    nextTarget[targetInd] -= nButtonPresses
                }
            }

            valid := true
            for _, t := range nextTarget {
                if t < 0 {
                    valid = false
                    break
                }
            }

            if !valid {
                continue
            }

            next := inner(nextTarget)
            if next != IMPOSSIBLE {
                out = min(out, nPresses+next)
            }
        }

        return out
    }
    return inner(machine.Joltage)
}

func factorial(n int) int64 {
    out := int64(1)
    for i := 2; i <= n; i++ {
        out *= int64(i)
    }
    return out
}

func comb(_n, _k int) int64 {
    // via https://github.com/gonum/gonum/blob/9b1a85bc89eb0f91671fd4a27fb38eb16dab63e4/stat/combin/combin.go#L29
    n, k := int64(_n), int64(_k)
    if k > n/2 {
        k = n - k
    }

    b := int64(1)
    for i := int64(1); i <= k; i++ {
        b = (n - k + i) * b / i
    }

    return b
}

func combinations(n int, r int) iter.Seq[[]int] {
    return func(yield func([]int) bool) {
        if r > n {
            return
        }

        indices := make([]int, 0, r)
        for i := range r {
            indices = append(indices, i)
        }

        yield(indices)

        for {
            var i int
            var found bool
            for i = r - 1; i >= 0; i-- {
                if indices[i] != i+n-r {
                    found = true
                    break
                }
            }

            if !found {
                return
            }

            indices[i]++
            for j := i + 1; j < r; j++ {
                indices[j] = indices[j-1] + 1
            }

            yield(indices)
        }
    }
}

func numStarsAndBars(nItems, nBins int) int64 {
    nDividers := nBins - 1
    return comb(nItems+nDividers, nDividers)
}

func starsAndBars(nItems, nBins int) iter.Seq[[]int] {
    // a la https://en.wikipedia.org/wiki/Stars_and_bars_(combinatorics)
    nDividers := nBins - 1
    return func(yield func([]int) bool) {
        for inds := range combinations(nItems+nDividers, nDividers) {
            prev := -1
            gaps := []int{}
            for _, i := range inds {
                gaps = append(gaps, i-prev-1)
                prev = i
            }
            gaps = append(gaps, nItems+nDividers-prev-1)
            yield(gaps)
        }
    }
}
