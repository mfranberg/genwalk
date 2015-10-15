import logging
from collections import defaultdict

import mysql.connector

##
# Maps the given sets of variants to nearby genes using
# the snp141 and refFlat table in UCSC.
#
# @param variants A list of rs-numbers.
#
# @return A dict mapping rs-numbers to a list of gene names.
# 
def get_gene_names(variants, window=100000):
    logging.info( "Connecting to genome-mysql.cse.ucsc.edu to annotate variants." )

    cnx = mysql.connector.connect( user='genome', host='genome-mysql.cse.ucsc.edu', database='hg19' )
    cursor = cnx.cursor( )
    cursor.execute( """select S.name, K.geneName from snp141 as S left join refFlat as K on (S.chrom=K.chrom and not (K.txEnd+{1}<S.chromStart or S.chromEnd+{1}<K.txStart) ) where S.name in ({0})""".format( ",".join( map( lambda x: '"' + x + '"', variants ) ), window ) )

    variant_gene = defaultdict( list )
    anno_variants = set( )
    for row in cursor:
        variant_gene[ row[ 0 ] ].append( row[ 1 ].replace( "-AS1", "" ) )
        anno_variants.add( row[ 0 ] )

    logging.info( "{0} of {1} variants could be annotated with +- 100kb.".format( len( anno_variants ), len( variants ) ) )

    cursor.close( )
    cnx.close( )

    return variant_gene

