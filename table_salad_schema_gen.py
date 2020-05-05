#!/usr/bin/env python

import argparse
import csv
import yaml
import json

from pprint import pprint

DEFAULT_CONTEXT = {
    "dc": "http://purl.org/dc/terms/",
    "cred": "https://w3id.org/credentials#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "prov": "http://www.w3.org/ns/prov#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "schema": "http://schema.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def compact_iri(iri_to_compact, context):
    compact_iri = None
    for prefix, iri in context.items():
        if iri_to_compact.startswith(iri):
            compact_iri = iri_to_compact.replace(iri, prefix + ":")
    return compact_iri


def parse_context(path_to_context):
    with open(path_to_context) as f:
        context = json.load(f)
    return context


def merge_contexts(default_context, additional_context):
    for prefix, iri in additional_context.items():
        if prefix not in default_context.keys():
            default_context.update({prefix:iri})
    return default_context


def parse_table(path_to_table):
    parsed_table = []
    with open(path_to_table) as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed_table.append(row)
    return parsed_table
  

def main(args):
    output = {}
    parsed_table = parse_table(args.input)
    if (args.context):
        provided_context = parse_context(args.context)
        context = merge_contexts(DEFAULT_CONTEXT, provided_context)
    else:
        context = DEFAULT_CONTEXT

    output['$namespaces'] = context

    output['$graph'] = [{}]
    
    if args.name:
        output['$graph'][0]['name'] = args.name
    else:
        output['$graph'][0]['name'] = 'SchemaClass'

    output['$graph'][0]['documentRoot'] = 'true'
    output['$graph'][0]['type'] = 'record'
    
    fields = {}
    for record in parsed_table:
        field = {
            'type': record['type'],
            'doc': record['doc'],
        }
        compacted_iri = compact_iri(record['iri'], context)
        if compacted_iri:
            field['jsonldPredicate'] = {
                '_id': str(compacted_iri),
            }
        fields[record['field_name']] = field

    output['$graph'][0]['fields'] = fields
    
    print(yaml.dump(output, sort_keys=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--name')
    parser.add_argument('--context')
    args = parser.parse_args()

    main(args)
