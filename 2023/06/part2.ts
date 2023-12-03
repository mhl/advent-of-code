import { getInputLines } from "../aoc";

async function main() {
    const lines = await getInputLines(2023, 6);
    const time = Number(lines[0].match(/(\d+)/g)?.join(""));
    const record_distance = Number(lines[1].match(/(\d+)/g)?.join(""));

    // record_distance = speed*time - speed**2
    // speed**2 + record_distance = speed*time
    // speed**2 - speed*time + record_distance = 0
    // speed**2 - speed*58996469 + 478223210191071 = 0

    const a = 1;
    const b = time * -1;
    const c = record_distance;

    const speed_1 = ((b * -1 - Math.sqrt(b ** 2 - 4 * a * c)) / 2) * a;
    const speed_2 = ((b * -1 + Math.sqrt(b ** 2 - 4 * a * c)) / 2) * a;

    console.log(Math.ceil(speed_2) - Math.ceil(speed_1));
}

main();
