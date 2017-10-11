#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample_k_20.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


unexpected = ["Lu", "road", "Rd.", "St", "Str", "Str.", "street"]

# UPDATE THIS VARIABLE
mapping = { "Lu": "Road",
            "road": "Road",
            "Rd.": "Road",
            "St": "Street",
            "Str": "Street",
            "Str.": "Street",
            "street": "Street"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type in unexpected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "name:en")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        weird_street_type = m.group()
        print weird_street_type
        # if weird_street_type in mapping.keys():

        name = name.replace(weird_street_type, mapping[weird_street_type])

    return name



def test():
    st_types = audit(OSMFILE)

    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name



if __name__ == '__main__':
    test()