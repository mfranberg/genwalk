import networkx
import logging
from collections import defaultdict

##
# Constructs a graph from the given file object.
# The file is assumed to consist of lines on the form:
# gene1 gene2 edge_type
#
# The edges will have the 'type' attribute set to edge_type.
#
# @return A networkx undirected graph object.
#
def parse_graph(graph_file):
    G = networkx.Graph( )
    for line in graph_file:
        gene1, gene2, exp_type = line.strip( ).split( "\t" )

        G.add_edge( gene1, gene2 )
        G[ gene1 ][ gene2 ][ "type" ] = exp_type.replace( " ", "_" )

    return G

##
# Constructs a mapping from variants to a list of nearby genes.
# The file is assumed to consist of lines on the form:
# variant gene
#
# where each variant may occur on multiple lines.
#
# @param variant_gene_file A file object.
#
# @return A dict mapping a variant to a list of genes.
#
def parse_variant_gene(variant_gene_file):
    variant_gene = defaultdict( list )
    for line in variant_gene_file:
        variant, gene = line.strip( ).split( )

        variant_gene[ variant ].append( gene )

    return variant_gene

##
# Constructs a list of pairs from the input file.
# The file is assumed to consist of lines on the form:
# variant1 variant2 
# 
# @param pair_file A file object.
#
# @return A list of pairs.
#
def parse_pairs(pair_file):
    pairs = list( )
    for line in pair_file:
        variant1, variant2 = line.strip( ).split( )

        pairs.append( ( variant1, variant2 ) )
    
    logging.info( "Parsed {0} pairs.".format( len( pairs )  ) )

    return pairs

