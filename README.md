# RichChk

RichChk is a Python library that parses Starcraft's [CHK format](http://www.starcraftai.com/wiki/CHK_Format) into a **richer**, human readable representation for editing all aspects of a Stacraft map inside Python.  RichChk implements the CHK format specified in [Staredit.net CHK format wiki](http://www.staredit.net/wiki/index.php/Scenario.chk).  This project was originally called chkjson, but that name no longer fits since the library does much more than turn CHK into JSON.  The CHK data can be safely edited in Python and then written back to a playable .SCX/.SCM Starcraft map file.  

RichChk offers numerous advantages over the traditional method of using a GUI based editor for creating a custom map.  These include:

* Ergonomic way to write many triggers in a Python/text based format without using mouse or GUI.  
* Leverage all the power of Python/version control to organize triggers, unit settings, etc. outside of a map file for high maintainbility and portability.
* Unify static data (unit settings, player settings, etc.) with Trigger data.  Trigger data can programmatically reference static data when building a map.  


RichChk is not a full replacement for traditional GUI based editors which should be used for terrain/unit/location placements, and instead is meant to be used alongside these.  Other key omissions are listed below.  Support for these could be added in the future.  

* No support for modded Starcraft
* No support for EUDs
* No support for map protection
* No support for CHK section stacking

## Installation

Python 3.10 is required.  Other versions of Python may work but are not tested.  Complete the following steps on a terminal or command line program.

* Clone the master branch
* Enter the root directory of the repo
* Run `pip install src/ --upgrade`
* Verify `richchk` is installed: `python -c "import richchk; print(richchk.__file__)"`


## Examples

TBD

## Design Philosophy

RichChk is a statically typed Python codebase, leveraging [mypy](https://mypy-lang.org/) for enforcing static type checking.  RichChk's technical design is focused on functional style programming, separating data from business logic.  This means for a single concept, such as a CHK section, there will be at least 2 Python classes/files: one for modeling just the data, and a 2nd for manipulating the model.  All manipulations produce new objects, making code easier to read about since there are no in place modifications or mutations.  Related to this, RichChk's classes are designed to be modular.  This means each class generally does a singular operation, and complex operations are produced by chaining together many specialized classes.  

RichChk also comes with a large test suite that verifies CHK data is being properly read, edited, and written back.  This gives confidence in developing new features and prevents regressions when changes are made.  

RichChk does not need to know how to parse every CHK section into a rich representation to work, and gracefully handles partial state by having special handlers for as-of-yet unmodeled parts of the CHK format.  

RichChk does its best not to mutate data.  What this means is if a CHK section is decoded into a rich format and then written back without being edited, the original binary CHK section should be unchanged.  

For a consistent and lint-free codebase, the codebase uses the [pre-commit framework](https://pre-commit.com/) for both local development, and as part of GitHub Action Workflows to prevent unformatted code from merging in the codebase.  These linters and checks include [mypy](https://mypy-lang.org/), [isort](https://pycqa.github.io/isort/), [docformatter](https://pypi.org/project/docformatter/), [flake8](https://flake8.pycqa.org/en/latest/), and [black](https://github.com/psf/black).

In summary:

* Statically typed Python codebase using [mypy](https://mypy-lang.org/).
* Functional programmign style, separating data from business logic.  
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


