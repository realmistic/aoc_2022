from dataclasses import dataclass
import re
from typing import Tuple, List
from enum import Enum
from copy import deepcopy


class FactoryState(Enum):
    BUILDING_ORE_ROBOT = 1
    BUILDING_CLAY_ROBOT = 2
    BUILDING_OBSIDIAN_ROBOT = 3
    BUILDING_GEODE_ROBOT = 4
    IDLE = 5


@dataclass
class Blueprint:
    """Blueprint stats"""
    no: int
    ore_robot_ore: int
    clay_robot_ore: int
    obsidian_robot_ore: int
    obsidian_robot_clay: int
    geode_robot_ore: int
    geode_robot_obsidian: int


@dataclass
class State:
    steps_passed: int
    materials: List[int]
    robots: List[int]
    factory: FactoryState


def read_stats(file_path: str, test_input: bool = True):
    text_file = open(file_path, 'r')
    lines = text_file.read().splitlines()

    if test_input:
        print(f'First 10 lines of input {lines[0:10]}')
        # print(f'First 10 lines of input {lines[-10:]}')
        print(f'Len input = {len(lines)}')
        print('------------')

    blueprints_ = []
    for line in lines:
        n = re.findall(r'\d+', line)
        nn = [int(elem) for elem in n]
        b = Blueprint(nn[0], nn[1], nn[2], nn[3], nn[4], nn[5], nn[6])
        blueprints_.append(b)
        # print(n)

    return blueprints_


