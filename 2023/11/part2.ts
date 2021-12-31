import { start } from "repl";
import { getExampleLines, getInputLines } from "../aoc";

class Star {
    constructor(
        public x: number,
        public y: number,
        public n: number,
    ) {}
    distanceTo(
        other: Star,
        empty_rows: Set<number>,
        empty_columns: Set<number>,
    ): number {
        const min_x = Math.min(this.x, other.x);
        const max_x = Math.max(this.x, other.x);
        const min_y = Math.min(this.y, other.y);
        const max_y = Math.max(this.y, other.y);
        let empty_columns_between = 0;
        for (let x = min_x + 1; x <= max_x - 1; ++x) {
            if (empty_columns.has(x)) {
                empty_columns_between++;
            }
        }
        let empty_rows_between = 0;
        for (let y = min_y + 1; y <= max_y - 1; ++y) {
            if (empty_rows.has(y)) {
                empty_rows_between++;
            }
        }
        const x_difference =
            max_x - min_x + empty_columns_between * (1000000 - 1);
        const y_difference = max_y - min_y + empty_rows_between * (1000000 - 1);

        return x_difference + y_difference;
    }
    toString(): string {
        return `x: ${this.x}, y: ${this.y}, star: ${this.n}`;
    }
}

async function main() {
    let lines = await getInputLines(2023, 11);
    // let lines = await getExampleLines();
    lines = lines.filter((l) => l.length > 0);

    const universe: number[][] = [];

    let star_count = 0;
    for (const line of lines) {
        universe.push(
            line.split("").map((c) => {
                if (c === "#") {
                    star_count++;
                    return star_count;
                } else {
                    return 0;
                }
            }),
        );
    }

    const width = universe[0].length;
    const height = universe.length;

    const empty_rows: Set<number> = new Set();
    const empty_columns: Set<number> = new Set();
    console.log({ universe });
    for (let y = 0; y < height; ++y) {
        if (universe[y].every((n) => n === 0)) empty_rows.add(y);
    }
    for (let x = 0; x < width; ++x) {
        const column = [];
        for (let j = 0; j < height; ++j) {
            column.push(universe[j][x]);
        }
        if (column.every((n) => n === 0)) empty_columns.add(x);
    }

    const stars: Star[] = [];
    for (let y = 0; y < height; ++y) {
        for (let x = 0; x < width; ++x) {
            const v = universe[y][x];
            if (v) stars.push(new Star(x, y, v));
        }
    }

    let total_shortest_distances = 0;
    for (let i = 0; i < stars.length - 1; ++i) {
        for (let j = i + 1; j < stars.length; ++j) {
            const shortest_distance = stars[i].distanceTo(
                stars[j],
                empty_rows,
                empty_columns,
            );
            console.log(
                `shortest distance between ${stars[i]} and ${stars[j]} was ${shortest_distance}`,
            );
            total_shortest_distances += shortest_distance;
        }
    }
    console.log({ total_shortest_distances });
}

main();
