#!/usr/bin/env python

import argparse
import csv
import ruamel.yaml
import schema_salad.schema
from schema_salad.sourceline import add_lc_filename
from pyshex.evaluate import evaluate

def parse_metadata(path_to_metadata):
    metadata = []
    with open(path_to_metadata) as csvfile:
        reader = csv.DictReader(csvfile)
    return []


def main(args):

    (document_loader,
     avsc_names,
     schema_metadata,
     metaschema_loader) = schema_salad.schema.load_schema(args.schema)

    with open(args.metadata) as f:
        metadata_contents = ruamel.yaml.round_trip_load(f)

    for metadata_content in metadata_contents:
        metadata_content["id"] = "http://example.org/id"
        add_lc_filename(metadata_content, metadata_content["id"])
        doc, metadata = schema_salad.schema.load_and_validate(document_loader, avsc_names, metadata_content, True)

    with open(args.shex) as f:
        shex = f.read()

    g = schema_salad.jsonld_context.makerdf("workflow", doc, document_loader.ctx)
    validation_result, reason = evaluate(g, shex, doc["id"], "sample_name")

    if not validation_result:
        print(reason)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--schema')
    parser.add_argument('--shex')
    parser.add_argument('--metadata')
    args = parser.parse_args()
    main(args)
