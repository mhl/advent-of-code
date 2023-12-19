import { getExampleLines, getInputLines } from "../aoc";

// I got stuck on this part, so this is basically me typing out
// this solution https://gist.github.com/Nathan-Fenner/781285b77244f06cf3248a04869e7161
// checking that I understood it along the way.

let cache: Map<string, number> = new Map();

function getCacheKey(pattern: string, counts: number[]) {
    return `${pattern}-${counts.join(",")}`;
}

function getPossibleSolutions(
    pattern: string,
    counts: number[],
    depth: number = 0,
): number {
    // console.log(" ".repeat(depth), `===== considering ${pattern} and ${counts}`);
    const key = getCacheKey(pattern, counts);
    const cached = cache.get(key);
    if (cached != null) {
        return cached;
    }

    // If you've run out of characters in the pattern, this
    // is only possible if you've also found all the runs
    // already.
    if (pattern.length === 0) {
        return counts.length > 0 ? 0 : 1;
    }

    // If you've run out of counts, then this is only possible
    // if there are no #s in the rest. (And there's only one way
    // for it to have no #s otherwise - all the ?s have to be .s.
    if (counts.length === 0) {
        return pattern.indexOf("#") >= 0 ? 0 : 1;
    }

    // The length of the pattern must be at least the length of
    // the all the runs left and the .s that must be between them
    const springs_left = counts.reduce((s, n) => s + n, 0);
    if (pattern.length < springs_left + counts.length - 1) {
        return 0;
    }

    // Consider the cases for what the first character might be
    // - either ?, . or #
    if (pattern[0] === ".") {
        const result = getPossibleSolutions(
            pattern.slice(1),
            counts,
            depth + 1,
        );
        cache.set(getCacheKey(pattern, counts), result);
        return result;
    } else if (pattern[0] === "?") {
        // Try both possible alternatives
        const result =
            getPossibleSolutions("#" + pattern.slice(1), counts, depth + 1) +
            getPossibleSolutions("." + pattern.slice(1), counts, depth + 1);
        cache.set(getCacheKey(pattern, counts), result);
        return result;
    } else {
        // So the first character in the pattern is a #
        const [count, ...other_counts] = counts;
        // For this pattern to be valid, the next count
        // characters must be springs:
        if (pattern.slice(0, count).includes(".")) {
            return 0;
        }
        // If the following character is a # then count
        // would be wrong, so excluce that.
        if (pattern[count] === "#") {
            return 0;
        }
        // The next character must be a . so now just move one
        // further and count the possibilities starting after the .
        const result = getPossibleSolutions(
            pattern.slice(count + 1),
            other_counts,
            depth + 1,
        );
        cache.set(getCacheKey(pattern, counts), result);
        return result;
    }
}

function parseCounts(s: string): number[] {
    return s.split(",").map(Number);
}

async function main() {
    let lines = await getInputLines(2023, 12);
    // let lines = await getExampleLines();
    lines = lines.filter((l) => l.length > 0);
    let total_possible_solutions = 0;
    for (let line of lines) {
        let [pattern, counts_string] = line.split(" ");
        pattern = `${pattern}?${pattern}?${pattern}?${pattern}?${pattern}`;
        counts_string = `${counts_string},${counts_string},${counts_string},${counts_string},${counts_string}`;

        const possible_solutions = getPossibleSolutions(
            pattern,
            parseCounts(counts_string),
        );
        console.log({ possible_solutions });
        total_possible_solutions += possible_solutions;
    }
    console.log({ total_possible_solutions });
}

if (require.main === module) {
    main();
}
