
import itertools

import pf2e.encounter as encounter


sample_alignments = [
    " ".join(pair) for pair in itertools.product(
        ["Lawful", "Neutral", "Chaotic"],
        ["Good", "Neutral", "Evil"]
    )
]
sample_alignments[5] = "Neutral"

sample_creatures = [
         {
           "Name": f"Creature {i}",
           "Family": f"Type {ctype} Family {ftype}",
           "Level": level,
           "Alignment": align,
           "Creature Type": f"Type ctype",
           "Size": "Medium"
         }
         for i, align in enumerate(sample_alignments)
            for ctype in ("1", "2", "3")
                for ftype in ("1", "2", "3")
                    for level in (1, 5, 8, 10)
]


def test_cost_of():
    costs = [10, 15, 20, 30, 40, 60, 80]
    inrange = lambda x: x['Level'] <= 12 and x['Level'] >= 6
    tenish_creatures = [c for c in sample_creatures if inrange(c)]
    for c in tenish_creatures:
        cost = encounter.cost_of(c, 10, costs)
        assert cost in costs, f"Cost {cost} of {c!r} must be in {costs!r}"
        if c['Level'] == 10:
            assert cost == 40, f"Cost {cost} of level 10 should be 40"

def test_in_budget():
    costs = [10, 15, 20, 30, 40, 60, 80]
    inrange = lambda x: x['Level'] <= 12 and x['Level'] >= 6
    tenish_creatures = [c for c in sample_creatures if inrange(c)]
    for c in tenish_creatures:
        if c['Level'] > 10:
            assert not encounter.in_budget(c, 10, costs, 40), "Level > 10 cannot be afforded"
        else:
            assert encounter.in_budget(c, 10, costs, 40), "Level <= 10 can be afforded"

def test_in_level_range():
    for c in sample_creatures:
        result = encounter.in_level_range(c, 10)
        if c['Level'] < 6:
            assert not result, f"Low level creature: {c!r}"
        elif c['Level'] <= 12:
            assert result, f"In-level creature: {c!r}"
        else:
            assert not result, f"High level creature: {c!r}"

def test_alignment_coords():
    for c in sample_creatures:
        align = c['Alignment']
        result = encounter.alignment_coords(align)
        if align == 'Neutral':
            assert result == (1,1), "Neutral is center"
        elif align.split(' ', 1)[0] == 'Lawful':
            assert result[0] == 0, "Lawful is first"
        elif align.split(' ', 1)[1] == 'Evil':
            assert result[1] == 2, "Evil is last"

def test_creature_aligned():
    ca = encounter.creature_aligned
    true_neutral_creatures = []
    lawful_creatures = []
    evil_creatures = []
    all_creatures = []
    for c in sample_creatures:
        align = c['Alignment']
        if align == 'Neutral':
            assert ca(c, all_creatures), f"Neutral creature aligned: {c!r}"
            assert ca(c, all_creatures, similar=True), f"Neutral creature similar aligned: {c!r}"
            true_neutral_creatures.append(c)
        if align.startswith("Lawful"):
            if align.endswith('Neutral'):
                assert ca(c, lawful_creatures, similar=True), f"Lawful creature similar to lawful: {c!r}"
            lne = [
                cl for cl in lawful_creatures
                if cl['Alignment'].endswith('Neutral') or
                    cl['Alignment'].endswith('Evil')]
            if lne:
                if align.endswith('Evil'):
                    assert ca(c, lne, similar=True), f"Lawful Evil creature similar Lawful Neutral/Evil {c!r}"
                if align.endswith('Good'):
                    assert not ca(c, lne, similar=True), f"Lawful Good creature not similar Lawful Neutral/Evil {c!r}"
            lawful_creatures.append(c)
        if align == 'Neutral Evil':
            assert ca(c, evil_creatures, similar=True), f"Evil creature similar to evil: {c!r}"
            evil_creatures.append(c)

def test_is_aligned():
    assert encounter.is_aligned("Neutral", ["Lawful Evil", "Neutral", "Chaotic Good"], similar=False)
    assert encounter.is_aligned("Lawful Neutral", ["Lawful Evil", "Neutral"], similar=True)
    assert not encounter.is_aligned("Lawful Good", ["Lawful Evil", "Neutral"], similar=True)
    assert not encounter.is_aligned("Lawful Good", ["Chaotic Good", "Neutral"], similar=True)
    assert not encounter.is_aligned("Lawful Neutral", ["Chaotic Neutral", "Neutral"], similar=True)
    assert encounter.is_aligned("Lawful Neutral", ["Neutral", "Neutral"], similar=True)
