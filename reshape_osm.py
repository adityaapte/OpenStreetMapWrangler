# -*- coding: utf-8 -*-
"""
This program reads osm data from OpenStreetMap and rshapes it to a json file.

Created on Fri May  1 22:42:40 2015

@author: adityaapte
"""

import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
def is_housenumber(elem):
    return (elem.attrib['k'] == "addr:housenumber")
def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")
def is_amenity(elem):
    return (elem.attrib['k'] == "amenity")
def is_name(elem):
    return (elem.attrib['k'] == "name")
        

def audit_amenity(amenity_dict):
    if amenity_dict["amenity"].lower() == "cafe" and "name" in amenity_dict:
        if amenity_dict["name"].lower() == "starbucks":
            amenity_dict["name"] = "Starbucks Coffee"
        if amenity_dict["name"].lower() == "ccd":
            amenity_dict["name"] = "Cafe Coffee Day"        
    return amenity_dict
        
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        created_dict = {}
        pos = [0, 0]
        nds = []
        address_dict = {}
        amenity_dict = {}
        #print "========================",element.tag
        for elem in element.iter():
            #print "---------------",elem.tag
            if elem.tag == "node" or elem.tag == "way":
                
                for key in elem.attrib:
                    if key in CREATED:
                        created_dict[key] = elem.attrib[key]
                        continue
                #if is_address(key):
                #    pass
                    if key == "lat":
                        pos[0] = float(elem.attrib[key])
                        continue
                    if key == "lon":
                        pos[1] = float(elem.attrib[key])
                        continue
                        
                    node[key] = elem.attrib[key]
                    
            if elem.tag == "tag":
                if is_street_name(elem):
                    address_dict["street"] = elem.attrib["v"]
                    continue
                if is_housenumber(elem):
                    address_dict["housenumber"] = elem.attrib["v"]
                    continue
                if is_postcode(elem):
                    address_dict["postcode"] = elem.attrib["v"]
                    continue
                if is_amenity(elem):
                    amenity_dict["amenity"] = elem.attrib["v"]
                if is_name(elem):                    
                    amenity_dict["name"] = elem.attrib["v"]

            if elem.tag == "nd":
                nds.append(elem.attrib["ref"])
                continue
                                                                 
        node["created"] = created_dict
        if "amenity" in amenity_dict:
            node["amenity"] = audit_amenity(amenity_dict)
        if len(address_dict.keys()) > 0:
            node["address"] = address_dict
        if pos != [0,0]:
            node["pos"] = pos
        if len(nds) > 0:
            node["node_refs"] = nds
        node["type"] = element.tag
        #pprint.pprint(node)
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def main():
    print "-----here"
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('/DataWranglingMongoDB/mumbai_india.osm', False)
    #pprint.pprint(data)
    print "end here ---------"
    

if __name__ == "__main__":
    main()
