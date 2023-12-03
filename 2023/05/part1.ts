import { promises as fs } from "fs";

type RangeMap = {
    dest_start: number;
    source_start: number;
    length: number;
};

class AlmanacMap {
    ranges: RangeMap[] = [];

    convert(source: number): number {
        for (const range of this.ranges) {
            if (
                source >= range.source_start &&
                source < range.source_start + range.length
            ) {
                return source - range.source_start + range.dest_start;
            }
        }
        return source;
    }
}

async function main() {
    const data = await fs.readFile("input-jenny.txt", { encoding: "utf-8" });
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
                maps[maps.length - 1].ranges.push({
                    dest_start: Number(match[1]),
                    source_start: Number(match[2]),
                    length: Number(match[3]),
                });
            }
        }
    }

    function seed_to_location(seed: number): number {
        let current_value = seed;
        for (const map of maps) {
            current_value = map.convert(current_value);
        }
        return current_value;
    }

    console.log(Math.min(...seeds.map(seed_to_location)));
}

main();
