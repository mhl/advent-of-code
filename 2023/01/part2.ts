import { getInputLines } from "../aoc";

function convertToDigitString(matched_string: string) {
    if (/^\d$/.test(matched_string)) {
        return matched_string;
    }
    const mapped = {
        one: "1",
        two: "2",
        three: "3",
        four: "4",
        five: "5",
        six: "6",
        seven: "7",
        eight: "8",
        nine: "9",
    }[matched_string];
    if (mapped) {
        return mapped;
    }
    throw new Error(`Unexpected input: “${matched_string}”`);
}

const DIGITS_RE = "one|two|three|four|five|six|seven|eight|nine|\\d";

const first_match_re = new RegExp(`^.*?(${DIGITS_RE})`);
const last_match_re = new RegExp(`^.*(${DIGITS_RE})`);

async function main() {
    const lines = await getInputLines(2023, 1);
    let total = 0;
    for (let line of lines) {
        const first_match = line.match(first_match_re);
        if (!first_match) continue;
        const last_match = line.match(last_match_re);
        if (!last_match) continue;
        const combined =
            convertToDigitString(first_match[1]) +
            convertToDigitString(last_match[1]);
        const combined_as_number = Number(combined);
        total += combined_as_number;
    }
    console.log("total is:", total);
}
main();
