import { getInputLines } from "../aoc";

class Card {
    readonly winning_numbers: number[];
    readonly numbers_we_have: number[];
    readonly match_count: number;
    copies: number = 1;

    constructor(
        winning_numbers: number[],
        numbers_we_have: number[],
        match_count: number,
    ) {
        this.winning_numbers = winning_numbers;
        this.numbers_we_have = numbers_we_have;
        this.match_count = match_count;
    }

    static createFromLine(line: string) {
        const numbers = line.split(/:\s+/)[1].split(/\s+\|\s+/);
        const winning_numbers = numbers[0].split(/\s+/).map(Number);
        const numbers_we_have = numbers[1].split(/\s+/).map(Number);
        const match_count = numbers_we_have.filter(
            (n) => winning_numbers.indexOf(n) >= 0,
        ).length;
        return new Card(winning_numbers, numbers_we_have, match_count);
    }
}

async function main() {
    const lines = await getInputLines(2023, 4)

    const all_cards = lines.filter((l) => l.length).map(Card.createFromLine);
    for (let i = 0; i < all_cards.length; i++) {
        const current_card = all_cards[i];
        for (let c = 1; c <= current_card.match_count; c++) {
            all_cards[i + c].copies += current_card.copies;
        }
    }
    const total_cards = all_cards.reduce(
        (total_so_far, card) => total_so_far + card.copies,
        0,
    );
    console.log(total_cards);
}

main();
