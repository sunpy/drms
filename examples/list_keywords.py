"""
==================================
List all keywords for a HMI series
==================================

This example shows how to display the keywords for a HMI series.
"""

import drms

###############################################################################
# First we will create a `drms.Client`, using the JSOC baseurl.

client = drms.Client()

###############################################################################
# Query series info

series_info = client.info("hmi.v_45s")

###############################################################################
# Print keyword info

print(f"Listing keywords for {series_info.name}:\n")
for keyword in sorted(series_info.keywords.index):
    keyword_info = series_info.keywords.loc[keyword]
    print(keyword)
    print(f"  type ....... {keyword_info.type} ")
    print(f"  recscope ... {keyword_info.recscope} ")
    print(f"  defval ..... {keyword_info.defval} ")
    print(f"  units ...... {keyword_info.units} ")
    print(f"  note ....... {keyword_info.note} ")
