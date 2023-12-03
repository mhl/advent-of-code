import { getInputLines } from "../aoc";

class Race {
    constructor(
        public time: number,
        public record_distance: number,
        public ways: number = 0,
    ) {}
}

async function main() {
    const lines = await getInputLines(2023, 6);
    const times = lines[0].split(/\s+/).slice(1).map(Number);
    const record_distances = lines[1].split(/\s+/).slice(1).map(Number);

    const races: Race[] = [];
    for (let i = 0; i < times.length; i++) {
        races.push(new Race(times[i], record_distances[i]));
    }

    for (const race of races) {
        for (let ms = 0; ms <= race.time; ms++) {
            let hold_button = ms;
            let speed = hold_button;
            let travelling_time = race.time - hold_button;
            let distance_travelled = speed * travelling_time;

            if (distance_travelled > race.record_distance) {
                race.ways = race.ways += 1;
            }
        }
    }

    let result = races.reduce(
        (total_so_far, race) => total_so_far * race.ways,
        1,
    );

    console.log(result);
}

main();
