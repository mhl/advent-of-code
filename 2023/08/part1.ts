import { getInputLines } from "../aoc";

async function main() {
    let lines = await getInputLines(2023, 8);

    const instructions = lines[0];

    const network = new Map<string, Record<string, string>>();
    for (const line of lines.slice(2)) {
        if (!line.length) {
            continue;
        }
        const [current_node, left_right] = line.split(" = ");
        const matches = left_right.match(/\((\w+), (\w+)\)/);
        if (!matches) {
            throw new Error(`no matches found in line: ${line}`);
        }
        network.set(current_node, {
            L: matches[1],
            R: matches[2],
        });
    }

    let next_node_key = "AAA";
    let next_node = network.get(next_node_key);
    if (next_node == null) {
        throw new Error("can't find starting node AAA");
    }
    let steps = 0;

    while (next_node_key != "ZZZ") {
        let i = steps % instructions.length;
        next_node_key = next_node[instructions[i]];
        steps += 1;
        next_node = network.get(next_node_key);
        if (!next_node) {
            throw new Error(`can't find next_node ${next_node_key}`);
        }
    }
    console.log(steps);
}

main();
