import { getExampleLines, getInputLines, getInputString } from "../aoc";

async function main() {
    // let lines = await getExampleLines();
    let lines = await getInputLines(2023, 15);
    lines.filter((l) => l.length > 0);
    const input = lines.join("");
    let total = 0;
    for (const s of lines[0].split(",")) {
        total += hash(s);
    }
    console.log({ total });
}

function hash(s: string) {
    const ascii_values = [...s].map((c) => c.charCodeAt(0));
    return ascii_values.reduce(
        (total: number, c: number) => ((total + c) * 17) % 256,
        0,
    );
}

if (require.main === module) {
    main();
}
