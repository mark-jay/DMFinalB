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

# [[String]] -> [String]
def pivot( parsedLines ):
    allItems = getAllItems( parsedLines[1:] )
    allItemsLen = len( allItems )
    findIndex = getIndexFinder( allItems )
    itemsetDict = getItemsetDict( parsedLines[1:] )
    
    res = []
    
    # printing header
    header = [getItemsetID( parsedLines[0] )] + allItems
    res.append( header )

    # printting other
    for itemsetID, items in itemsetDict.items():
        arr = ["0"]*allItemsLen
        for item in items:
            idx = findIndex( item )
            arr[idx] = "1"
        arr = [itemsetID] + arr
        res.append(arr)
    
    #print list(itemsetDict)[0:10]
    return map( lambda r: ",".join(map(repr, r)) + "\n", res )

def parseLines( lines ):
    reader = csv.reader( lines, delimiter=',', quoting=csv.QUOTE_ALL ) 
    return list(reader)

def testRead( lines ):
    parsed = parseLines( lines )
    if ( not( all( map( lambda r: len( r ) == 2, parsed ) ) ) ):
        print "parsing test failed"
        sys.exit()

def go( infile, outfile ):
    lines = infile.readlines()
    testRead( lines )
    parsedLines = parseLines( lines )
    outfile.writelines( pivot( parsedLines ) )

def main():
    go( sys.stdin, sys.stdout )

main()