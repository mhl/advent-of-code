import { getInputLines } from "../aoc";

async function main() {
    const lines = await getInputLines(2023, 3);
    const width = lines[0].length;
    const height = lines.length;

    function has_symbol_neighbour(x: number, y: number, length: number) {
        const min_x = Math.max(0, x - 1);
        const max_x = Math.min(x + length, width - 1);
        const min_y = Math.max(0, y - 1);
        const max_y = Math.min(y + 1, height - 1);
        for (let j = min_y; j <= max_y; j++) {
            const line = lines[j];
            const char_string = line.slice(min_x, max_x + 1);
            const has_symbol = /[^0-9.]/.test(char_string);
            if (has_symbol) {
                return true;
            }
        }
        return false;
    }

    let total = 0;
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const matches = Array.from(line.matchAll(/\d+/g));
        for (const match of matches) {
            if (match.index == null) {
                throw new Error(`no index found for match ${match}`);
            }
            if (has_symbol_neighbour(match.index, i, match[0].length)) {
                total += Number(match[0]);
            }
        }
    }
    console.log(total);
}

main();
