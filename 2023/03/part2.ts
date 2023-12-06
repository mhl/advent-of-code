import { getInputLines } from "../aoc";

type Coord = { x: number; y: number };

async function main() {
    const lines = await getInputLines(2023, 3);
    const width = lines[0].length;
    const height = lines.length;

    function get_star_neighbours_coords(
        x: number,
        y: number,
        length: number,
    ): Coord[] {
        const min_x = Math.max(0, x - 1);
        const max_x = Math.min(x + length, width - 1);
        const min_y = Math.max(0, y - 1);
        const max_y = Math.min(y + 1, height - 1);
        const coords: Coord[] = [];
        for (let j = min_y; j <= max_y; j++) {
            const line = lines[j];
            const char_string = line.slice(min_x, max_x + 1);
            const star_matches = Array.from(char_string.matchAll(/\*/g));
            for (const star_match of star_matches) {
                if (star_match.index == null) {
                    throw new Error(
                        `no index found for star_match ${star_match}`,
                    );
                }
                coords.push({ x: star_match.index + min_x, y: j });
            }
        }
        return coords;
    }

    const star_to_numbers = new Map<string, number[]>();
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const matches = Array.from(line.matchAll(/\d+/g));
        for (const match of matches) {
            const matched_string = match[0];
            const match_as_number = Number(matched_string);
            if (match.index == null) {
                throw new Error(`no index found for match ${match}`);
            }
            const star_coords = get_star_neighbours_coords(
                match.index,
                i,
                matched_string.length,
            );
            for (const star_coord of star_coords) {
                const key = `${star_coord.x},${star_coord.y}`;
                if (!star_to_numbers.has(key)) {
                    star_to_numbers.set(key, []);
                }
                star_to_numbers.get(key)?.push(match_as_number);
            }
        }
    }

    let total = 0;
    for (const part_numbers of star_to_numbers.values()) {
        if (part_numbers.length === 2) {
            total += part_numbers[0] * part_numbers[1];
        }
    }
    console.log(total);
}

main();
