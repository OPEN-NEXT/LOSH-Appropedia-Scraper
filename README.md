<!--
SPDX-FileCopyrightText: 2021 Robin Vobruba <hoijui.quaero@gmail.com>

SPDX-License-Identifier: CC0-1.0
-->

[![DOI](
    https://zenodo.org/badge/360458831.svg)](
    https://zenodo.org/badge/latestdoi/360458831)
[![GitHub license](
    https://img.shields.io/github/license/OPEN-NEXT/LOSH-Appropedia-Scraper.svg?style=flat)](
    ./LICENSE.txt)
[![REUSE status](
    https://api.reuse.software/badge/github.com/OPEN-NEXT/LOSH-Appropedia-Scraper)](
    https://api.reuse.software/info/github.com/OPEN-NEXT/LOSH-Appropedia-Scraper)

# LOSH Appropedia scraper

This contains code (BASH and AWK) that fetches the list of project names
hosted on appropedia.org, and makes them available as:

* [`appro_proj_names.csv`](https://open-next.github.io/LOSH-Appropedia-Scraper/appro_proj_names.csv)
  \- the list of project names
* [`appro_yaml_urls.csv`](https://open-next.github.io/LOSH-Appropedia-Scraper/appro_yaml_urls.csv)
  \- the table containin the OKH v1 file URLs

(Both are re-generated weekly at 03:02 each Monday, UTC)

The later uses the same format as [`projects_okhs.csv`](
https://github.com/OpenKnowHow/okh-search/blob/master/projects_okhs.csv)
\- the official OKH v1 "database" of known, supporting projects.

That later file - [`appro_yaml_urls.csv`](
https://open-next.github.io/LOSH-Appropedia-Scraper/appro_yaml_urls.csv) -
can be used to fetch all the okh.yml files of appropedia.org
and convert them to our newer format, using the [conversion tool](
https://github.com/OPEN-NEXT/LOSH-OKH-Conversion).

The new version of OKH (LOSH-v1) is currently being developed at
[LOSH](https://github.com/OPEN-NEXT/LOSH/).

## Use

run the script:

```bash
./appro-fetcher
```

If all goes well, you will find the generated lists at `target/*.csv`.
