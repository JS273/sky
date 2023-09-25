# Sky 

With this package comes the necessariy toolbox for the [pyhon-project-template](https://github.com/JS273/python-project-template)
It provides all needed utilities when working with in the template project.

## Getting Started

Install the package via `pip install -e .`. So every change will be immediately available.
Usually onlyon the plotlib stylesheets, changes may be made.
Here one can either upload personal stylesheet or edit the existing ones.

## Basic Structure

The sky packages comes with 4 major methods:
- `filemanager` creates the folder structure for saving the results of your calcualtions
- `plotlib` contains often used plots with basic settings. Here new plot classes can be added.
- `datastructures` is a basic format for the plotlib tool.
- `latexExporter` exports the generated grafics into a tex flie via the inkscape export.
- `translationsRules` For text calles within the math mode of LaTeX one needs placeholders since the export from matplotlib genreates the command not the resulting text. So the desired text needs to be replaced with letters with the same scaling. Lateron they will be replaced by the correct command.

