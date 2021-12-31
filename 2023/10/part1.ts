import { getInputLines } from "../aoc";

class AdjacentTile {
    constructor(
        public dx: number,
        public dy: number,
    ) {}
    equals(other: AdjacentTile): boolean {
        return this.dx === other.dx && this.dy === other.dy;
    }
    reverse() {
        return new AdjacentTile(-this.dx, -this.dy);
    }
}

type Board = string[][];

const NORTH = new AdjacentTile(0, -1);
const SOUTH = new AdjacentTile(0, 1);
const EAST = new AdjacentTile(1, 0);
const WEST = new AdjacentTile(-1, 0);

const ALL_DIRECTIONS: AdjacentTile[] = [NORTH, SOUTH, EAST, WEST];

class Coordinate {
    constructor(
        public x: number,
        public y: number,
    ) {}
    move(direction: AdjacentTile) {
        return new Coordinate(this.x + direction.dx, this.y + direction.dy);
    }
    equals(other: Coordinate): boolean {
        return this.x === other.x && this.y === other.y;
    }
}

const PIPES: Record<string, AdjacentTile[]> = {
    "|": [NORTH, SOUTH],
    "-": [EAST, WEST],
    L: [NORTH, EAST],
    J: [NORTH, WEST],
    "7": [SOUTH, WEST],
    F: [SOUTH, EAST],
};

function getOtherEnd(
    directions_pair: AdjacentTile[],
    this_end: AdjacentTile,
): AdjacentTile | null {
    if (directions_pair[0].equals(this_end)) {
        return directions_pair[1];
    } else if (directions_pair[1].equals(this_end)) {
        return directions_pair[0];
    } else {
        return null;
    }
}

const PIPE_CHARACTERS = Object.keys(PIPES);

class CurrentPosition {
    constructor(
        public coordinate: Coordinate,
        public entered_from: AdjacentTile,
        public steps_count: number,
        public override_letter: string | null = null,
    ) {}

    getNext(): CurrentPosition | null {
        let current_letter = this.override_letter;
        if (!current_letter) {
            current_letter = board[this.coordinate.y][this.coordinate.x];
        }
        const pipe_ends = PIPES[current_letter];
        if (!pipe_ends) {
            return null;
        }
        const leave_by = getOtherEnd(pipe_ends, this.entered_from);
        if (!leave_by) {
            throw new Error(
                `No other end of ${this.entered_from} found in ${pipe_ends}`,
            );
        }
        const new_coordinate = this.coordinate.move(leave_by);
        // Does the pipe at that new coordinate accept input from
        // here?
        const new_pipe_entered_from = leave_by.reverse();
        const new_pipe_ends = PIPES[board[new_coordinate.y][new_coordinate.x]];
        if (!new_pipe_ends) return null;
        if (!getOtherEnd(new_pipe_ends, new_pipe_entered_from)) {
            return null;
        }
        return new CurrentPosition(
            new_coordinate,
            new_pipe_entered_from,
            this.steps_count + 1,
        );
    }
}

const board: Board = [];

function getStartCoordinate(): Coordinate {
    for (let y = 0; y < board.length; y++) {
        for (let x = 0; x < board[0].length; x++) {
            if (board[y][x] === "S") {
                return new Coordinate(x, y);
            }
        }
    }
    throw new Error("S didn't exist in the grid");
}

function getSolution(paths: CurrentPosition[]) {
    if (paths.length !== 2) {
        throw new Error(`Expected 2 paths, got ${paths.length}`);
    }
    if (paths[0].coordinate.equals(paths[1].coordinate)) {
        return paths;
    }
    return null;
}

function tryStartPipe(start_pipe_type: string, start_coordinate: Coordinate) {
    let paths: CurrentPosition[] = [];
    for (const came_from of PIPES[start_pipe_type]) {
        paths.push(
            new CurrentPosition(
                start_coordinate,
                came_from,
                0,
                start_pipe_type,
            ),
        );
    }
    let solution;
    do {
        const new_paths: CurrentPosition[] = [];
        for (const possible_path of paths) {
            const next_possible_path = possible_path.getNext();
            if (next_possible_path) {
                new_paths.push(next_possible_path);
            }
        }
        paths = new_paths;
        if (paths.length < 2) {
            return null;
        }
    } while (!(solution = getSolution(paths)));
    return paths;
}

async function main() {
    let lines = await getInputLines(2023, 10);
    lines = lines.filter((l) => l.length > 0);
    for (const line of lines) {
        board.push(line.split(""));
    }
    const start_coordinate = getStartCoordinate();

    for (const pipe_type of PIPE_CHARACTERS) {
        console.log("Trying S as", pipe_type);
        const solution = tryStartPipe(pipe_type, start_coordinate);
        if (!solution) {
            continue;
        }
        console.log("Steps to furthest point:", solution[0].steps_count);

        break;
    }
}

main();
