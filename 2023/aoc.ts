import { promises as fs, existsSync } from "fs";

export async function getInputLines(year: number, day: number): Promise<string[]> {
    const text = await getInputString(year, day);
    return text.split("\n");
}

export async function getInputString(year: number, day: number): Promise<string> {
    const local_copy_path = "input.txt";
    if (existsSync(local_copy_path)) {
        return fs.readFile(local_copy_path, { encoding: "utf-8" });
    } else {
        const session_cookie = process.env.AOC_SESSION_COOKIE;
        if (!session_cookie) {
            throw new Error("AOC_SESSION_COOKIE was not set in the environment");
        }
        const url = `https://adventofcode.com/${year}/day/${day}/input`;
        const response = await fetch(url, { headers: { 'Cookie': `session=${session_cookie}` }});
        if (response.status !== 200) {
            throw new Error(`Failed to fetch the input; HTTP status code ${response.status}`);
        }
        const text = await response.text();
        await fs.writeFile(local_copy_path, text);
        return text;
    }
}

export async function getExampleLines(): Promise<string[]> {
    const data = await fs.readFile("example.txt", { encoding: "utf-8" });
    return data.split("\n");
}
