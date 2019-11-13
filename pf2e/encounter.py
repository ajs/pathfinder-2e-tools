
import random
import argparse
from .rules import PF2Rules


def cost_of(creature, party_level, costs):
    return costs[creature['Level'] - party_level + 4]


def in_budget(creature, party_level, costs, budget):
    return cost_of(creature, party_level, costs) <= budget


def in_level_range(creature, party_level):
    creature_level = creature['Level']
    min_level = party_level - 4
    max_level = party_level + 2
    return (creature_level >= min_level and creature_level <= max_level)


def print_creature(creature):
    name = creature['Name']
    level = creature['Level']
    alignment = creature['Alignment']
    creature_type = creature['Creature Type']
    print(f"{name} lvl {level} {alignment} {creature_type}")


def alignment_coords(alignment):
    if alignment == 'Neutral':
        return (1,1)
    parts = alignment.split(' ', 1)
    locs = {
        'Lawful': 0, 'Neutral': 1, 'Chaotic': 2,
        'Good': 0, 'Evil': 2,
    }
    return tuple(locs[p] for p in parts)


def creature_aligned(creature, encounter, similar=False):
    enc_aligns = [c['Alignment'] for c in encounter]
    return is_aligned(creature['Alignment'], enc_aligns, similar)

def is_aligned(target_align, match_aligns, similar):
    align_c = alignment_coords(target_align)
    if similar:
        box = [align_c, align_c]
        for align_c in (alignment_coords(c) for c in match_aligns):
            box = [
                (min(align_c[0], box[0][0]), min(align_c[1], box[0][1])),
                (max(align_c[0], box[1][0]), max(align_c[1], box[1][1])),
            ]
            if box[1][0] - box[0][0] > 1 or box[1][1] - box[0][1] > 1:
                return False
        return True
    else:
        if align_c == (1,1):
            return True
        return all(
            align_c == alignment_coords(c)
            for c in match_aligns if c != 'Neutral'
        )


def type_match(creature1, creature2):
    return creature1['Creature Type'] == creature2['Creature Type']


def generate_encounter(rules, options):
    costs = rules.encounter_costs
    min_cost = costs[0]
    party_level = options.party_level
    threat_level = options.threat_level
    creatures = rules.creatures
    creatures = [c for c in rules.creatures if in_level_range(c, party_level)]
    budget = rules.threat_budget[threat_level]
    result_type = None
    result_align = None
    encounter = []

    while budget > min_cost:
        creatures = [c for c in creatures if in_budget(c, party_level, costs, budget)]
        if not len(creatures):
            break
        creature = random.choice(creatures)
        if not result_type:
            result_type = creature['Creature Type']
            if options.same_type:
                creatures = [c for c in creatures if type_match(creature, c)]
        creatures = [c for c in creatures if creature_aligned(c, encounter, options.similar_alignment)]

        encounter.append(creature)
        print_creature(creature)

        budget -= cost_of(creature, party_level, costs)

        if options.verbose:
            print(f"Budget left: {budget}")

def main():
    threats = (
        "Trivial",
        "Low",
        "Moderate",
        "Severe",
        "Extreme",
    )
    parser = argparse.ArgumentParser(
        description='Pathfinder 2 Random Encounter Generator')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument(
        '-p', '--party-level', action='store', type=int, default=1, help='Set the average party level')
    parser.add_argument(
        '-t', '--threat-level', action='store', choices=threats, default='Moderate', help='Set the threat level')
    parser.add_argument(
        '-T', '--same-type', action='store_true', help='Encounter must contian creatures of same type')
    parser.add_argument(
        '-a', '--similar-alignment', action='store_true', help='Alignments can be different, if similar')

    options = parser.parse_args()

    with open('rules.json', 'r') as rules_file:
        rules = PF2Rules(rules_file, options)
        generate_encounter(rules, options)


if __name__ == '__main__':
    main()
