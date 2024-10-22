# RichChk

RichChk is a cross-platform Python library that parses StarCraft's [CHK format](http://www.starcraftai.com/wiki/CHK_Format) into a **richer**, human readable representation for editing all aspects of a Stacraft map (.SCM/.SCX files) inside Python.  RichChk implements the CHK format specified in [Staredit.net CHK format wiki](http://www.staredit.net/wiki/index.php/Scenario.chk).  This project was originally called chkjson, but that name no longer fits since the library does much more than turn CHK into JSON.  The CHK data can be safely edited in Python and then written back to a playable .SCX/.SCM Starcraft map file.

RichChk offers numerous advantages over the traditional method of using a GUI based editor for creating a custom map.  These include:

* Edit a map directly from Python to a .SCX/.SCM map file.  No copy+pasting triggers needed!
* Ergonomically write many triggers in a Python/text based format without using a GUI.
* Leverage all the power of Python/version control to organize triggers, unit settings, etc. outside of a map file for high maintainability and portability.
* Unify static data (unit settings, player settings, etc.) with Trigger data.  Trigger data can programmatically reference static data when building a map.  


RichChk is not a full replacement for traditional GUI editors (e.g. ScmDraft 2) which should still be used for terrain/unit/location placements.  Other key omissions are listed below:

* No support for modded StarCraft
* No support for EUDs
* No support for map protection
* No support for CHK section stacking

## Installation

Python 3.11 is required.  Other versions of Python may work but are not tested.  Complete the following steps on a terminal or command line program.

* Clone master branch: `git clone https://github.com/sethmachine/richchk`
* Enter the root directory of the repo, e.g. `cd richchk/`
* Run `pip install src/ --upgrade`
* Verify `richchk` is installed: `python -c "import richchk; print(richchk.__file__)"`

### StormLib

