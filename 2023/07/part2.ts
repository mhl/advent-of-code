import { getInputLines } from "../aoc";
import { promises as fs } from "fs";

function getTypeRank(cards: string) {
    const number_of_jokers = (cards.match(/J/g) || []).length;
    const cards_without_jokers = cards.replace(/J/g, "");
    const card_to_counts: Record<string, number> = {};
    for (const card of cards_without_jokers) {
        if (card in card_to_counts) {
            card_to_counts[card] += 1;
        } else {
            card_to_counts[card] = 1;
        }
    }

    let counts = Object.values(card_to_counts);
    counts.sort().reverse();
    counts[0] += number_of_jokers;

    if (counts.length === 1) {
        return 6;
    } else if (counts[0] === 4) {
        return 5;
    } else if (counts[0] === 3 && counts[1] === 2) {
        return 4;
    } else if (counts[0] === 3) {
        return 3;
    } else if (counts[0] === 2 && counts[1] === 2) {
        return 2;
    } else if (counts[0] === 2) {
        return 1;
    } else {
        return 0;
    }
}

const TYPE_RANK_TO_NAME = [
    "High Card",
    "Pair",
    "Two Pair",
    "Three of a Kind",
    "Full House",
    "Four of a Kind",
    "Five of a Kind",
];

// AKQT98765432J
// EDCB        1

function rewrite_card_string(cards: string) {
    return cards.replace(/./g, function (m) {
        const mapped = {
            A: "E",
            K: "D",
            Q: "C",
            J: "1",
            T: "B",
        }[m];
        if (mapped) {
            return mapped;
        }
        return m;
    });
}

function compare_hands(line1: string, line2: string) {
    const cards1 = line1.split(" ")[0];
    const cards2 = line2.split(" ")[0];

    const type_rank_1 = getTypeRank(cards1);
    const type_rank_2 = getTypeRank(cards2);
    if (type_rank_1 != type_rank_2) {
        return type_rank_1 - type_rank_2;
    }

    const mapped_cards1 = rewrite_card_string(cards1);
    const mapped_cards2 = rewrite_card_string(cards2);

    return mapped_cards1.localeCompare(mapped_cards2);
}

async function main() {
    let lines = await getInputLines(2023, 7);
    // let lines = (await fs.readFile("more-complex-example.txt", { encoding: "utf-8" })).split("\n")
    lines = lines.filter((l) => l.length);
    lines.sort(compare_hands);
    for (const line of lines) {
        const cards = line.split(" ")[0];
        const type_rank = getTypeRank(cards);
        console.log(type_rank, TYPE_RANK_TO_NAME[type_rank], line);
    }

    const total = lines.reduce((total_winnings, line, i) => {
        const bid_string = line.split(" ")[1];
        if (bid_string == null) {
            throw new Error("malformed line");
        }
        return Number(bid_string) * (i + 1) + total_winnings;
    }, 0);
    console.log(total);
}

main();
