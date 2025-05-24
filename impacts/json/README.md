[Trade Flow](/profile/trade/)
# Trade File Pipeline - to json and parquet

Colab that creates tables in pandas and sends tables to Supabase.  
The last colab sends to Github from Supabase.

First we move data from the Exiobase API into Supabase...

[Fetch tables](https://colab.research.google.com/drive/1Zg9gq4WnEknW6hHGA3aP2BBlneGCqRx5?usp=sharing) - Table names: Import, ImportContributions, Commodity, Industry
<!--
[ImportContributions table](https://colab.research.google.com/drive/1Ms-gDn4U7XdmCRs7zBpmmpSMuoaB-zgU)

[Commodity table](https://colab.research.google.com/drive/1Fxyfh23CXipo7O8f01XayG6BF6Kr7-In)

[Industry table](https://colab.research.google.com/drive/1ZoG9VTm9CR3X2xh_4xfv2QTUMfdE-uN0)
-->

Then we send to GitHub...

[Supabase tables to Github](https://colab.research.google.com/drive/18xCRO35WvLAZR1eDvMpgSw4asMDMQqF3#scrollTo=adFIMfPWNH2D) - Sends tables above from Supabase to impacts folder in json and parquet format.

TO DO:  
[JSON Output](https://github.com/ModelEarth/profile/tree/main/impacts/json) - For [javascript form frontend](../).


Developed by [Gary](https://dreamstudio.com/earth/)