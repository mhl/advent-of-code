import { getInputLines } from "../aoc";

const VALID_BALL_COLOURS = ["red", "green", "blue"] as const;

type BallColour = (typeof VALID_BALL_COLOURS)[number];

function isValidBallColour(s: string): s is BallColour {
    return VALID_BALL_COLOURS.includes(s as BallColour);
}

type BallCounts = Record<BallColour, number>;

const max_per_colour: BallCounts = {
    red: 0,
    green: 0,
    blue: 0,
};

function get_colour_counts(subset: string) {
    const colours = subset.split(", ");
    const result: BallCounts = {
        red: 0,
        green: 0,
        blue: 0,
    };
    for (let colour_number of colours) {
        const n = colour_number.split(" ")[0];
        const c = colour_number.split(" ")[1];
        if (!isValidBallColour(c)) {
            throw new Error(`Invalid ball colour ${c}`);
        }
        result[c] = Number(n);
    }
    return result;
}

function max_colour_counts(a: BallCounts, b: BallCounts): BallCounts {
    return {
        red: Math.max(a.red, b.red),
        green: Math.max(a.green, b.green),
        blue: Math.max(a.blue, b.blue),
    };
}

function power(ball_counts: BallCounts): number {
    return ball_counts.red * ball_counts.green * ball_counts.blue;
}

async function main() {
    const lines = await getInputLines(2023, 2);
    let total = 0;
    for (let line of lines) {
        const match = line.match(/^Game (\d+): (.*)/);
        if (!match) {
            continue;
        }
        const game_id = match[1];
        const subsets = match[2].split("; ");

        const max_ball_counts = subsets.reduce(
            (aggregated, current, i) =>
                max_colour_counts(aggregated, get_colour_counts(current)),
            {
                red: 0,
                green: 0,
                blue: 0,
            },
        );
        total += power(max_ball_counts);
    }
    console.log("total is:", total);
}
main();
