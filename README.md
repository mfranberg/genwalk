# Genwalk
The tool genwalk suggests possible paths in a gene-gene interaction network between two genes derived from a pair of genetic variants.

# Installation
The installation is simple:

    > python setup.py install

or if you want to install it for your local user

    > python setup.py install --user

# Usage

To run genwalk on a file cvd.pairs using the biogrid.graph in this repository write:

    > genwalk --graph-file data/biogrid.graph --pair-file cvd.pairs

This will give a list of possible paths between the gene pairs corresponding to the given variant pairs. You can also plot this in graph by:

    > genwalk --graph-file data/biogrid.graph --pair-file cvd.pairs --plot graph.png