[StormLib](http://www.zezula.net/en/mpq/stormlib.html) is an open source library used to read and write data to MPQ archives, which is the file format that StarCraft maps are stored in (a .SCM/.SCX file).  StormLib is only required if you wish to directly edit a StarCraft map or add WAV files.  RichChk can edit the CHK itself without using StormLib, as the CHK can exist outside of the MPQ archive (but not as a playable map).  Nevertheless, the majority of workflows will likely produce new map files, in which case StormLib is a requirement.

For convenience, RichChk comes with 3 embedded StormLib DLLs compiled for Windows (64-bit), macOS apple silicon, and Linux (64-bit).  Relying on the embedded DLLs is highly discouraged for many reasons: the DLLs will eventually no longer work for newer OS/architectures, RichChk is not meant to serve as a build repository for StormLib, DLLs without trusted sources can be dangerous, etc.

Thus, you are highly encouraged to always bring your own StormLib DLL.  Some package managers can build StormLib for you, e.g. [macOS Homebrew StormLib formula](https://formulae.brew.sh/formula/stormlib).

StormLib is absolutely required when using any IO classes from `richchk.io.mpq`.  These IO classes specialize in reading and write CHK data to and from StarCraft map files.

### Configuration

RichChk can be externally configured by specifying a path to a local YAML configuration file using an environment variable.  Set `io.sethmachine.richchk.config` environment variable to point to a local YAML configuration file, e.g. on macOS `export io.sethmachine.richchk.config=my-config.yaml`.

Currently the config only supports changing the logging level (verbosity).  The default logging level is `WARNING` but can be made more verbose by setting it to `INFO`, `DEBUG` or `TRACE`.  This affects the logging level for every logger in RichChk.  

Example YAML config that sets the log level to `DEBUG`:

```yaml
logging:
  level: DEBUG
```

Note the above is the only possible configuration supported at the moment (changing the logging level).  In the future additional configuration options may be available.  

## Usage

Specific examples are provided in the [examples/](examples/) top level folder.  These showcase the basic operations of a reading a map's CHK data, adding new data, and saving it to a new map.  [hello_world.py](examples/hello_world.py) illustrates how to edit unit settings data and display messages.  [hyper_triggers.py](examples/hyper_triggers.py) shows how to add hyper triggers to a map and demonstrates this by spawning many Zerglings quickly in the map center.

To use RichChk for map development, it is best to divide a map into two logical divisions:

* A .SCM/.SCX map file containing the terrain, pre-placed units, pre-placed locations, etc. (anything that is best done in a graphical interface)
* A set of RichChk Python scripts that represent the triggers, unit setting data, etc.  

Producing a new map typically involves the following steps:

1.  Load the map in memory, e.g. `StarcraftMpqIo#read_chk_from_mpq`
1.  Edit the desired sections, e.g. to add new triggers use `RichTrigEditor#add_triggers`
1.  Create a new CHK with the edited section(s), e.g. `RichChkEditor#replace_chk_section`
1.  Save the new CHK to a new map file, e.g. `StarcraftMpqIo#save_chk_to_mpq`

Whenever a map is "edited", a new map file should be created everytime.  It is highly discouraged to replace the map file being edited, as this risks loss of data.  Existing maps should be viewed as immutable--they cannot be changed, only used to make newer versions.  The RichChk file I/O operations have safeguards that prevent overwriting exist files, but these flags can be disabled in each method.  


## Design Philosophy

RichChk is a statically typed Python codebase, leveraging [mypy](https://mypy-lang.org/) for enforcing static type checking.  RichChk's technical design is focused on functional style programming, separating data from business logic.  This means for a single concept, such as a CHK section, there will be at least 2 Python classes/files: one for modeling just the data, and a 2nd for manipulating the model.  All manipulations produce new objects, making code easier to read about since there are no in place modifications or mutations.  Related to this, RichChk's classes are designed to be modular.  This means each class generally does a singular operation, and complex operations are produced by chaining together many specialized classes.  

RichChk also comes with a large test suite that verifies CHK data is being properly read, edited, and written back.  This gives confidence in developing new features and prevents regressions when changes are made.  

RichChk does not need to know how to parse every CHK section into a rich representation to work, and gracefully handles partial state by having special handlers for as-of-yet unmodeled parts of the CHK format.  

RichChk does its best not to mutate data.  What this means is if a CHK section is decoded into a rich format and then written back without being edited, the original binary CHK section should be unchanged.  

For a consistent and lint-free codebase, the codebase uses the [pre-commit framework](https://pre-commit.com/) for both local development, and as part of GitHub Action Workflows to prevent unformatted code from merging in the codebase.  These linters and checks include [mypy](https://mypy-lang.org/), [isort](https://pycqa.github.io/isort/), [docformatter](https://pypi.org/project/docformatter/), [flake8](https://flake8.pycqa.org/en/latest/), and [black](https://github.com/psf/black).

In summary:

* Statically typed Python codebase using [mypy](https://mypy-lang.org/).
* Functional programming style, separating data from business logic.
* Modularity and isolation of functionality to specialist classes; each class should have a single core function.
* Large unit test suite to verify the library works, and make it easier to add new functionality/avoid regressions.
* Handle partial parse of CHK format; RichChk works even if it does not understand every CHK section.
* No mutation of data when writing back unchanged CHK sections.  
* Use [pre-commit framework](https://pre-commit.com/) for uniform and consistent code style with isort, docformatter, flake8, and black


## Transcoder Architecture

TBD



## Contributions

Contributions are welcome!  There are several ways to contribute:

* Review the open issues and make a branch to address one of these.
* Review the [CHK format](http://www.starcraftai.com/wiki/CHK_Format) and propose adding support for an unhandled CHK section.
* Create a new issue to improve an existing feature, fix a bug, add tests, etc. and propose a fix.

Contributions should follow the [design philosophy](#design-philosophy), and re-use as much existing components as possible.  There are already patterns for most common scenarios and these should be repeated when possible.  

The repository has pre-commit and unit test checks in place to prevent merges to the master branch, so you will want to replicate these locally before opening a pull request.  

To get started, install [pre-commit](https://pre-commit.com/#install) in your local development environment.  There is extensive documentation on how pre-commit works.  This will ensure your code locally passes the checks before you can even open a pull request.  

[PyCharm Community Edition](https://www.jetbrains.com/pycharm/download) is the recommended IDE and is available for free. 

I recommend using Python virtual environments to manage local development.  I use [miniconda](https://docs.anaconda.com/free/miniconda/) but any equivalent tool will work too.  

I also recommend integrating the static typing check and linting tools like mypy, flake8, black, isort, and docformatter directly into the IDE.  You can use [File Watchers](https://www.jetbrains.com/help/pycharm/using-file-watchers.html) to automatically reformat your Python code when you save the file.  This will help reduce manual reformatting and avoid headaches if pre-commit checks fail.  


## Acknowledgements

Many thanks to the StarCraft community for providing a wealth of knowledge, libraries, and existing examples that made RichChk possible:

* [staredit.net](http://www.staredit.net/): a vibrant StarCraft community that has always been helpful and answered many questions, and intensively documented the [staredit\\Scenario.chk](http://www.staredit.net/wiki/index.php/Scenario.chk) format.
* [StormLib](https://www.zezula.net/en/mpq/stormlib.html): Ladislav Zezula for creating and maintaining StormLib, which is the foundation of most mapping tools.
* [PyMS](https://github.com/poiuyqwert/PyMS): poiuyqwert's BroodWar modding suite provided some helpful examples on how to use StormLib in Python correctly