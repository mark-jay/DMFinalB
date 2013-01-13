# Description: Creates a list of association rules, selects five rules and prints them out
# Category:    description
# Uses:        imports-85
# Classes:     orngAssoc.build, Preprocessor_discretize, EquiNDiscretization
# Referenced:  assoc.htm

import orange
import sys
import orngAssoc

def tryParseFloat(s, val=None):
  try:
    return float(s)
  except ValueError:
    return val

defaultSupport = 0.9

def getSupport():
    if len( sys.argv ) > 2:
        return tryParseFloat( sys.argv[2], val = defaultSupport )
    return defaultSupport

def getFile():
    if len( sys.argv ) > 1:
        return sys.argv[1]
    print usage()
    sys.exit()

def usage():
    return ("The first parameter is filepath, and the second is a minimum support which equals %s if it is not supported" % defaultSupport)

def main():
    print ("searching in a file '%s' ..." % getFile())
    print
    data = orange.ExampleTable(getFile())
    # data = orange.Preprocessor_discretize(data, method=orange.EquiNDiscretization(numberOfIntervals=3))
	### uncomment if not working
    # data = data.select(range(10))

    # print orange.maxItemSets
    rules = orange.AssociationRulesSparseInducer(data, support=getSupport())

    print "%i rules with support higher than or equal to %5.3f found.\n" % (len(rules), getSupport())

    orngAssoc.sort(rules, ["confidence", "support"])

    orngAssoc.printRules(rules[:40], ["support", "confidence"])
    print

main()