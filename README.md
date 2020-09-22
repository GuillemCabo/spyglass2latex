# spyglass2latex
Script to parse spyglass port reports to latex tables.

Tested with SpyGlass\_vO-2018.09-SP1-1 and python2.7

## Usage
` python2.7 spy2tex.py input.rpt output.tex `

## Limitations
*   Only one module shall be pressent in the report.
*   Report shall have the same format as example.rpt. 6 fields for each table.  
*   `...` shall not be used for the name of the signals or comments.
*   Signal names with more than 19 characters may not be parsed propperly. A
Space needs to be added between the type of input and the name, since the
script searches for two or more spaces in order to pace the item separator.
