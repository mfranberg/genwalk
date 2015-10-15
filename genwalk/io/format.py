##
# Takes a path and constructs a string representation.
#
# @param path A list of strings.
#
# @return A string representation of the path.
#
def format_path(path):
    if len( path ) <= 1:
        return "-"
    else:
        return "->".join( path )

##
# Takes a path and a graph and constructs a sequence of
# edge types using the 'type' attribute of the edges.
#
# @param path A list of strings representing nodes in G.
# @param G A graph.
#
# @return A string representation of the edge types on the path.
#
def format_edges(path, G):
    if len( path ) == 0:
        return "-"
    else:
        return ";".join( G[ path[ i ] ][ path[ i + 1 ] ][ "type" ] for i in range( len( path ) - 1 ) )

