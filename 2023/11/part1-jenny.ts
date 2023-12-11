import { getInputLines, getExampleLines } from "../aoc";

function expandUniverse(universe: string[][]) {
    const expanded_universe = [];
    for (let i = 0; i < universe.length; i++) {
        const current_row = [...universe[i]];
        expanded_universe.push(current_row);
        if (current_row.every(s => s === ".")) {
            const current_row_copy = [...current_row];
            expanded_universe.push(current_row_copy);
        }
    }
    // start inserting from the ends of the rows to avoid breaking the indexing
    for (let i = universe[0].length - 1; i >= 0; i--) {
        const current_column = universe.map(r => r[i]);
        if (current_column.every(s => s === ".")) {
            for (const row of expanded_universe) {
                row.splice(i, 0, ".");
            }
        }
    }
    return expanded_universe;
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
    const original_universe = [];
    for (const line of lines) {
        original_universe.push(line.split(""));
    }
    const expanded_universe = expandUniverse(original_universe);
    const galaxy_coords = getGalaxyCoords(expanded_universe);

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
