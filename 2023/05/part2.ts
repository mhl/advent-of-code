import { promises as fs } from "fs";

type InclusiveRange = {
    start: number;
    end: number;
};

type SplitResult = {
    in_other_range: InclusiveRange;
    outside_other_range: InclusiveRange[];
};

function splitRange(
    to_split: InclusiveRange,
    other: InclusiveRange,
): SplitResult | null {
    //                  ---other---
    //  ---to_split--
    if (to_split.end < other.start || to_split.start > other.end) {
        return null;
    }
    //     ----------other-----------
    //           ---to_split---
    else if (to_split.start >= other.start && to_split.end <= other.end) {
        return {
            in_other_range: to_split,
            outside_other_range: [],
        };
    }
    //           ---other---
    //       --------to_split------
    else if (to_split.start < other.start && to_split.end > other.end) {
        return {
            in_other_range: other,
            outside_other_range: [
                { start: to_split.start, end: other.start - 1 },
                { start: other.end + 1, end: to_split.end },
            ],
        };
    }
    //           ---other---
    //   ------to_split-----
    else if (to_split.start < other.start && to_split.end <= other.end) {
        return {
            in_other_range: { start: other.start, end: to_split.end },
            outside_other_range: [
                { start: to_split.start, end: other.start - 1 },
            ],
        };
    }
    //           ---other---
    //           -------to_split-------
    else if (to_split.start >= other.start && to_split.end > other.end) {
        return {
            in_other_range: { start: to_split.start, end: other.end },
            outside_other_range: [{ start: other.end + 1, end: to_split.end }],
        };
    } else {
        throw new Error(
            `Unhandled case - input_range: ${to_split}, other_range: ${other}`,
        );
    }
}

class RangeMap {
    constructor(
        public dest_start: number,
        public source_range: InclusiveRange,
    ) {}

    includesNumber(n: number): boolean {
        return n >= this.source_range.start && n <= this.source_range.end;
    }

    convert(n: number): number {
        return (n - this.source_range.start) + this.dest_start;
    }
}

class AlmanacMap {
    ranges: RangeMap[] = [];

    convertSingleNumber(source: number): number {
        for (const range of this.ranges) {
            if (range.includesNumber(source)) return range.convert(source);
        }
        return source;
    }

    splitInputRanges(input_ranges: InclusiveRange[]): InclusiveRange[] {
        const final_ranges: InclusiveRange[] = [];
        let still_to_try_splitting = [...input_ranges];
        while (still_to_try_splitting.length > 0) {
            const to_split = still_to_try_splitting.pop()!;
            let dealt_with = false;
            for (const other_range_map of this.ranges) {
                const other_range = other_range_map.source_range;
                const split_result = splitRange(to_split, other_range);
                if (split_result) {
                    final_ranges.push(split_result.in_other_range);
                    still_to_try_splitting = still_to_try_splitting.concat(
                        split_result.outside_other_range,
                    );
                    dealt_with = true;
                    break;
                }
            }
            if (!dealt_with) {
                // Then it's outside all the known ranges
                final_ranges.push(to_split);
            }
        }
        return final_ranges;
    }

    convertInputRanges(input_ranges: InclusiveRange[]) {
        let split_input_ranges = this.splitInputRanges(input_ranges);
        return split_input_ranges.map((input_range) => ({
            start: this.convertSingleNumber(input_range.start),
            end: this.convertSingleNumber(input_range.end),
        }));
    }
}

async function main() {
    const data = await fs.readFile("input-mark.txt", { encoding: "utf-8" });
    const lines = data.split("\n");

    const seeds = lines[0].split(" ").slice(1).map(Number);

    const maps: AlmanacMap[] = [];
    for (const line of lines.slice(2)) {
        if (!line) {
            continue;
        }
        if (line.match(/ map:$/)) {
            maps.push(new AlmanacMap());
        } else {
            const match = line.match(/^(\d+) (\d+) (\d+)$/);
            if (match) {
                maps[maps.length - 1].ranges.push(
                    new RangeMap(
                        Number(match[1]),
                        {
                            start: Number(match[2]),
                            end: Number(match[2]) + Number(match[3]) - 1,
                        }
                    )
                );
            }
        }
    }

    const seed_ranges = [];
    for (let i = 0; i < seeds.length; i += 2) {
        seed_ranges.push({ start: seeds[i], end: seeds[i] + seeds[i + 1] - 1 });
    }

    function seed_range_to_final_ranges(
        seed_range: InclusiveRange,
    ): InclusiveRange[] {
        let current_ranges = [seed_range];
        for (const map of maps) {
            current_ranges = map.convertInputRanges(current_ranges);
        }
        return current_ranges;
    }

    const final_ranges = seed_ranges.flatMap(seed_range_to_final_ranges);

    console.log(Math.min(...final_ranges.map((r) => r.start)));
}

main();
