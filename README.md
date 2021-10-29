<!--
SPDX-FileCopyrightText: 2021 Robin Vobruba <hoijui.quaero@gmail.com>

SPDX-License-Identifier: CC0-1.0
-->

[![DOI](
    https://zenodo.org/badge/360458831.svg)](
    https://zenodo.org/badge/latestdoi/360458831)
[![GitHub license](
    https://img.shields.io/github/license/OPEN-NEXT/LOSH-Appropedia-Scraper.svg?style=flat)](
    ./LICENSE)
[![REUSE status](
    https://api.reuse.software/badge/github.com/OPEN-NEXT/LOSH-Appropedia-Scraper)](
    https://api.reuse.software/info/github.com/OPEN-NEXT/LOSH-Appropedia-Scraper)

# LOSH Appropedia scraper

This contains code (BASH and AWK) that fetches the [list of project names](https://open-next.github.io/LOSH-Appropedia-Scraper/appro_proj_names.csv)
hosted on appropedia.org, and makes them available as a 1 column CSV file,
and uses them to create a [list of OKH v1 file URLs](https://open-next.github.io/LOSH-Appropedia-Scraper/appro_yaml_urls.csv) for all the projects.


in the same format as [projects_okhs.csv](
https://github.com/OpenKnowHow/okh-search/blob/master/projects_okhs.csv),
the official OKH v1 "database" of known, supporting projects.

That later list - [OKH v1 file URLs](
https://open-next.github.io/LOSH-Appropedia-Scraper/appro_yaml_urls.csv) -
can be used to fetch all the okh.yml files of appropedia,
and convert them to our newer format with the [conversion tool](
https://github.com/OPEN-NEXT/LOSH-OKH-Conversion).
It can also be scraped with that tool,
just like [projects_okhs.csv](
https://github.com/OpenKnowHow/okh-search/blob/master/projects_okhs.csv) -
which is the official OKH v1 "database" of known, supporting projects -
as these two CSV files use the same format.

OKH v2 is currently being developed at [LOSH](https://github.com/OPEN-NEXT/LOSH/).

## Use

run the script:

```bash
./appro-fetcher
```

If all goes well, you will find the generated lists at `target/*.csv`.