def simulate_one_blueprint(b_: Blueprint, max_steps_=24, debug=False) -> int:
    print(f'SIMULATING BLUEPRINT {b_}')
    MAX_STEPS = max_steps_

    blueprint = b_
    print(f'Current blueprint {blueprint}')
    step = 0
    initial_state = State(steps_passed=step,
                          materials=[0, 0, 0, 0],
                          robots=[1, 0, 0, 0],
                          factory=FactoryState.IDLE)

    # print('------------------------------------------------')
    # print(f' Initial state ={initial_state}')

    states = [initial_state]

    while step < MAX_STEPS:
        step += 1
        if debug:
            print(f'Current step: {step}')
            print(f'Initial amount of states {len(states)} ')

        next_states = []
        for state in states:
            materials = [state.materials[0], state.materials[1], state.materials[2], state.materials[3]]
            robots = [state.robots[0], state.robots[1], state.robots[2], state.robots[3]]

            # # new robots arrived?
            # if state.factory == FactoryState.BUILDING_ORE_ROBOT:
            #     robots[0] += 1
            # elif state.factory == FactoryState.BUILDING_CLAY_ROBOT:
            #     robots[1] += 1
            # elif state.factory == FactoryState.BUILDING_OBSIDIAN_ROBOT:
            #     robots[2] += 1
            # elif state.factory == FactoryState.BUILDING_GEODE_ROBOT:
            #     robots[3] += 1

            # options for the next step
            # 4) decided to build a Geode robot
            if materials[0] >= blueprint.geode_robot_ore and materials[2] >= blueprint.geode_robot_obsidian:
                materials[0] -= blueprint.geode_robot_ore
                materials[2] -= blueprint.geode_robot_obsidian

                # all robots collect materials
                materials2 = deepcopy(materials)
                for i, robot in enumerate(robots):
                    materials2[i] += robot

                robots[3] += 1
                s = State(step, materials=deepcopy(materials2), robots=deepcopy(robots),
                          factory=FactoryState.BUILDING_GEODE_ROBOT)
                robots[3] -= 1
                next_states.append(s)
                materials[0] += blueprint.geode_robot_ore
                materials[2] += blueprint.geode_robot_obsidian

            # 3) build an obsidian_robot
            elif materials[0] >= blueprint.obsidian_robot_ore and materials[1] >= blueprint.obsidian_robot_clay:
                materials[0] -= blueprint.obsidian_robot_ore
                materials[1] -= blueprint.obsidian_robot_clay

                # all robots collect materials
                materials2 = deepcopy(materials)
                for i, robot in enumerate(robots):
                    materials2[i] += robot

                robots[2] += 1
                s = State(step, materials=deepcopy(materials2), robots=deepcopy(robots),
                          factory=FactoryState.BUILDING_OBSIDIAN_ROBOT)
                robots[2] -= 1
                next_states.append(s)
                materials[0] += blueprint.obsidian_robot_ore
                materials[1] += blueprint.obsidian_robot_clay
                # built_robot = True

            # 2) build a clay_robot /ore_robot/idle
            else:
                if materials[0] >= blueprint.clay_robot_ore:
                    materials[0] -= blueprint.clay_robot_ore

                    # all robots collect materials
                    materials2 = deepcopy(materials)
                    for i, robot in enumerate(robots):
                        materials2[i] += robot

                    robots[1] += 1
                    s = State(step, materials=deepcopy(materials2), robots=deepcopy(robots),
                              factory=FactoryState.BUILDING_CLAY_ROBOT)
                    robots[1] -= 1
                    next_states.append(s)
                    materials[0] += blueprint.clay_robot_ore

                # 1) build an ore_robot
                if materials[0] >= blueprint.ore_robot_ore:
                    materials[0] -= blueprint.ore_robot_ore

                    # all robots collect materials
                    materials2 = deepcopy(materials)
                    for i, robot in enumerate(robots):
                        materials2[i] += robot

                    robots[0] += 1
                    s = State(step, materials=deepcopy(materials2), robots=deepcopy(robots),
                              factory=FactoryState.BUILDING_ORE_ROBOT)
                    robots[0] -= 1
                    next_states.append(s)
                    materials[0] += blueprint.ore_robot_ore

                # 5) don't go IDLE, if we can build at least one ROBOT!
                # all robots collect materials
                materials2 = deepcopy(materials)
                for i, robot in enumerate(robots):
                    materials2[i] += robot

                s = State(step, materials=deepcopy(materials2), robots=deepcopy(robots), factory=FactoryState.IDLE)
                next_states.append(s)

        if debug:
            print(f'Generated these amount of states {len(next_states)} ')
            print('------------------------------------------------')

        max_obsidian_robots = max([state.robots[2] for state in next_states])
        max_geode_robots = max([state.robots[3] for state in next_states])

        # geod_building_states = [state for state in next_states if state.factory == FactoryState.BUILDING_GEODE_ROBOT]
        # obs_building_states = [state for state in next_states if state.factory == FactoryState.BUILDING_OBSIDIAN_ROBOT]
        #
        # if len(geod_building_states) > 0:
        #     states = geod_building_states
        #     if debug:
        #         print(
        #             f'We have cases with building a Geode robot within {len(states)} states')
        #         print(states)
        # elif len(obs_building_states) > 0:
        #     states = obs_building_states
        #     if debug:
        #         print(
        #             f'We have cases with building an Obsidian robot within {len(states)} states')
        #         print(states)
        # else:
        #     states = next_states

        if max_geode_robots > 0:
            states = [state for state in next_states if
                      state.robots[3] >= max_geode_robots - 1]
            if debug:
                print(
                    f'We have max {max_geode_robots} Geode robots within {len(states)} states')
                # print(states)

        elif max_obsidian_robots > 0:
            states = [state for state in next_states if state.robots[2] >= max_obsidian_robots - 1]
            if debug:
                print(f'We have max {max_obsidian_robots} Obsidian robots {len(states)} states')
        else:
            states = next_states

    max_geode_materials_count = max([state.materials[3] for state in states])
    best_states = [state for state in states if state.materials[3] == max_geode_materials_count]

    print(f'Found {len(best_states)} best states with geode count== {max_geode_materials_count}')
    print(f'RETURNING VALUE {b_.no * max_geode_materials_count}, max geods ={max_geode_materials_count}')

    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    return b_.no * max_geode_materials_count


# blueprints = read_stats('../inputs/inputs_day19_test.txt', test_input=False)
blueprints = read_stats('../inputs/inputs_day19.txt', test_input=False)

print(f' Blueprints: {blueprints}')
print(f'Begin simulation')
print('=================')

rez_part1 = 0
for b in blueprints:
    rez_part1 += simulate_one_blueprint(b)

print(f'Result Part1 = {rez_part1}')

rez_part2 = 1
for b in blueprints[0:3]:
    rez_part2 *= simulate_one_blueprint(b, max_steps_=32, debug=True) / b.no

print(f'Result Part2 = {rez_part2}')
