# Dataset notes

These are some notes about the datasets contained in the Data Science for Everyone course.

## gender_stats.csv

This dataset is a subset of a larger dataset from the World Bank
on gender and inequality:
<https://data.worldbank.org/data-catalog/gender-statistics>.

The subset is a selection of variables for every country. For
each variable, we have taken the mean of all available values
from 2012 through 2016.

See the `notes` directory of the source repository for the
notebooks that generate the data from the original dataset.

## Country codes etc

The file `un_stats_division_countries.csv` contains information about country
codes and classification. It is a very slightly modified copy of a file
downloaded in March 2019 from the [UN statistics
website](https://unstats.un.org/unsd/methodology/m49/overview).  The
modifications are three single-character edits to replace commas in country
names with semi-colons. It's not clear what the license is, but I will assume,
until someone tells me otherwise, that the data are public domain, and can be
distributed freely.

## Oliner 1988 table 6.8

`oliner_tab6_8a_1.csv` contains data derived from table 6.8 of this book:

Samuel P. Oliner and Pearl M. Oliner (1992) "The Altruistic Personality:
Rescuers of Jews in Nazi Europe". Free Press, New York. ISBN 0-02923829-3.

See <https://github.com/matthew-brett/datasets/oliner1988> for details.

I believe the underlying *data* are not subject to copyright.  To the extent
that this table reflects my own (MBs) arrangement of the data, I release it
under the [PDDL](https://opendatacommons.org/licenses/pddl).

## Houses

`houses.csv` is the Ames house price data set, originally from
<http://jse.amstat.org/v19n3/decock.pdf>.  This is a backup copy of the data
and various documentation files at
<https://github.com/odsti/datasets/tree/master/ames_houses>.  It differs from
the original only in that it is a CSV file, rather than tab-delimited.
