---
title: "Handling Parquet Schema Mismatch Based on Data"
date: 2021-01-24T05:38:50Z
tags: ["esoteric bug", "python"]
---

{{<toc>}}

TL;DR: explicitly define your parquet schema when reading/writing from pq tables if you want to maintain consistent datatypes even when column values are null.

## The Problem

Consider the following pandas dataframe, written into parquet format:

```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

df = pd.DataFrame(
  {
    'organizationId' : ['org1', 'org2', 'org3'],
    'customerProducts' : [['p1', 'p2'], ['p4', 'p5'], ['p1', 'p3']]
  }
)

table = pa.Table.from_pandas(df)
pq.write_table(table, 'output.parquet')
```

Here, we have a dataframe with two columns - with the `customerProducts` col storing a list of strings as data.

Let's use pyarrow to read this file and display the schema.

```python
import pyarrow.parquet as pq

pfile = pq.read_table('output.parquet')
pfile.schema
```

The output is this:

```text
organizationId: string
customerProducts: list<item: string>
  child 0, item: string
```

So far, so good. Ok, now let's try this again but now, for this particular dataframe, in every row `customerProducts` will be empty.

```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

df = pd.DataFrame(
  {
    'organizationId' : ['org1', 'org2', 'org3'],
    'customerProducts' : [[], [], []]
  }
)

table = pa.Table.from_pandas(df)
pq.write_table(table, 'output_nulls.parquet')
```

What happens though - when we try to read the schema of _this_ pq file?

```python
import pyarrow.parquet as pq

pfile = pq.read_table('output_nulls.parquet')
pfile.schema
```

The output is this:

```text
organizationId: string
customerProducts: list<item: null>
  child 0, item: null
```

**null**!! 

## Analysis and Remarks

So firstly - let's consider the _why_ here: why does this happen? If we look only at `output_nulls.parquet`, the behavior actually makes a lot of sense. `customerProducts` has no data - it is a list of empty lists. Parquet has no way to tell that it actually _ought_ to be a list of strings.

Furthermore, if we were to analyze these files using `parquet-tools`, the results look even more funky:

**output.parquet**

```bash
$ root@5ecebf0a7dc8:/# parquet-tools inspect output.parquet
# ... Ignoring non relevant columns 
############ Column(item) ############
name: item
path: customerProducts.list.item
max_definition_level: 3
max_repetition_level: 1
physical_type: BYTE_ARRAY
logical_type: String
converted_type (legacy): UTF8
# ... Ignoring non relevant columns 
```

**output_nulls.parquet**

```bash
$ root@5ecebf0a7dc8:/# parquet-tools inspect output_nulls.parquet
# ... Ignoring non relevant columns 
############ Column(item) ############
name: item
path: customerProducts.list.item
max_definition_level: 3
max_repetition_level: 1
physical_type: INT32
logical_type: Null
converted_type (legacy): NONE
# ... Ignoring non relevant columns 

```

Nulls are interpreted and stored as `INT32` in parquet - this is especially problematic if you are using pq files along with Hive and/or Presto, kinda like so:

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS my_ext_table(
	organizationId string,
	customerProducts array<string>
) PARTITIONED BY(
    year string,
    month string,
    day string)
STORED AS PARQUET
LOCATION 's3://my_s3_bucket/';
```

In these cases, within `my_s3_bucket`, partitioned by `year`, `month` and `day` there may be 1 or more parquet files. Some of these files _may_ have **no** `customerProducts` set, meaning that the schema is interpreted as:

```bash
# ... Ignoring non relevant columns 
############ Column(item) ############
name: item
path: customerProducts.list.item
max_definition_level: 3
max_repetition_level: 1
physical_type: INT32
logical_type: Null
converted_type (legacy): NONE
# ... Ignoring non relevant columns 

```

which has a `physical_type` of `INT32`. Hive/prestodb absolutely does NOT like seeing `array<int>` when it is expecting corresponding column `customerProducts` to be of type `array<string>`. In these cases, your query will fail and everything will suck.

So - this behavior we see when creating parquet files from pandas is odd because while the conversion code (from pd => pq) is actually fine, we may want to read batches of these files downstream using technologies that require exact datatype definitions declared upfront.

The best way I can think of to solve this problem is to manage and maintain a parquet schema somewhere and when _creating_ these pq files explicitly provide the schema as well.


```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

df = pd.DataFrame(
  {
    'organizationId' : ['org1', 'org2', 'org3'],
    'customerProducts' : [[], [], []]
  }
)

fields = [
    pa.field('organizationId', pa.string()),
    # explicitly define `customerProducts` as list of strings
    pa.field('customerProducts', pa.list_(pa.string())),
]

# explicitly define schema before writing table
table = pa.Table.from_pandas(df, schema=pa.schema(fields))
pq.write_table(table, 'output_nulls.parquet')

table.schema
```

Output of schema:

```text
pyarrow.Table
organizationId: string
customerProducts: list<item: string>
  child 0, item: string
```
