[International Trade](/profile/trade/)
# Harmonized System (HS)

<!-- Initial work by Wenjie (and Chen) -->

TO DO:

Using Tabulator, relate Harmonized System (HS) .csv to NAICS and other international categories

[Upcoming list of industries by location](/localsite/info/#state=CA)
[Upcoming list of industries by location](/localsite/info/#state=CA&beta=true) - React drops state

Sample use of [Product HS Codes for Georgia Exporter Directory](https://model.georgia.org/display/exporters/)

TO DO: Insert and pull HS tables from Exiobase supabase  
[Javascript form to pull from Supabase SQL](../prep/sql/supabase/)  

[Satwik's Exiobase data output](https://model.earth/global-trade/plotly)

## Concordance

We're using the files they maintain as our source.  
The Concordance R-library is a leading process for relating:
Harmonized System (HS), ISIC/SITC and NAICS


**While R-Language was ultimately not used in our HS pull, you might find this useful**
[How to use R-Language libraries in a Python CoLab (2nd example)](https://www.geeksforgeeks.org/how-to-use-r-with-google-colaboratory/)
[Our CoLab](https://colab.research.google.com/drive/1etpn1no8JgeUxwLr_5dBFEbt8sq5wd4v?usp=sharing) for interacting with R from Python - not used here, but you could expand on this.
We ended up NOT using the Concordance R package directly.
<!--
[Chinese sectors](https://chatgpt.com/share/dbb6de4b-1366-4190-b284-3b7165951c61),  ISIC,  and the Harmonized System (HS)
-->

Instead we used raw files in the [Concordance GitHub Repo](https://github.com/insongkim/concordance/tree/master/data-raw) as our source for CSV lookup files.

## CSV Lookup Files

Columns for a table named 

**Naics**
Naics (6 digits) - Unique Key
NaicsDescription
HarmonizedID (4 digits HS) - not unique
HarmonizedDescription
InternationalID (4 digits ISID) - not unique
InternationalDescription

Naics, NaicsDescription, InternationalID, InternationalDescription
https://github.com/insongkim/concordance/blob/master/data-raw/2017_NAICS_to_ISIC_4.xlsx

Find a way to relate HS to unique NAICS
https://github.com/insongkim/concordance/tree/master/data-raw

**HarmonizedNAICS**
HS (4-digit)
HS-Description
NAICS (4-digits multiple)
NAICS-Description

**HarmonizedISIC**
HS (4-digit)
HS-Description
ISIC-Code (2-digits multiple)
ISIC-Description 

<!--
HS (4-digit)
HS-Description
Chinese-Sector-Code (2-digits)
Chinese-Sector-Description
-->
