**Northern Ireland housing bulletin**

https://www.communities-ni.gov.uk/topics/housing-statistics#toc-2

**Flowchart**

https://gss-cogs.github.io/family-homelessness/datasets/specflowcharts.html?NIHE-Northern-Ireland-housing-bulletin/flowchart.ttl

**End table structure:**

Period, Building Stage, Development Type, Housing Type, Measure Type, Unit, Value

*Notes at bottom of each sheet needs to be added to description/comment/metadat*a

**Sheet: T1_1 Building Control New Dwelling Starts by development type**

(A5:A52) Period - combination of year and quarters

(B3:D4) Development Type (Total New Dwelling Starts >- Total)

Add Building Stage column with value Starts

Add Measure Type column with value Houses

Add Housing Type column with value All

Add Unit column with value Count

&nbsp;

**Sheet: T1_2 Building Control New Dwelling Completions by development type**
 
(A5:A52) Period - combination of year and quarters

(B3:D4) Development Type (Total New Dwelling Completions -> Total)

Add Building Stage column with value Completions

Add Housing Type column with value All

Add Measure Type column with value Houses

Add Unit column with value Count

&nbsp;

**Sheet: T1_3 Social Housing Development Programme (SHDP) New Social Housing Dwelling Starts**

(C3:P4) Period - combination of year and quarters

(B5:B17) Housing Type:

		Shared new build
		Shared off the shelf
		Shared existing satisfactory purchase
		Shared improvement
Shared Total

		Self-Contained new build
		Self-Contained off the shelf
		Self-Contained existing satisfactory purchase
		Self-Contained improvement
		Self-Contained Total
		Total 
Add Development Type column with value Social Housing Development

Add Building Stage column with value Starts

Add Measure Type column with value Houses

Add Unit column with value Count

&nbsp;

**Sheet: T1_4 Social Housing Development Programme (SHDP) New Social Housing Dwelling Completions**

(C3:P4) Period - combination of year and quarters

(B5:B17) Housing Type:

		Shared new build
		Shared off the shelf
		Shared existing satisfactory purchase
		Shared improvement
Shared Total

		Self-Contained new build
		Self-Contained off the shelf
		Self-Contained existing satisfactory purchase
		Self-Contained improvement
		Self-Contained Total
Total 
Add Development Type column with value Social Housing Development

Add Building Stage column with value Completions

Add Measure Type column with value Houses

Add Unit column with value Count

&nbsp;

3 Tables can now be joined as one dataset with name NIHE - Building Development

****

**End table structure:**

Period, Reason for Homelessness, Household Composition, Household Homeless Status, Measure Type, Unit, Value

Notes at bottom of each sheet needs to be added to description/comment/metadata

**Sheet: T2_1 Households Presenting As Homeless by Reason**

(A4:A47) Period - combination of year and quarters

		Periods with total to be replaced with relevant year range
(B3:Z3) Reason for Homelessness 

Intimidation breakdown: values with .. to be replaced with 0 and “Breakdown not available” put in Marker column

Accommodation breakdown: values with .. to be replaced with 0 and “Breakdown not available” put in Marker column

Add Household Homeless Status column with value Presenting

Add Household Composition column with value All

&nbsp;

**Sheet: T2_2 Households Presenting As Homeless by Household Type**

(A4:A47) Period - combination of year and quarters

		Periods with total to be replaced with relevant year range
(B3:B4) Household Composition:

		Single Male 16-17 yrs (joined B2 with B3)
		Single Male 18-25 yrs (joined B2 with C3)
		Single Male 26-59 yrs (joined B2 with D3)
		Single Male Total (joined B2 with E3)
Single Female 16-17 yrs (joined F2 with F3)

		Single Female 18-25 yrs (joined F2 with G3)
		Single Female 26-59 yrs (joined F2 with H3)
		Single Female Total (joined F2 with I3)
		Couples (J2)
Families (K2)

		Pensioner Household (L2)
		Undefined (M2)
		Total (N2)
Add Household Homeless Status column with value Presenting

Add Reason for Homelessness column with value All

&nbsp;

Sheet: T2_3 Homeless Households Accepted as Full Duty Applicants by Reason

(A4:A47) Period - combination of year and quarters

		Periods with total to be replaced with relevant year range
(B3:X3) Reason for Homelessness  (Columns hidden on sheet)

Intimidation breakdown: values with .. to be replaced with 0 and “Breakdown not available” put in Marker column

Accommodation breakdown: values with .. to be replaced with 0 and “Breakdown not available” put in Marker column

