#!/usr/bin/env python3

import re
from dataclasses import dataclass


line_re = re.compile("^(\w{2,3}) x=([-\d]+)\.\.([-\d]+),y=([-\d]+)\.\.([-\d]+),z=([-\d]+)\.\.([-\d]+)$")

instructions = {
    "on": 1,
    "off": 0
}

bounds = {
    "min": -50,
    "max": 50
}


@dataclass
class RebootStep:
    instruction: int
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    @classmethod
    def from_line(cls, line):
        params = line_re.search(line).groups()
        return RebootStep(instructions[params[0]], *(int(p) for p in params[1:]))

    def cubes(self):
        cubes = set()
        for x in range(max(self.x_min, bounds["min"]), min(self.x_max+1, bounds["max"])):
            for y in range(max(self.y_min, bounds["min"]), min(self.y_max+1, bounds["max"])):
                for z in range(max(self.z_min, bounds["min"]), min(self.z_max+1, bounds["max"])):
                    cubes.add((x,y,z))
        return cubes


with open("input-jenny.txt") as f:
    reboot_steps = [RebootStep.from_line(line.rstrip()) for line in f.readlines()]

on_cubes = set()
for reboot_step in reboot_steps:
    if reboot_step.instruction == 1:
        on_cubes.update(reboot_step.cubes())
    else:
        on_cubes -= reboot_step.cubes()

print(len(on_cubes))
