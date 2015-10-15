import sys
import click
import itertools
import pygraphviz as pgv
import logging

from genwalk.io import util
from genwalk.io import format
from genwalk.io import anno
from genwalk.algo import graph

##
# Construct a list of unique variants from a list of pairs.
#
# @param pairs A list of pairs (either as tuples or lists)
#
# @return A list of unique variants in the pairs.
#
def flatten(pairs):
    variants = set( )
    for var1, var2 in pairs:
        variants.add( var1 )
        variants.add( var2 )

    return list( variants )

@click.command( short_help="For each pair of variants the set of shortest paths is found." )
@click.option( '--graph-file', type=click.File( "r" ), help = "A graph between genes.", required = True )
@click.option( '--variant-gene-file', type=click.File( "r" ), help = "A file mapping variants to genes", required = False )
@click.option( '--pair-file', type=click.File( "r" ), help = "A file mapping variants to genes", required = True )
@click.option( '--log-file', type=click.Path( writable=True ), help = "The log file.", required = False )
@click.option( '--out', help='Resulting genes', type=click.File( 'w' ), default = sys.stdout, required = True )
@click.option( '--plot', help="Graph showing all paths", type=click.Path( writable = True ), required = False )
def main(graph_file, variant_gene_file, pair_file, log_file, out, plot):
    G = util.parse_graph( graph_file )
    pairs = util.parse_pairs( pair_file )

    if log_file:
        logging.getLogger( '' ).handlers = []
        logging.basicConfig( filename = log_file, level = logging.DEBUG, filemode = "w" )
        logging.info( "Hello" )
    
    variant_gene = None
    if variant_gene_file:
        variant_gene = util.parse_variant_gene( variant_gene_file )
    else:
        variant_gene = anno.get_gene_names( flatten( pairs ) )

    out.write( "snp1 snp2\tgenepath\texperiment_types\n" )
    for pair, path in graph.find_paths( pairs, variant_gene, G ):
        out.write( "{0} {1}\t{2}\t{3}\n".format( pair[ 0 ], pair[ 1 ], format.format_path( path ), format.format_edges( path, G ) ) )

    if plot:
        logging.info( "Constructing graph" )
        PG = pgv.AGraph( directed = True )
        for pair, path in graph.find_paths( pairs, variant_gene, G ):
            for i in range( len( path ) - 1 ):
                PG.add_edge( path[ i ], path[ i + 1 ] )

            PG.get_node( path[ 0 ] ).attr[ "color" ] = "red"
            PG.get_node( path[ -1 ] ).attr[ "color" ] = "red"

        PG.layout( )
        PG.draw( plot, prog = "dot" )
