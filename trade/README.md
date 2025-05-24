[Active Projects](../../projects/)
# Trade Flow

[SuiteCRM](../crm) - Partner Data analysis using Azure, SQL Express and MariaDB.
[Trade Impact Colabs](../impacts/json) - Deploys Exiobase international data to GitHub as JSON
[Global Trade - our Comtrade and Exobase API data pulls](../../global-trade)
[Try MARIO Input-Output library](https://mario-suite.readthedocs.io/en/latest/intro.html) as a striped-down [Pymyrio](https://pymrio.readthedocs.io/en/latest/intro.html)

<b>Exiobase International Trade Data</b>
Our IO Team has been generating [JSON](../impacts/json/), <a href="/profile/prep/sql/duckdb/">DuckDB Parquet</a> and <a href="/profile/prep/sql/supabase/">Supabase database inserts</a> for comparing industries and identifying imports with positive environmental impacts using [a Javascript frontend](../impacts/).


We've also output [DuckDB parquet files from USEEIO](https://github.com/ModelEarth/profile/tree/main/impacts/useeio) - dev by Satyabrat<!-- When readme added: [DuckDB parquet files from USEEIO](../impacts/useeio) -->
DuckDB supports SQL JOINs in any browser via [WebAssembly WASM](https://duckdb.org/docs/api/wasm/overview.html)

There are examples of using [Apache Parquet](../impacts/useeio/parquet/) files from static html files using DuckDB-Wasm and JavaScript

We're imitating the data pull into .csv from Exiobase in [generate\_import\_factors.py](https://github.com/ModelEarth/USEEIO/tree/master/import_factors_exio) but we're pushing directly to json, DuckDB .parquet and Supabase.  

<!--
We're also using [Mario](https://mario-suite.readthedocs.io/en/latest/intro.html), a friendly version of Pymrio. (Mario may lack some of the functionality and/or data Pymrio provides.)
-->

Each database instance (for a country-year) will contain these tables:

**GOAL: Output these SQL Tables for a country and year (2020)**
Factor (includes FactorID and FlowUUID)
Industry (5-char sector)
IndustryFactor
Commodity (6-char product)
CommodityFactor
ImportIndustryFactor
ImportCommodityFactor
ImportContributions
ImportMultiplierFactor

The Industry is 5-char and the Commodity is 6-char.

**Contribute to these CoLabs:**   
<!-- these 2 also reside on DuckDB page -->
[NEW - Parquet To Github](https://colab.research.google.com/drive/1Pqpdebj4rY06E6NAgqJskgt-G4HBHPUZ?usp=sharing)
[NEW - Colab to Github](https://colab.research.google.com/drive/1mnZKBypCBlVLXiCuSpGj0JZf4NZzNR7h?usp=sharing)
[Exiobase To Github Pipeline](https://colab.research.google.com/drive/1N47_pfTUyOzeukgf4KYX1pmN_Oj1N3r_?usp=sharing) - Pulls zip of year from Exiobase and unzips 
[Create Database from Panda Dataframe](https://colab.research.google.com/drive/1IMpOYzT6oXbZXaJKugi5vCmUB_tIHo0J?usp=sharing) - Output SQL 
[Pymrio Exiobase Industry](https://colab.research.google.com/drive/1bXUO1iXyBGbmZODmnl0NVn3yFpWwBCOi?usp=sharing) - Sends to Supabase
[Inserting Factors and Sectors into Supabase](https://colab.research.google.com/drive/1INHz02V-cU_y_nAlS-BWxQQtz8Qg_lLi#scrollTo=KUnI-Va8M1Nl) - Invite only
[Satwick's PYMRIO.ipynb CoLab](https://colab.research.google.com/drive/1AZPfBlG0iUKmKRZjlNxn8uOuvtAfEarn?usp=sharing)  

TO DO: Send about 8 countries to unique datasets for the year 2020.
TO DO: Send to DuckDB instances for a country and year - See DuckDB example in our [zip code processing](https://model.earth/community-zipcodes/) 


TO DO: Experiment in our [Pymiro CoLab](https://colab.research.google.com/drive/1Q9_1AhdY8uPUfLVUN71X6mKbEy_kqPuQ?usp=sharing) using the [Pymiro for Exiobase library](https://pymrio.readthedocs.io/en/latest/). Save DuckDB country-year data instances. Jaya and Satwick are investigating using .feather within the Pymiro CoLab.

TO DO: Try the following frontend [javascript with a .feather file](feather).

The [Big Sankey](https://github.com/baptiste-an/Application-mapping-GHG) ([view chart](https://sankey.theshiftproject.org/)) uses Plotly with .feather files. We could do the same with [Anvil](https://anvil.works) and Google Looker. 

[ExiobaseSupabase CoLab](https://colab.research.google.com/drive/1LsEDmXrAAGs40OiAKWH48K63E_2bMGBb?usp=sharing)<!-- Himanshu, Sahil, Ben, Parth, Jack, Satwik, Indrasenareddy--> and [New version by Gary](https://colab.research.google.com/drive/16a2pykb_ycfHhAhxK949giWuVf3c_IeD)

TO DO: Update the ExiobaseSupabase CoLab above to also pull the BEA data to match the <a href="https://github.com/ModelEarth/USEEIO/tree/master/import_factors_exio">generate\_import\_factors.py</a>. Test with the US.   <!-- Yuhao, Ruolin, Nancy-->

## Trade Flow/Impact Visualizations

See chart starter sample in upper right.

<!--
In the CoLab, add the [Sector table output](https://github.com/ModelEarth/USEEIO/commit/c10d087d916477b3335127de560d4689fa5818ea) Ben created.
-->

TO DO: Create [interactive versions](/profile/impacts/) of the [three Exiobase charts](https://exiobase.eu)  
See our [SQL Project Overview](/profile/prep/) - Three Charts using International Exiobase Data


TO DO: <a href="/profile/prep/">Create International Industry Reports</a> - like Energy Consumption in Drying

TO DO: Generate SQL for [US States from Matrix table files](/io/about/) with new [50 State USEEIO json](https://github.com/ModelEarth/profile/tree/main/impacts/2020)


<!--<a href="#reports">Our Javascript USEEIO TO DOs</a>-->
<!--<a href="/io/charts/">Our React USEEIO widget TO DOs</a>-->

<b>Pulling data into state SQL databases</b>
New simple table names - for use by elementary school students
<a href="/profile/prep/sql/supabase/">Supabase from .csv files</a>
<a href="/profile/prep/sql/duckdb/">DuckDB from .csv files</a>
<a href="/requests/products/">Harmonized System (HS) codes</a> - <a href="https://colab.research.google.com/drive/1etpn1no8JgeUxwLr_5dBFEbt8sq5wd4v?usp=sharing">Our HS CoLab</a>

<b>View SQL Data</b>
[Javascript with Supabase](/profile/impacts) and [Just Tables](/profile/prep/sql/supabase/SupabaseWebpage.html)
Our DuckDB parquet tables in [ObservableHQ Dashboard](https://observablehq.com/d/2898d01446cefef1) and [Static Framework](/data-commons/dist/innovation/)
<a href="/profile/impacts/">Sample of JavaScript joining DuckDB Parquet tables</a>
<a href="https://model.earth/storm/impact/process.html">SQL Documentation Sample - Storm Tweet Data</a>

<b>Python to pull CSV files into SQL</b>
<a href="https://colab.research.google.com/drive/1qWgO_UjeoYYB3ZSzT3QdXSfVZb7j09_S?usp=sharing">Generate Supabase Exiobase (Colab)</a> - <a href="https://github.com/ModelEarth/profile/tree/main/impacts/exiobase/US-source">Bkup</a>
<a href="https://colab.research.google.com/drive/1Wm9Bvi9pC66xNtxKHfaJEeIYuXKpb1TA?usp=sharing">Generate DuckDB Exiobase (CoLab) - <a href="https://github.com/ModelEarth/profile/tree/main/impacts/exiobase/US-source">Bkup</a>
<br>

# US EPA Trade Data Pipeline

The US EPA also merges in US Bureau of Economic Analysis (BEA) with Exiobase. We'd like to get close to this process for all the countries using just Exiobase (and possibly Google Data Commons).

For the US EPA analysis, their repo generates six [US-2020-17schema CSV files](https://github.com/ModelEarth/profile/tree/main/impacts/exiobase/US-source/2022) by running <a href="https://github.com/ModelEarth/USEEIO/tree/master/import_factors_exio">generate\_import\_factors.py</a>. The merge combines US BEA and <a href="https://exiobase.eu">EXIOBASE</a> data emissions factors for annual trade data. (The ExiobaseSupabase CoLab above aims to send the same Exiobase data directly to Supabase and DuckDB for each country and year.)

Exiobase provides the equivalent to <a href="https://github.com/USEPA/useeior/blob/master/format_specs/Model.md">M, N, and x</a> which is used in the <a href="/io/about/">USEEIO models</a> for import emissions factors. Exiobase also provides gross trade data which has no equivalent in USEEIO.



**Data Prep Notes**
- We remove underscores and use CamelCase for column names.
- We exclude the Year columns because each database is a different year.
- Commodity refers to the 6-character detail sectors.
- Sector refers to the 5-character and fewer sectors.
- Region is referred to as Import.
- National is omitted from the table names.
- Country abbreviations (Example: US) are appended to country-specific tables.
This structure supports pulling all the country data into one database.