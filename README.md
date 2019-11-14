# A Pathfinder 2e Tools Repository

As I find that I need tools for my Pathfinder 2e games (as a GM or player),
I will throw them here for people to play with, modify and enjoy!

## Installation

These tools use Python, so just use pip to set them up:

    pip install -e .

## `pf2e-encounter`

The `pf2e-encounter` tool is a random encounter generator that takes the
monster list, randomizes it and then selects an encounter according to a
threat level and average party level that you provide.

Use:

	$ pf2e-encounter --help

for more information.

### Examples

A moderate encounter for a level 10 party of creatures that are all the
same type:

	$ pf2e-encounter --party-level=10 --threat=Moderate --same-type --similar-alignment
	Dezullon lvl 10 Neutral Plant
	Shambler lvl 6 Neutral Plant
	Shambler lvl 6 Neutral Plant
	Shambler lvl 6 Neutral Plant

A moderate encounter for a level 10 party of all undead creatures of
similar alignments, including elite/weak adjustments:

	$ pf2e-encounter --party-level=10 --similar-alignment --adjustments --filter='Creature Type=Undead'
	Graveknight lvl 10 Lawful Evil Undead
	Skeletal Hulk lvl 7 Neutral Evil Undead
	Forge-Spurned (elite adj.) lvl 6 Neutral Evil Undead
	Wraith lvl 6 Lawful Evil Undead

## LICENSE

The **source code** in this repository is all licensed under the MIT
LICENSE.

However the data files and other items in the `ogl-content` directory are
derived from the Pathfinder 2e rules and as such those files fall under
the OGL. It is included here for conviniece, but may be replaced with
creature, NPC, rule and item data from a source of your choosing.

For more detail, see [`LICENSE.txt`](LICENSE.txt) and
[`ogl-content/OGL.txt`](ogl-content/OGL.txt)
