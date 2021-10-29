#!/usr/bin/env awk

# SPDX-FileCopyrightText: 2021 Robin Vobruba <hoijui.quaero@gmail.com>
#
# SPDX-License-Identifier: Unlicense

# Parses the HTML of https://www.appropedia.org/Special:Export
# as of 28. October 2021.
# If you enter "Projects" in the "Add pages from category:" field,
# and then click the `[Add]` button,
# you get the list of projects in the field below.
# This script extracts that list from that whole sites HTML.
# The same site ca be automatically fetched with `curl`,
# see script `appro-fetcher`.

BEGIN {
	found_id=0
	in_list=0
	done=0
}

/id='ooui-php-2'/ {
	if (!found_id) {
		sub(/.*id='ooui-php-2'/, "", $0)
		found_id = 1
	}
}

/>/ {
	if (found_id && !in_list && !done) {
		sub(/.*>/, "", $0)
		in_list = 1
	}
}

/</ {
	if (in_list) {
		sub(/.*>/, "", $0)
		in_list = 0
		done = 1
	}
}

{
	if (in_list) {
		print($0)
	}
}

