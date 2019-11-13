
import random
import argparse
from .rules import PF2Rules
from .rules import PF2RulesFile


def cost_of(creature, party_level, costs):
    """
    Return the XP budget cost of the given creature in a
    party with average level given by party_level. The costs
    array is indexed by the relative level of the creature to
    the party, plus 4
    """

    return costs[creature['Level'] - party_level + 4]


def in_budget(creature, party_level, costs, budget):
    """
    Does the given creature fit in the budget of the given
    party level party. Costs is the fixed array of XP costs.
    """

    return cost_of(creature, party_level, costs) <= budget


def in_level_range(creature, party_level):
    """
    Is the creature in the appropriate level range for a party
    with average level given by party_level.
    """
    
    creature_level = creature['Level']
    min_level = party_level - 4
    max_level = party_level + 2
    return (creature_level >= min_level and creature_level <= max_level)


def print_creatures(creatures, options):
    """Print out the creatures in the encounter"""

    def namekey(obj):
        return obj['Name']

    def levelkey(obj):
        return (-obj['Level'], namekey(obj))

    def typekey(obj):
        return (obj['Creature Type'], namekey(obj))

    sortkeymap = dict(level=levelkey, name=namekey, type=typekey)

    try:
        sortkey = sortkeymap[options.sort]
    except KeyError:
        raise ValueError(f"Unknown sort mode {options.sort}")

    for creature in sorted(creatures, key=sortkey):
        print_creature(creature, options)


def print_creature(creature, options):
    """
    Print out the creature's one-line summary
    """

    name = creature['Name']
    level = creature['Level']
    alignment = creature['Alignment']
    creature_type = creature['Creature Type']
    print(f"{name} lvl {level} {alignment} {creature_type}")


def alignment_coords(alignment):
    """
    Return a tuple with two integers representing the
    location of the given alignment in the alignment grid.
    e.g. Lawful Good is 0,0 while true Neutral is 1,1.
    """

    if alignment == 'Neutral':
        return (1,1)
    parts = alignment.split(' ', 1)
    locs = {
        'Lawful': 0, 'Neutral': 1, 'Chaotic': 2,
        'Good': 0, 'Evil': 2,
    }
    return tuple(locs[p] for p in parts)


def creature_aligned(creature, encounter, similar=False):
    """
    Is the given creature in keeping with the alignment of the
    given array of creatures in encounter. If similar is true,
    then alignements that are "one step" away are alloed. Otherwise
    creature and all elements of encounter must either be the same
    alignment or true Neutral.
    """

    enc_aligns = [c['Alignment'] for c in encounter]
    return is_aligned(creature['Alignment'], enc_aligns, similar)

def is_aligned(target_align, match_aligns, similar):
    """
    See creature_aligned for details. This function does the
    work of matching alignments, but works from the alignments
    themselves, not the creature stats overall.
    """

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
    """Are the creatures of the same type?"""

    return creature1['Creature Type'] == creature2['Creature Type']


def generate_encounter(rules, options):
    """
    Given rules and command-line options, generate a full encounter.
    """

    costs = rules.encounter_costs
    min_cost = costs[0]
    party_level = options.party_level
    threat_level = options.threat_level
    creatures = [c for c in rules.creatures if in_level_range(c, party_level)]
    budget = rules.threat_budget[threat_level]
    result_type = None
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

        budget -= cost_of(creature, party_level, costs)

        if options.verbose:
            print(f"Budget left: {budget}")

    print_creatures(encounter, options)

def main():
    """
    Parse command-line, read rule data and then call
    generate_encounter.
    """

    threats = (
        "Trivial",
        "Low",
        "Moderate",
        "Severe",
        "Extreme",
    )
    sorts = ('level', 'name', 'type')

    parser = argparse.ArgumentParser(
        description='Pathfinder 2 Random Encounter Generator')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument(
        '-p', '--party-level', action='store', type=int, default=1, help='Set the average party level')
    parser.add_argument(
        '-t', '--threat-level', action='store', choices=threats, default='Moderate', help='Set the threat level')
    parser.add_argument(
        '--sort', action='store', choices=sorts, default='level', help='Set the output sort mode')
    parser.add_argument(
        '-T', '--same-type', action='store_true', help='Encounter must contian creatures of same type')
    parser.add_argument(
        '-a', '--similar-alignment', action='store_true', help='Alignments can be different, if similar')

    options = parser.parse_args()

    with open(PF2RulesFile, 'r') as rules_file:
        rules = PF2Rules(rules_file, options)
        generate_encounter(rules, options)


if __name__ == '__main__':
    main()
