import { getExampleLines, getInputLines, getInputString } from "../aoc";

type Beam = {
    dx: number;
    dy: number;
    x: number;
    y: number;
};

function carryOn(beam: Beam) {
    return {
        x: beam.x + beam.dx,
        y: beam.y + beam.dy,
        dx: beam.dx,
        dy: beam.dy,
    };
}

function deflectDown(beam: Beam) {
    return { x: beam.x, y: beam.y + 1, dx: 0, dy: 1 };
}

function deflectUp(beam: Beam) {
    return { x: beam.x, y: beam.y - 1, dx: 0, dy: -1 };
}

function deflectLeft(beam: Beam) {
    return { x: beam.x - 1, y: beam.y, dx: -1, dy: 0 };
}

function deflectRight(beam: Beam) {
    return { x: beam.x + 1, y: beam.y, dx: 1, dy: 0 };
}

function printGrid(rows: string[], indent = 0) {
    for (const row of rows) {
        process.stdout.write(`${" ".repeat(indent)}${row}\n`);
    }
}

function beamToString(beam: Beam) {
    let c;
    if (beam.dx === 1) {
        c = ">";
    } else if (beam.dx === -1) {
        c = "<";
    } else if (beam.dy === 1) {
        c = "v";
    } else if (beam.dy === -1) {
        c = "^";
    }
    return `x: ${beam.x}, y: ${beam.y}, d: ${c}`;
}

function countEnergizedLocations(rows: boolean[][]) {
    let total = 0;
    for (const row of rows) {
        total += row.reduce((s, v) => s + +v, 0);
    }
    return total;
}

function getKey(beam: Beam) {
    return JSON.stringify(beam);
}

async function main() {
    // let lines = await getExampleLines();
    let lines = await getInputLines(2023, 16);
    lines = lines.filter((l) => l.length > 0);

    printGrid(lines);

    const w = lines[0].length;
    const h = lines.length;
    const energized_locations = lines.map((line) =>
        new Array(line.length).fill(false),
    );
    const visited_states: Set<string> = new Set();

    function outOfBounds(beam: Beam) {
        return beam.x < 0 || beam.x >= w || beam.y < 0 || beam.y >= h;
    }

    let beams: Beam[] = [{ x: 0, y: 0, dx: 1, dy: 0 }];
    while (beams.length > 0) {
        const new_beams: Beam[] = [];
        for (const beam of beams) {
            energized_locations[beam.y][beam.x] = true;
            visited_states.add(getKey(beam));
            const item = lines[beam.y][beam.x];
            if (item === ".") {
                new_beams.push(carryOn(beam));
            } else if (item === "|") {
                if (beam.dx === 0) {
                    new_beams.push(carryOn(beam));
                } else {
                    new_beams.push(deflectUp(beam));
                    new_beams.push(deflectDown(beam));
                }
            } else if (item === "-") {
                if (beam.dx === 0) {
                    new_beams.push(deflectLeft(beam));
                    new_beams.push(deflectRight(beam));
                } else {
                    new_beams.push(carryOn(beam));
                }
            } else if (item === "/") {
                if (beam.dx === -1) {
                    new_beams.push(deflectDown(beam));
                } else if (beam.dx === 1) {
                    new_beams.push(deflectUp(beam));
                } else if (beam.dy === -1) {
                    new_beams.push(deflectRight(beam));
                } else if (beam.dy === 1) {
                    new_beams.push(deflectLeft(beam));
                }
            } else if (item === "\\") {
                if (beam.dx === -1) {
                    new_beams.push(deflectUp(beam));
                } else if (beam.dx === 1) {
                    new_beams.push(deflectDown(beam));
                } else if (beam.dy === -1) {
                    new_beams.push(deflectLeft(beam));
                } else if (beam.dy === 1) {
                    new_beams.push(deflectRight(beam));
                }
            } else {
                throw new Error(`Unknown item “${item}”`);
            }
        }
        beams = new_beams
            .filter((beam) => !outOfBounds(beam))
            .filter((beam) => !visited_states.has(getKey(beam)));
    }
    printGrid(
        energized_locations.map((r) => r.map((b) => (b ? "#" : ".")).join("")),
    );
    const energized_locations_count =
        countEnergizedLocations(energized_locations);
    console.log({ energized_locations_count });
}

if (require.main === module) {
    main();
}
