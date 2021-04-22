# LOSH Appropedia scraper

This contains a python script that fetches the list of projects from [Appropedia.org](https://www.appropedia.org/),
downlaods their WikiMedia source files,
and parses their `Infobox` content into a python dictionary.
It then maps this dictionary to [Open Know-How](https://openknowhow.org/) 2.0 keys,
and generates an OKH meta-data file.

OKH v2 is currently being developed at [LOSH](https://github.com/OPEN-NEXT/LOSH/).

## Use

Install requirements:

* Python 3
* `pip install -r requirements.txt`

run the script:

```bash
./scraper.py
```

If all goes well, you will find the generated OKH files at
`tmp/okh-*.toml`.
