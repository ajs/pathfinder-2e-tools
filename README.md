# A Pathfinder 2e Tools Repository

As I find that I need tools for my Pathfinder 2e games (as a GM or player),
I will throw them here for people to play with, modify and enjoy!

## Installation

These tools use Python, so just use pip to set them up:

    pip install -e .

### Windows Installation

Under Windows 10, the Windows Linux Subsystem makes running tools like python
scripts much easier than it used to be! To use it, follow these instructions:

* Go to the Start menu and type "Ubuntu"
* Select "Install App"
* Follow the instructions for enabling WSL if given (may require a one-time reboot) and setting up Linux as instructed
* Go to the Start menu and type "Ubuntu" and this time run the app
* In the new shell run:
  * `sudo apt install build-essential python3-venv` # *Give your password and/or answer yes if prompted*
  * `git clone https://github.com/ajs/pathfinder-2e-tools.git` # *This fetches the tools*
  * `python3 -m venv ~/.venv/pathfinder-2e-tools` # *This creates a place to install the tools*
  * And now you can actually install the tools:
  * `. ~/.venv/pathfinder-2e-tools/bin/activate && pip install -e pathfinder-2e-tools`

Now you're ready to go! Whenever you start the Ubuntu shell back up, just run that last command to get
yourself back into the virtual environment that has the tool installed and update any libraries as
needed. To pull down the latest version of the package, use:

* `cd pathfinder-2e-tools && git pull && pip install -e .`

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
