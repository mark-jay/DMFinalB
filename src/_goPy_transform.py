# to use accented characters in the code
# -*- coding: cp1252 -*-
# ===============================
# author: Paulo Trigo Silva (PTS)
# since: NOV.2012
# version: v01
# ===============================



#_______________________________________________________________________________
# Modules to Evaluate
import csv
import unicodedata
import sys
from operator import add


#_______________________________________________________________________________
# convert string to unicode format
def to_unicode( obj, encoding='utf-8' ):
    if isinstance( obj, basestring ):
        if not isinstance( obj, unicode ):
            obj = unicode( obj, encoding )
    return obj


#_______________________________________________________________________________
# remove accentes in an unicode string
def remove_accents( aString, encoding='utf-8' ):
    aString_unicode = to_unicode( aString, encoding )
    nfkd_form = unicodedata.normalize( 'NFKD', aString_unicode )
    only_ascii_form = nfkd_form.encode( 'ascii', 'ignore' )
    return only_ascii_form


#_______________________________________________________________________________
# define the "normalize" process that applies to each string
def normalizeString( aString ):
    # substitute "=" symbol because it is used in the basket format
    symbolToReplace = "="
    symbolNew = "|"
    aString = aString.replace( symbolToReplace, symbolNew )
    
    # eliminate spaces (white characters)
    symbolToReplace = " "
    symbolNew = ""
    aString = aString.replace( symbolToReplace, symbolNew )
    
    # eliminate tabs
    symbolToReplace = "\t"
    symbolNew = ""
    aString = aString.replace( symbolToReplace, symbolNew )
    
    # eliminate accent characters
    encoding_windows = "iso-8859-1" #"cp1252" #"latin-1" #"latin9" 
    aString = remove_accents( aString, encoding_windows )
    
    # to lower
    aString = aString.lower()

    return aString



#_______________________________________________________________________________
# generate the "basket information" from a dataset file with the format:
# TransactioID;ProductID
def generateBasket( fileNameIN ):
    def encloseString( string ):
        return '"' + string + '"'
    indexTransaction = 0
    indexItem = 1
    basket = []
    with open( fileNameIN, 'rb' ) as f:
        # have to set QUOTE_ALL to make the parser work well
		# otherwise it could raise an error when see enclosed tab like "tabbed\ttext"
        reader = csv.reader( f, delimiter=',', quoting=csv.QUOTE_ALL ) 
        for i, row in enumerate(reader):
            if True:
                # print "row: ", map(normalizeString, row)
                r = map(encloseString, map(normalizeString, row))
                basket.append(r)
            
    return basket

#_______________________________________________________________________________
# generate a dataset file with the ".basket" structure expected by Orange"
def generateDataFile( basket, fileNameOUT ):
    def interpolateWith( array, symbol ):
	    return reduce(lambda acc, c: acc + symbol + c, array)
    with open ( fileNameOUT, 'w') as f:
        for row in basket:
            f.writelines(interpolateWith( row, "\t" ))
            f.write("\n")
    
#_______________________________________________________________________________
# getting command line args
def getIO():
    def usage():
        return ("the first and the second argument should be a input and output file")
    if len( sys.argv ) == 3:
        return (sys.argv[1], sys.argv[2])
    elif len( sys.argv ) == 1:
        return ( sys.stdin, sys.stdout )
    else:
        print usage()
        sys.exit()

#_______________________________________________________________________________
# the main of this module (in case this module is imported from another module)
if __name__=="__main__":
    # assumption: the CSV file does not contain the header line
    # (make sure that the export script does not generate the CSV header)
    
	# fIN = "zz_dataset_2012_01.txt"
	# fIN = "z_datasetSample_201201.txt"
    fIN, fOUT = getIO()
    print
    print ">> 1. Generate Basket"
    basket = generateBasket( fIN )
    print ">> 2. Generate .basket dataset file"
    generateDataFile( basket, fOUT )





