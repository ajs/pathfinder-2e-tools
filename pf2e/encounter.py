
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
    if 'Alignment' in creature:
        alignment = creature['Alignment']
        creature_type = creature['Creature Type']
        if options.core_format:
            alignment = "".join(a[0] for a in alignment.split(' '))
            tags = [alignment, creature_type]
            if 'Adjustment' in creature:
                tags += [creature['Adjustment']]
            print(f"{name:<40} CREATURE {level:>2d}")
            print(" ".join(f"[{tag.upper()}]" for tag in tags))
        else:
            if 'Adjustment' in creature:
                name += " (" + creature['Adjustment'].lower() + " adj.)"
            print(f"{name} lvl {level} {alignment} {creature_type}")
    else:
        if options.core_format:
            print(f"{name:<40} HAZARD {level:>2d}")
        else:
            print(f"Hazard: {name} lvl {level}")


def alignment_coords(alignment):
    """
    Return a tuple with two integers representing the
    location of the given alignment in the alignment grid.
    e.g. Lawful Good is 0,0 while true Neutral is 1,1.
    """

    if alignment in ('Neutral', 'Any'):
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

    if 'Alignment' not in creature:
        return True
    enc_aligns = [c.get('Alignment', 'Neutral') for c in encounter]
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


def elite(creature):
    """Elite level adjustment"""

    ecreature = creature.copy()
    ecreature['Level'] += 1
    ecreature['Adjustment'] = 'Elite'
    return ecreature


def weak(creature):
    """Weak level adjustment"""

    wcreature = creature.copy()
    wcreature['Level'] -= 1
    wcreature['Adjustment'] = 'Weak'
    return wcreature


def filter_creature(creature, filters):
    for filter_exp in filters.split(','):
        name, value = filter_exp.split('=', 1)
        name = name.strip()
        value = value.strip()
        if value.startswith('~'):
            value = value[1:]
            the_filter = lambda c: value in c[name]
        else:
            the_filter = lambda c: c[name] == value

        match = the_filter(creature)
        if not match:
            return False
    return True


def do_hazard(hazard, hazard_mode, creatures):
    """
    Determine whether or not to include a hazard

    hazard is the flag that says always include

    hazard_mode is described in the command-line options.

    creatures is the base list of creatures (before adjustments).
    """

    if hazard:
        return True
    elif hazard_mode:
        if hazard_mode == 'creature':
            prob = len(creatures)+1
        elif hazard_mode == 'common':
            prob = 2
        elif hazard_mode == 'uncommon':
            prob = 5
        else:
            raise ValueError(f"Unknown hazard mode: {hazard_mode}")
        return random.randint(1,prob) == 1
    else:
        return False


def generate_encounter(rules, options):
    """
    Given rules and command-line options, generate a full encounter.
    """

    costs = rules.encounter_costs
    min_cost = costs[0]
    party_level = options.party_level
    threat_level = options.threat_level
    creatures = rules.creatures.copy()
    hazards = rules.hazards
    budget = rules.threat_budget[threat_level]
    result_type = None
    encounter = []

    if options.adjustments:
        creatures += [elite(c) for c in rules.creatures]
        creatures += [weak(c) for c in rules.creatures if c['Level'] >= 0]
    creatures = [c for c in creatures if in_level_range(c, party_level)]
    if options.filter:
        creatures = [c for c in creatures if filter_creature(c, options.filter)]

    if do_hazard(options.hazard, options.hazard_mode, rules.creatures):
        hazards = [
            h for h in hazards
            if in_level_range(h, party_level) and in_budget(h, party_level, costs, budget)]
        hazard = random.choice(hazards)
        budget -= cost_of(hazard, party_level, costs)
        encounter.append(hazard)

    while budget > min_cost:
        creatures = [c for c in creatures if in_budget(c, party_level, costs, budget)]
        if not len(creatures):
            break
        creature = random.choice(creatures)
        if not result_type:
            result_type = creature['Creature Type']
            if options.same_type:
                creatures = [c for c in creatures if type_match(creature, c)]

        encounter.append(creature)

        creatures = [c for c in creatures if creature_aligned(c, encounter, options.similar_alignment)]

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
    hazard_modes = ('creature', 'common', 'uncommon')
    hazard_modes_help = (
        '("creature" = as common as any creature, '
        '"common" = 50 percent chance, '
        '"uncommon" = 20 percent chance)')

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Pathfinder 2 Random Encounter Generator')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument(
        '-p', '--party-level', action='store', type=int, metavar='LEVEL', default=1, help='Set the average party level')
    parser.add_argument(
        '-t', '--threat-level', action='store', choices=threats, default='Moderate', help='Set the threat level')
    parser.add_argument(
        '--sort', action='store', choices=sorts, default='level', help='Set the output sort mode')
    parser.add_argument(
        '-T', '--same-type', action='store_true', help='Encounter must contian creatures of same type')
    parser.add_argument(
        '-a', '--similar-alignment', action='store_true', help='Alignments can be different, if similar')
    parser.add_argument(
        '--adjustments', action='store_true', help='Include elite/weak adjustments')
    parser.add_argument(
        '--filter', action='store', help='A filter of the form name=value[,name=value,...]')
    parser.add_argument(
        '-e', '--encounters', action='store', type=int, metavar='COUNT', default=1, help='Generate this many encounters')
    parser.add_argument(
        '--hazard', action='store_true', help='Include a hazard')
    parser.add_argument(
        '--hazard-mode', action='store', choices=hazard_modes, help='Hazard chance: ' + hazard_modes_help)
    parser.add_argument(
        '--core-format', action='store_true', help='Format output more like Core Rules')

    options = parser.parse_args()

    with open(PF2RulesFile, 'r') as rules_file:
        rules = PF2Rules(rules_file, options)
        for n in range(1, options.encounters+1):
            if options.encounters > 1:
                print(f"Encounter #{n}")
            generate_encounter(rules, options)
            if options.encounters > 1:
                print("")


if __name__ == '__main__':
    main()
