import { promises as fs } from "fs";

const VALID_BALL_COLOURS = ["red", "green", "blue"] as const;

type BallColour = (typeof VALID_BALL_COLOURS)[number];

function isValidBallColour(s: string): s is BallColour {
    return VALID_BALL_COLOURS.includes(s as BallColour);
}

const max_per_colour: Record<BallColour, number> = {
    red: 12,
    green: 13,
    blue: 14,
};

function check_colour(colour_number: string) {
    const n = colour_number.split(" ")[0];
    const c = colour_number.split(" ")[1];
    if (!isValidBallColour(c)) {
        throw new Error(`Invalid ball colour ${c}`);
    }
    return max_per_colour[c] >= Number(n);
}

function check_valid_subset(subset: string) {
    const colours = subset.split(", ");
    return colours.every(check_colour);
}

async function main() {
    const data = await fs.readFile("input-jenny.txt", { encoding: "utf-8" });
    const lines = data.split("\n");
    let total = 0;
    for (let line of lines) {
        const match = line.match(/^Game (\d+): (.*)/);
        if (!match) {
            continue;
        }
        const game_id = match[1];
        const subsets = match[2].split("; ");
        if (subsets.every(check_valid_subset)) {
            total += Number(game_id);
        }
    }
    console.log("total is:", total);
}
main();
