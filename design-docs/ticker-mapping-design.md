# Ticker Mapping Design Doc
## Rationale
The goal of this portion of the project is to create mapping functionality that is abstracted enough to apply to any situation that needs to map company names to tickers, should we decide to move away from the drug approval data or need to map some other datasource to ticker information. Additionally, if sufficiently abstract, this code can be made into a publicly available library and used for future project implementations.

## Implementation
I think this should be built with a couple different classes to both: make it easier to replace functionality, and to allow us to work on it asynchronously without having to worry about conflicting changes to the code or merge conflicts.  
The high level functionality should work as follows: the main mapping class should be able to be instantiated with no parameters (although it might end up being better to instantiate the main class with instances of the worker classes to make it easier to swap out functionality). It should have a master function, say a function called <b>map()</b>. <b>map()</b> should accept 2 arguments, <b>String company_name</b> and <b>DateTime from_date</b>, where <b>company_name</b> is the name of the company to map to the ticker, and <b>from_date</b> is the date to look for subsidiary-parent company relationships at. The function should return 2 values, <b>String ticker</b> and <b>DateTime to_date</b> where <b>ticker</b> is the ticker of the most closely related publicly traded company on the NYSE, and <b>to_date</b> is the most recent date the ticker can be mapped to the company in question.  
Though the <b>to_date</b> value will add difficulty to the calculation, it is useful to track for the purpose of subsidiary mapping. For instance, if we get a drug approval for a subsidiary but our mapping shows the parent (publicly traded company) no longer owns this subsidiary less than one month after the approval, we probably want to reconsider buying stake in the parent, at least with the rationale that the stock will go up related to the approved drug.  
Since we want the main class to be compositional in nature, I think the work should be delegated to separate classes loosely following the below structure:
### Classes (names pending)
<b>main</b>  
<b>public functionality:</b>  
<b>map(</b>String company_name, DateTime from_date<b>):</b>  
Map a company to its ticker on the NYSE, or the ticker of its parent if it is a subsidiary.  
Returns:  
String <b>ticker</b>: the ticker of the relevant publicly traded company  
DateTime <b>to_date</b>: datetime representing the last known time the company -> ticker relationship is valid (so if the company to be mapped is not a subsidiary, to_date should be the current date or some other flag)  
  
<b>map_df(</b>DataFrame data, String name_column, String date_column<b>):</b>  
Given a dataframe and 2 strings pointing to the columns in the df containing company names and dates respectively, add 2 new columns (or 1 column of tuples) containing the mapped ticker and to_date values for each entry in the dataframe. Basically just a compositional function relying heavily on above <b>map</b>.  
Returns:  
DataFrame <b>mapped_df</b>: the passed DataFrame with ticker and to_date columns added to it.
<br /><br /><br />

<b>subsidiary_mapping</b>  
<b>public functionality:</b>  
<b>find_parent(</b>String company_name, DateTime from_date<b>):</b>  
Given the company name (which we assume is a subsidiary, since this classes' functionality should not be hit unless a ticker cannot be found directly from the company name) and the date to look starting from, try to find a parent company name (most likely using Pitchbook M&A data) and the most recent date the subsidiary was owned by said company.  
Returns:  
String <b>parent_name</b>: the full name of the relevant publicly traded parent company  
DateTime <b>to_date</b>: datetime representing the last known time the parent company owned the subsidiary  
  
<b>find_next_parent(</b>String company_name, DateTime from_date<b>):</b>  
Same functionality as <b>find_parent</b> but finds the next parent of the subsidiary, IE the next company to own the subsidiary assuming it moves ownership soon after <b>from_date</b>. This function is probably not needed to implement right away, but may be helpful in the future depending on the strategy we decide on, and should be relatively similar to <b>find_parent</b>.  
Returns:  
String <b>parent_name</b>: the full name of the relevant publicly traded parent company  
DateTime <b>to_date</b>: datetime representing the last known time the parent company owned the subsidiary
<br /><br /><br />

<b>ticker_finding</b>  
<b>public functionality:</b>  
<b>find_ticker(</b>String company_name<b>):</b>  
Given a company name, attempt to find a ticker for the company on the NYSE (probably using Pitchbook). This is intended to be used in tandem with the <b>subsidiary_mapping</b> functionality so the passed name does not have to be a known parent company (IE we'd like to use this function, if it can't find a ticker we assume the company is a subsidiary and use the <b>subsidiary_mapping</b> functionality, then back to this once we find a new company name to try, which will be handled by the compositional <b>main</b> class).  
Returns:  
String <b>ticker</b> OR False: The ticker of the publicly traded company, or False if no ticker could be mapped, in which case we assume the company is a subsidiary.
<br /><br /><br />

<b>name_cleaning</b>  
<b>public functionality:</b>  
<b>standardize_name(</b> String company_name<b>):</b>  
To avoid having to do slant or partial matching on company names, we'd like to be able to standardize the names to the format they'll be in Pitchbok, so this function should accept a company_name and apply the necessary transformations (if any) to allow 1:1 matching to Pitchbook company names.  
Returns:  
String <b>standardized_name</b>: The standardized version of the passed company name.
<br /><br /><br />

<b>storage_mode</b>  
<b>public functionality:</b>  
We will likely use an AWS database or some other similar DB to host the data we will be using, so this class will contain the functionality to read and write from the desired source. TO BE IMPLEMENTED at a later date.
<br /><br /><br />