(Y and Z) Set Reason for Homelessness as All

For Y column set Household Status to Live Full Duty

For Z column set Household Status to Discharged Full Duty

Set Marker column for Y and Z values to “Accepted during Quarter” 

Add Household Homeless Status column with value Accepted as Full Duty

Add Household Composition column with value All

&nbsp;

3 tables can now be joined together as one dataset with name NIHE Homelessness by Reason and Household Type 



****


**End table structure:**

Period, ONS Geography Code, House Price and Index Values, Housing Type, Housing Sector, Measure Type, Unit, Value

Notes at bottom of each sheet needs to be added to description/comment/metadata

**Sheet: T3_1 Northern Ireland House Price and Index Values**

(A4:B55) Period - Year and quarter columns need to be formatted together into calendar years

(C3:F3) House Price and Index Values

		C3: NI House Price Index = House Price Index
		D3: NI Standardised House Price = Standardised House Price
E3: Quarterly change = Quarterly change

		F3: Annual change = Annual change
Add Housing Type column with value All

Add ONS Geography Code column with value N07000001

Add Housing Sector column with value All

Add Measure Type column:

		House Price Index = Index
Standardised House Price value is: GBP

		Quarterly change value is: Percentage
		Annual change value is: Percentage
All Unit column:

House Price Index value is: Index

		Standardised House Price value is: GBP
		Quarterly change value is: Percent
		Annual change value is: Percent

&nbsp;

**Sheet: T3_2 Number of Verified Residential Property in Northern Ireland**

(A4:B55) Period - Year and quarter columns need to be formatted together into calendar years

(C3:G3) Housing Type

Add House Price and Index Values with value N/A

Add ONS Geography Code column with value N07000001

Add Housing Sector column with value All

Add Measure Type column: with value Sales

All Unit column with value count

&nbsp;

**Sheet: T3_3 Northern Ireland House Price by Property Type**

(B3) Period - one quarter value 

(B3:E3) House Price and Index Values:

		B3: index (Quarter 4 2019) = House Price Index
		C3: Percentage Change on Previous Quarter = Quarterly Change
		D3: Percentage Change over 12 Months = Annual Change
		E3 = Standardised Price (Quarter 2 2019) = Standardised Price
(A5:A9) Housing Type

Add ONS Geography Code column with value N07000001

Add Housing Sector column with value All

Add Measure Type column:

		House Price Index = Index
Standardised House Price value is: GBP

		Quarterly change value is: Percentage
		Annual change value is: Percentage
All Unit column:

House Price Index value is: Index

		Standardised House Price value is: GBP
		Quarterly change value is: Percent
		Annual change value is: Percent

&nbsp;

**Sheet: T3_4 Northern Ireland New Dwelling Sales and Prices**

(B3) Period - combination of years and quarters (Calendar or FInancial?)

(B3:C4) House Price and Index Values

		Number of Sales = New Dwelling Sales
		Average Price = New Dwellings Average Price
Add Housing Type column with value All

Add ONS Geography Code column with value N07000001


Add Housing Sector column with value All
Add a Measure Type column:

		New Dwelling Sales =  Sales
		New Dwellings Average Price = GBP
Adda Unit column:

		New Dwelling Sales = count
		New Dwellings Average Price = price

&nbsp;

**Sheet: T3_5 Northern Ireland New Dwelling Sales and Prices by Local Government District**

(A2) Period - Quarter date value in heading	

(A9:A21) ONS Geography code - Values to be changed to following codes:

		Antrim and NewtownAbbey = N09000001
		Ards and North Down = N09000011
		Armagh City, Banbridge and Craigavon = N09000002
		Belfast = N09000003
		Causeway Coast and Glens = N09000004
		Derry City and Strabane = N09000005
		Fermanagh and Omagh = N09000006
		Lisburn and Castlereagh = N09000007
		Mid and East Antrim = N09000008
		Mid Ulster = N06000010
		Newry, Mourne and Down = N09000010
		Northern Ireland = N07000001
(B4:G5) Housing Sector

		Private Sector
		Public Sector
		All Sectors
		Replace N/A values with a zero (0) and put Not Applicable in Marker column
Add Housing Type column with value All

Add House Price and Index Values with value N/A

Add Measure Type column

		Sales values = Count
		Average Price values = GBP
Add Unit column

		Sales values = Sales
		Average Price values = Average Price

&nbsp;

**5 tables can now be joined together as one dataset with name NIHE - Housing Stock**


