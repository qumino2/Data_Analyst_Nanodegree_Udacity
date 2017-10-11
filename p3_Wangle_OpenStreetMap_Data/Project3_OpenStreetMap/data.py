#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "Beijing_China.osm"

NODES_PATH = "Beijing_nodes_cleaned.csv"
NODE_TAGS_PATH = "Beijing_nodes_tags_cleaned.csv"
WAYS_PATH = "Beijing_ways_cleaned.csv"
WAY_NODES_PATH = "Beijing_ways_nodes_cleaned.csv"
WAY_TAGS_PATH = "Beijing_ways_tags_cleaned.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

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


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in unexpected:
            weird_street_type = street_type
            name = name.replace(weird_street_type, mapping[weird_street_type])

    return name

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE id 'node': {'id': 757860928,


    if element.tag == 'node':
        for attrib in ['id', 'user', 'uid', 'version', 'lat', 'lon', 'timestamp', 'changeset']:
            node_attribs[attrib] = element.attrib[attrib]

        for tag in element.iter('tag'):
            if not PROBLEMCHARS.search(tag.attrib['k']):
                dic = {}
                dic['id'] = element.attrib['id']
                print tag.attrib['k']
                if ":" not in tag.attrib['k']:
                    dic['key'] = tag.attrib['k']
                    dic['value'] = tag.attrib['v']
                    dic['type'] = 'regular'
                else:
                    dic['key'] = tag.attrib['k'].split(':', 1)[1]
                    dic['value'] = tag.attrib['v']
                    dic['type'] = tag.attrib['k'].split(':', 1)[0]
                tags.append(dic)


        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        for attrib in ['id', 'user', 'uid', 'version', 'timestamp', 'changeset']:
            way_attribs[attrib] = element.attrib[attrib]

        for tag in element.iter('tag'):
            if not PROBLEMCHARS.search(tag.attrib['k']):
                dic = {}
                dic['id'] = element.attrib['id']
                dic['value'] = tag.attrib['v']
                print tag.attrib['k']
                if ":" not in tag.attrib['k']:
                    dic['key'] = tag.attrib['k']
                    dic['type'] = 'regular'
                else:
                    dic['key'] = tag.attrib['k'].split(':', 1)[1]
                    dic['type'] = tag.attrib['k'].split(':', 1)[0]
                    if tag.attrib['k'] == 'name:en':
                      dic['value'] = update_name(tag.attrib['v'], mapping)
                tags.append(dic)
        position = 0
        for nd in element.iter('nd'):
            dic = {}
            dic['id'] = element.attrib['id']
            dic['node_id'] = nd.attrib['ref']
            dic['position'] = position
            position += 1
            way_nodes.append(dic)



        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)
