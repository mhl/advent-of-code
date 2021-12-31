import { getInputLines } from "../aoc";

type MultipleNodes = string[];

type Side = "L" | "R";

function isValidSide(s: string): s is Side {
    return s === "L" || s === "R";
}

function endsInZ(node: string): boolean {
    return /Z$/.test(node);
}

type PrimeFactors = Map<number, number>;

function primeFactors(n: number): PrimeFactors {
    const factors: PrimeFactors = new Map();
    let divisor = 2;

    while (n >= 2) {
        if (n % divisor == 0) {
            let existing = factors.get(divisor);
            if (existing == null) {
                factors.set(divisor, 0);
                existing = 0;
            }
            factors.set(divisor, existing + 1);
            n = n / divisor;
        } else {
            divisor++;
        }
    }
    return factors;
}

function leastCommonMultiple(ns: number[]) {
    const lcm_prime_factors: PrimeFactors = new Map();
    for (const n of ns) {
        const prime_factors = primeFactors(n);
        for (const [prime_factor, exponent] of prime_factors.entries()) {
            let existing = lcm_prime_factors.get(prime_factor);
            if (!existing) {
                existing = 0;
            }
            if (exponent > existing) {
                lcm_prime_factors.set(prime_factor, exponent);
            }
        }
    }
    return Array.from(lcm_prime_factors.entries()).reduce(
        (total, [prime_factor, exponent]) => total * prime_factor ** exponent,
        1,
    );
}

async function main() {
    let lines = await getInputLines(2023, 8);

    const instructions: Side[] = [];
    for (const letter of lines[0]) {
        if (!isValidSide(letter)) {
            throw new Error(`Unknown instruction found: “${letter}”`);
        }
        instructions.push(letter);
    }

    const network = new Map<string, Record<Side, string>>();
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

    const starting_nodes = Array.from(network.keys()).filter((node) =>
        /A$/.test(node),
    );

    function getNextNode(old_node: string, side: Side) {
        const entry = network.get(old_node);
        if (!entry) {
            throw new Error(`Unknown entry “${old_node}”`);
        }
        return entry[side];
    }

    function zAfter(start_node: string) {
        let current_node = start_node;
        let steps = 0;
        while (!endsInZ(current_node)) {
            let i = steps % instructions.length;
            current_node = getNextNode(current_node, instructions[i]);
            steps++;
        }
        return steps;
    }

    const cycle_lengths = starting_nodes.map((node) => zAfter(node));
    console.log(leastCommonMultiple(cycle_lengths));
}

main();
