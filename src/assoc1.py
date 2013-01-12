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
    if len( sys.argv ) > 1:
        return tryParseFloat( sys.argv[1], val = defaultSupport )
    return defaultSupport

def usage():
    return ("The first parameter is a minimum support which equals %s if it is not supported" % defaultSupport)

print usage()

def main():
    data = orange.ExampleTable("../data/zz_datasetSample_201201_for_Orange.txt")
    data = orange.Preprocessor_discretize(data, \
      method=orange.EquiNDiscretization(numberOfIntervals=3))
    data = data.select(range(10))

    rules = orange.AssociationRulesInducer(data, support=getSupport())

    print "%i rules with support higher than or equal to %5.3f found.\n" % (len(rules), getSupport())

    orngAssoc.sort(rules, ["support", "confidence"])

    orngAssoc.printRules(rules[:5], ["support", "confidence"])
    print

    del rules[:3]
    orngAssoc.printRules(rules[:5], ["support", "confidence"])
    print

main()