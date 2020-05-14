**MHCLG Rough sleeping**

https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness

The footnotes from one of the sheets needs to be added to the description or metadata

End table structure
Period, ONS Geography Code, Sex, Nationality, Age, Measure Type, Marker, Value, Percentage of Total, Yearly Percentage Change, Projected Number of Households, Rough Sleeping Rate, Measure Type, Unit, Value

&nbsp;

**Sheet: table 1**

(A) ONS Code - change name to ONS Geography code

(B) Local Authority - Not needed as we have ONS Code

(C) Higher level Local Authority - Not needed as we have ONS Code

(D4:L4) Year - change name to Period and format as year/2015

(M) Number of Households mid-2018 (‘000) - change to 
	Projected Number of Households - and add footnote 2 to description
	
(N) 2018 rough sleeping rate (per 10,000 household) - change to:

		Rough Sleeping Rate per 10,000 households
		Or
		Rough Sleeping Rate - and add note to description explaining that the rate per 10,000 households (this is not a percentage)
	
(B) % change from previous year - move to a column as an attribute and rename 

	 	Percentage Change - This is only for the higher level stats

(B) % of England total - move to a column as an attribute and rename

		Percentage of Total - This is only for the higher level stats
	
Add a Sex column with the value All

Add a Nationality column with the value All

Add Measure Type column with value People

Add Unit column with value Count

Add Age column with value Total

&nbsp;

**Sheet: table 2a**

(A) ONS Code - change name to ONS Geography code

(B) Local Authority - Not needed as we have ONS Code

(C) Higher level Local Authority - Not needed as we have ONS Code

(D4:O4) Year - change name to Period and format as year/2015

(D5:O5) Sex - (T | M | F | U)

(B) % of total - move to a column as an attribute and rename

		Percentage of Total - This is only for the higher level stats
		
Add a Nationality column with the value All

Add Measure Type column with value People

Add Unit column with value Count

Add Age column with value All

&nbsp;

**Sheet: table 2b**

(A) ONS Code - change name to ONS Geography code

(B) Local Authority - Not needed as we have ONS Code

(C) Higher level Local Authority - Not needed as we have ONS Code

(D4:R4) Year - change name to Period and format as year/2015

(D5:R5) Nationality - (Total | UK | EU non-UK | Non-EU | Unknown)

(Q31) 2018 Method - put in Marker column but only for 2018 figures.

		Notes in metadata will explain values

(B) % of total - move to a column as an attribute and rename

		Percentage of Total - This is only for the higher level stats
		
Add a Sex column with the value All

Add Measure Type column with value People

Add Unit column with value Count

Add Age column with value All


&nbsp;

**Sheet: table 2c**

(A) ONS Code - change name to ONS Geography code

(B) Local Authority - Not needed as we have ONS Code

(C) Higher level Local Authority - Not needed as we have ONS Code

(D4:Q4) Year - change name to Period and format as year/2015

(D5:Q5) Age - (Total | Under 25 | Under 18 | 18 to 25 | 26 + | Unknown)

(B) % of total - move to a column as an attribute and rename

		Percentage of Total - This is only for the higher level stats
	
Add a Sex column with the value All

Add Measure Type column with value People

Add Unit column with value Count

Add Nationality column with value All


All data should be joined together in 1 dataset with the name

**MHCLG Rough Sleeping in England**







