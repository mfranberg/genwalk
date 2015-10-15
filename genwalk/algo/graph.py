import itertools
import logging
import networkx

##
# Finds the shortest paths between pairs of genes corresponding to pairs of variants.
#
# @param pairs A list of variant pairs.
# @param variant_gene A mapping from variant to gene.
# @param G A graph in which genes are nodes.
# 
# @return A generator for all paths between genes corresponding to each variant pair.
# 
def find_paths(pairs, variant_gene, G):
    logging.info( "Discovering shortest paths." )
    for var1, var2 in pairs:
        gene1 = variant_gene.get( var1, None )
        gene2 = variant_gene.get( var2, None )

        if not gene1 or not gene2:
            yield( (var1, var2), [] )
            continue

        for g1, g2 in itertools.product( gene1, gene2 ):
            if g1 == g2 or g1 not in G or g2 not in G:
                continue

            path_list = networkx.all_shortest_paths( G, g1, g2 )

            for p in path_list:
                yield ( (var1, var2), p )

