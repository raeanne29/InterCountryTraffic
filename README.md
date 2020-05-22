# InterCountryTraffic

The user should have 4 codes that MUST be in the same directory as the measurements file named menog-internet-study-master.

The user needs to install the following modules before running any code:
-pyasn
-plotly
-numpy
-matplotlib
-prettytable

The user needs to have the "asnames.json" and "IPASN.DAT" files in the same directory as the codes.

The user needs to run the "measurements_decoding" file.
This file generates a binary file that contains the measurements.
Once the binary file generated, the user won't need to run the "measurements_decoding" file again.

The three other python files are for the plotting the results.
"chartResults" returns a chart containing the non-menog countries with their occurrences in the traceroutes.
"tableResults" returns a table containing the non-menog asn with their occurrences in the traceroutes.
"sankeyResults" returns a diagram showing the flow of the traceroutes.
For the "sankeyResults" file, the user must provide an argument on his command line:
For an outgoing flow from a specific country, the user must provide the menog country code of two capital letters.
(The country codes are in the measurements files).
For all traceroutes flow, the user must pass the argument "ALL".
