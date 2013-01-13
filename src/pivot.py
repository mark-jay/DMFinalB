# import orange, orngAssoc
import sys
import csv

def getItem( row ):
    return row[1]

def getItemsetID( row ):
    return row[0]

# [String] -> Map ItemsetID [Item]
# in our case ItemsetID is a cookie id which is a string a Item is a Product_Id which is a string too
# receives a text as lines and returns FIXME
def getItemsetDict( parsedLines ):
    aMap = dict()
    for row in parsedLines:
        itemsetID, item = getItemsetID( row ), getItem( row )
        items = aMap.get(itemsetID, [])
        items.append(item)
        aMap.update({itemsetID : items})
    return aMap

# receives parsed lines
# returns all possible values from the item column
def getAllItems( splittedLines ):
    aSet = set()
    for splittedLine in splittedLines:
        aSet.add( getItem( splittedLine ) )
    return list( aSet )

# [a] -> (a -> Int)
# receives a list and returns effient( O( lg n ) ) function to find a index by an item
def getIndexFinder( aList ):
    aMap = dict( zip( aList, range( len( aList ) ) ) )
    return aMap.get

def testRes( res ):
    lenFst = len( res[0] )
    def testLen( row ):
        if len( row ) != lenFst:
            sys.stderr.write ( "length of the header = %s, len of the row = %s, where row = %s" % ( lenFst, len( row ), row ) )
            sys.exit()
    map( testLen, res )

# [[String]] -> [String]
def pivot( parsedLines ):
    allItems = getAllItems( parsedLines[1:] )
    allItemsLen = len( allItems )
    findIndex = getIndexFinder( allItems )
    itemsetDict = getItemsetDict( parsedLines[1:] )
    
    res = []
    
    # # printing header
    # header = [getItemsetID( parsedLines[0] )] + allItems
    # res.append( header )

    def repr1( x ): return str(x)#'"' + str(x) + '"'
    
    def toCounted( item, items ):
        cnt = items.count( item )
        if cnt == 1:   
            return repr1( item )
        else: 
            return repr1( item ) + "%" + str( cnt ) # "%" will be replaced by "="
    
    # printting other
    for itemsetID, items in itemsetDict.items():
        arr = []
        for item in list( set( items ) ):
            counted = toCounted( item, items )
            arr.append( counted )
        res.append( arr )

    # testRes( res )
    # print list(itemsetDict)[0:10]
    return map( lambda r: ",".join(r) + "\n", res )

def parseLines( lines ):
    reader = csv.reader( lines, delimiter=',', quoting=csv.QUOTE_ALL ) 
    return list(reader)

def testRead( lines ):
    parsed = parseLines( lines )
    if ( not( all( map( lambda r: len( r ) == 2, parsed ) ) ) ):
        sys.stderr.write( "parsing test failed" )
        sys.exit()

def go( infile, outfile ):
    lines = infile.readlines()[0:200]
    testRead( lines )
    parsedLines = parseLines( lines )
    outfile.writelines( pivot( parsedLines ) )

def main():
    go( sys.stdin, sys.stdout )

main()