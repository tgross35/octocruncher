# Octocruncher V3

Use this to query Octopart using the v3 API

To function with active requests, the OCTOPART_API_KEY environment variable must
be set. This can be done in your Python using the following:

```python
import os
os.environ['OCTOPART_API_KEY'] = 'xxxxxxxxx'
```

## Usage
```python
from octocruncher import OctoCruncher

# Setup the manufacturer part number here
x = OctoCruncher(mpn='mpn')
```

OctoCruncher takes in the argument 'mpn' (manufacturer part number) which
everything else is based off of. Other optional arguments:

json_source: You can provide a json.load[s]() object instead of querying online.
This is helpful for when you want to cache (use with OctoCruncher.getJSON())

file_source: Similar to json_source but will load from the given file path

## Callables

### .getNumItems():
This tells you how many results there are

### .setItemNumber(itemnumber=0)
This sets the working item for all other functions

### .getMPN():
Returns working manufacturer part number

### .getJSON():
This will return a json object that can be cached and loaded later

### .getNumDescriptions():
Tells you how many available part descriptions there are

### .getDescription(n=0):
Returns the nth description. If n is not specified, the 0th
description will be returned. Returntype is a description class which has the
`value` and `source` elements

### .getNumDatasheets():
Tells you how many datasheets are available

### .getDatasheet(n=0)
Returns the nth Datasheet object. This object has the
following parameters that can be accessed:
```
date_created
last_updated
num_pages
size_bytes
date_created
mimetype
url
source
```

### .getManufacturer():
This returns a manufacturer object with the `name` and `homepage_url` attributes
