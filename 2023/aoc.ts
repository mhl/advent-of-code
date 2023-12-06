import { promises as fs, existsSync } from "fs";

export async function getInputLines(year: number, day: number): Promise<string[]> {
    const local_copy_path = "input.txt";
    if (existsSync(local_copy_path)) {
        const text = await fs.readFile(local_copy_path, { encoding: "utf-8" });
        return text.split("\n");
    } else {
        const session_cookie = process.env.AOC_SESSION_COOKIE;
        if (!session_cookie) {
            throw new Error("AOC_SESSION_COOKIE was not set in the environment");
        }
        const url = `https://adventofcode.com/${year}/day/${day}/input`;
        const response = await fetch(url, { headers: { 'Cookie': `session=${session_cookie}` }});
        const text = await response.text();
        await fs.writeFile(local_copy_path, text);
        return text.split("\n");
    }
}
