import { getExampleLines, getInputLines, getInputString } from "../aoc";

type Lens = {
    label: string;
    focal_length: number;
};

async function main() {
    // let lines = await getExampleLines();
    let lines = await getInputLines(2023, 15);
    lines.filter((l) => l.length > 0);
    const input = lines.join("");
    const boxes: Lens[][] = [];
    for (let i = 0; i < 256; ++i) {
        boxes[i] = [];
    }
    for (const instruction of lines[0].split(",")) {
        const m = instruction.match(
            /^(?<label>\w+)(?<operation>[-=])(?<focal_length>\d+)?$/,
        );
        if (!m?.groups) {
            throw new Error(`Failed to match “${instruction}”`);
        }
        const label = m.groups.label;
        const operation = m.groups.operation;
        const focal_length = m.groups.focal_length
            ? Number(m.groups.focal_length)
            : null;
        const box_index = hash(label);
        if (operation === "-") {
            boxes[box_index] = boxes[box_index].filter(
                (l) => l.label !== label,
            );
        } else if (operation === "=") {
            if (focal_length == null) {
                throw new Error(
                    `The instruction ${instruction} had operation “${operation}” but no focal length`,
                );
            }
            const lenses = boxes[box_index];
            const existing_lens = lenses.find((lens) => lens.label === label);
            if (existing_lens) {
                existing_lens.focal_length = focal_length;
            } else {
                lenses.push({ label, focal_length });
            }
        }
    }
    for (let i = 0; i < boxes.length; ++i) {
        const lenses = boxes[i];
        if (lenses.length > 0) {
            console.log("Box", i, lenses);
        }
    }
    let total_focussing_power = 0;
    for (let i = 0; i < boxes.length; ++i) {
        const lenses = boxes[i];
        for (let l = 0; l < lenses.length; ++l) {
            const focussing_power = (i + 1) * (l + 1) * lenses[l].focal_length;
            total_focussing_power += focussing_power;
        }
    }
    console.log({ total_focussing_power });
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
