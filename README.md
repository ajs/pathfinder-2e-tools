# A Pathfinder 2e Tools Repository

As I find that I need tools for my Pathfinder 2e games (as a GM or player),
I will throw them here for people to play with, modify and enjoy!

## Installation

These tools use Python, so just use pip to set them up:

    pip install -e .

## `encounter`

The `encounter` tool is a random encounter generator that takes the monster list, randomizes it and then selects an encounter according to a threat level and average party level that you provide.

Use:

	$ pf2e-encounter --help

for more information.

### Example

	$ pf2e-encounter --party-level=10 --threat=Moderate --same-type --similar-alignment
	Dezullon lvl 10 Neutral Plant
	Shambler lvl 6 Neutral Plant
	Shambler lvl 6 Neutral Plant
	Shambler lvl 6 Neutral Plant

## LICENSE

The code in this repository is all licensed under the MIT LICENSE. However, the
rules.json data file is derived from the Pathfinder 2e rules and as such that
file falls under the OGL. It is included here for conviniece, but may be replaced
with creature, NPC, rule and item data from a source of your choosing.

For more detail, see LICENSE.txt and OGL.txt
