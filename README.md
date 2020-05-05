# Table->SALAD

Convert a `.csv` table to a [SALAD](https://github.com/common-workflow-language/schema_salad) schema

## Schema Generation

### Input

A `.csv` file with the field headers: `field_name`, `doc`, `type`, `iri`

Eg:

|field_name       | doc                                         | type   | iri                                        |
|-----------------|---------------------------------------------|--------|--------------------------------------------|
| sample_name     | The user-defined name for the sample.       | string | http://edamontology.org/data_3273          |
| collection_date | The date on which the sample was collected. | string | http://purl.obolibrary.org/obo/NCIT_C81286 |

(Note that SALAD has a limited set of [primitive types](https://www.commonwl.org/v1.0/SchemaSalad.html#PrimitiveType) available to choose from.)

A `context.json` file with prefixes for any IRIs used in your table:

```json
{
  "edam_data": "http://edamontology.org/data_",
  "ncit": "http://purl.obolibrary.org/obo/NCIT_"
}
```

(optionally) a name for your schema class (defaults to `SchemaClass` if not provided.

### Usage

```
table_salad_schema_gen.py --input schema_table.csv --context context.json --name SampleSchema
```

```yaml
$namespaces:
  ncit: http://purl.obolibrary.org/obo/NCIT_
  edam_data: http://edamontology.org/data_

$graph:
- fields:
    collection_date:
      doc: The date on which the sample was collected.
      jsonldPredicate:
        _id: ncit:C81286
      type: date
    sample_name:
      doc: The user-defined name for the sample.
      jsonldPredicate:
        _id: edam_data:3273
      type: string
  type: record
  name: SampleSchema
  documentRoot: 'true'
```

## Data Validation

### Input

### Usage

```
table_salad_validate.py
```