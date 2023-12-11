import { getInputLines, getExampleLines } from "../aoc";

function findEmptyRows(universe: string[][]) {
    const empty_rows = [];
    for (let i = 0; i < universe.length; i++) {
        if (universe[i].every(s => s === ".")) {
            empty_rows.push(i);
        }
    }
    return empty_rows;
}

function findEmptyColumns(universe: string[][]) {
    const empty_cols = [];
    for (let i = 0; i < universe[0].length; i++) {
        const current_column = universe.map(r => r[i]);
        if (current_column.every(s => s === ".")) {
            empty_cols.push(i);
        }
    }
    return empty_cols;
}

class Coord {
    constructor(
        public x: number,
        public y: number,
    ) {}
    path_length_to(other: Coord): number {
        return Math.abs(this.x - other.x) + Math.abs(this.y - other.y);
    }
}

function getGalaxyCoords(universe: string[][]){
    const coords: Map<Number, Coord> = new Map();
    let galaxy_number = 1;
    for (let y = 0; y < universe.length; y++) {
        const row = universe[y];
        for (let x = 0; x < row.length; x++) {
            if (row[x] === "#") {
                coords.set(galaxy_number, new Coord(x, y));
                galaxy_number += 1;
            }
        }
    }
    return coords;
}

async function main() {
    let lines = await getInputLines(2023, 11);
    lines = lines.filter((l) => l.length > 0);
    const universe = [];
    for (const line of lines) {
        universe.push(line.split(""));
    }
    const galaxy_coords = getGalaxyCoords(universe);
    const empty_rows = findEmptyRows(universe);
    const empty_cols = findEmptyColumns(universe);

    for (let galaxy = 1; galaxy <= galaxy_coords.size; galaxy++) {
        const coord = galaxy_coords.get(galaxy);
        if (coord == null) {
            throw new Error("where is that galaxy then");
        }

        const empty_rows_before = empty_rows.filter(i => i < coord.y).length;
        coord.y += 999999 * empty_rows_before;

        const empty_cols_before = empty_cols.filter(i => i < coord.x).length;
        coord.x += 999999 * empty_cols_before;
    }

    const paths_to_lengths: Map<string, Number> = new Map();
    let total_path_lengths = 0;
    for (let from_galaxy = 1; from_galaxy <= galaxy_coords.size; from_galaxy++) {
        for (let to_galaxy = from_galaxy + 1; to_galaxy <= galaxy_coords.size; to_galaxy++) {
            const path = `${from_galaxy} - ${to_galaxy}`;
            const g1 = galaxy_coords.get(from_galaxy);
            const g2 = galaxy_coords.get(to_galaxy);
            if (g1 == null || g2 == null) {
                throw new Error("can't find galaxy");
            }
            const l = g1.path_length_to(g2);
            paths_to_lengths.set(path, l);
            total_path_lengths += l;
        }
    }
    console.log(total_path_lengths);
}

main();
