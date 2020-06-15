**Housing Options (Prevent 1) Statistics**

https://www2.gov.scot/Topics/Statistics/Browse/Housing-Regeneration/RefTables

**Flowchart**
To be created


Use ONS Geography Codes to convert from Local Authority 

Scotland = S04000001

Aberdeen City = S05000001

Aberdeenshire = S05000002


Angus = S05000003

Argyll & Bute = S05000004

Clackmannanshire = S05000005

Dumfries & Galloway = S05000006

Dundee City = S05000007

East Ayrshire = S05000008

East Dunbartonshire = S05000009

East Lothian = S05000010

East Renfrewshire = S05000011

Edinburgh = S05000012

Eilean Siar = S12000013 (Na h-Eileanan Siar on Portal)

Falkirk = S05000013

Fife = S05000014

Glasgow City = S05000015

Highland = S05000016

Inverclyde = S05000017

Midlothian = S05000018

Moray = S12000020

North Ayrshire = S05000019

North Lanarkshire = S05000020

Orkney = S08000025

Perth & Kinross = S05000021

Renfrewshire = S05000022

Scottish Borders = S12000026

Shetland = S05000023

South Ayrshire = S05000025

South Lanarkshire = S05000026

Stirling = S05000024

West Dunbartonshire = S05000027

West Lothian = S05000028

<br /> 


**End dataset 1 structure
Period, ONS Geography Code, Marker, Annual change, Totals, Housing options approaches, Rate of Approaches per 10,000 households,  Housing Options activity, Outcomes by Quarter, Repeat Approaches by household, Measure type, Unit, Value**

**End dataset 2 structure 
Period, Reasons for approaching homelessness services, Activity type, Housing Option activity type, Measure type, Unit, Value**

**Dataset 1 - Tables 1, 2, 3, 7, 8, 9, 10 can be joined as one cube using ONS Geography code with name - SG Housing Options Prevent1 Statistics in Scotland by location
Dataset 2 - Table 4, 5, 6 can be joined by Period as one cube with name SG Housing Options Prevent1 Statistics in Scotland by Period**

<br />

**Sheet: Table 1 - Approaches** 
Title: Table 1: Total Housing Options approaches by LA and quarter**

(A) Local authority change to ONS code and add Local Authority as attribute - display Local Authority on PMD if possible
(B:U) Period - change to Quarters year
(Row 29) Add footnote as attribute - 1 There is a known issue with the number of approaches for Q1 2018/19 and Q3 2018/19 for Perth & Kinross, for this reason please treat any results with caution. 
(X:AA) - Period change to financial years 
 
Add column Period  
Add footnote to totals column- Column totals may not sum to total of individual cells due to rounding.
Add to description - Disclosure Control has been applied to this table.  All cells have been rounded to the nearest five.
Add Data marker - 

Add column Housing options approaches with value Total
Erroneous numbers in columns AB, AC, AD - disregard

Add Measure Type column 
	
		Approaches annual change
		Approaches percentage change
		Financial year total

Add Unit column

		(X:Y) Count
		(AA) Percent Change
		(X) Financial year 2017/18 total
		(Y) Financial year 2018/19 total
		(Z) Annual change

<br />


**Sheet: Table 2 - Unique Households
Title: Table 2: Unique household approaches as a percentage of households in each Local Authority**

(A) Local authority change to ONS code and add Local Authority as attribute - display Local Authority on PMD if possible

(Row 29) Add footnote as attribute - 1 There is a known issue with the number of approaches for Q1 2018/19 and Q3 2018/19 for Perth & Kinross, for this reason please treat any results with caution. 

Erroneous numbers in columns A and B from rows 48 to 81 - disregard

Add Measure Type column 
	
		(B) Number of Households
		(C) Unique household approaches 2018/19
		(D) Unique household approaches within Local Authority percentage 
		(E) Rate of Approaches per 10,000 households 

Add Unit column

		(B:C) Count
		(C) Percentage
		(E) Rate 
		

Create codelist - Quarterly from last day of month http://reference.data.gov.uk/id/gregorian-interval/2020-04-30T00:00:00/P3M
 
Add metadata as attribute in rows 39 and 40

<br />

**Sheet: Table 3 - Open Approaches
Title: Table 3: Open Approaches at the end of each quarter by LA**
(A) Local authority change to ONS code and add Local Authority as attribute - display Local Authority on PMD if possible
(B - U) Period - change to Quarters year

Discard Approaches received 1 April 2014 to 31 March 2018 (from Table1)and Open Approaches as a % of all Approaches (columns X and Y) as derivative
Add Local authority proportions 2018/19 as column with values as percentages
Add column Approaches with open cases 

Add Measure Type column 
	
		Households

Erroneous numbers in columns AC and AD from rows 7 to 10 and Columns A and B from rows 42 to 77 - disregard

Add metadata as attribute in rows 39 and 40

<br />

**Sheet: Table 4 - Reasons
Title: Table 4a: Reasons for Approach (Number)**

(B - U) Period - change to Quarters year
(A) Create column with title Reasons for approaching homelessness services changed from Reasons for approach adding the following categories for reasons:
General housing options advice
Dispute within household / relationship breakdown: non-violent
Asked to leave
Risk of losing accommodation
Other action by landlord resulting in the termination of the tenancy 
Dispute within household: violent or abusive
Discharge from prison / hospital / care / other institution
Other reason for loss of accommodation
Other reason for leaving accommodation / household
Termination of tenancy / mortgage due to rent arrears / default on payments
Accommodation unsuitable
Other
Personal issues – affordability / financial difficulties
Fleeing non-domestic violence
Harassment
Applicant terminated secure accommodation
Overcrowding
Benefit issues & Welfare Reform
Household experiencing anti-social behaviour / neighbour problems
Property condition
Household member needing care
Forced division and sale of matrimonial home
Loss of service / tied accommodation
Landlord issue
Emergency add attribute to cover the following metadata includes fire, flood, storm, and closing order from Environmental Health etc

Add column Total
Add column with unit value Percent or Count
Reasons for approach abbreviated number and percent can be removed as derivative 


Add Measure Type column 
	
		Reasons for Approach (Percent)
		Reasons for Approach (Number)

Add Unit column

		(B:U) Count - Rows (4:30)
		(B:U) Percent - Rows (35:61)

<br />

**Sheet: Table 5 Maximum Activity Type 
Title: Table 5a and 5b: Maximum Activity Type change (numbers and percentage) to Table 5 Activity types**
(B - U) Period - change to Quarters year

Add column to above columns Total 
Add column Activity type with the following categories:
Type I – Active Information, Sign-posting and Explanation 
Type II – Casework
Type III – Advocacy, Representation and Mediation at Tribunal or Court Action Level

Add Measure Type column 
	
		Cases
		Annual change percentage change
		Annual change Financial year total
		Percent summary

Add Unit column

		(B:U) Count
		(Z) Percent Change
		(W) Financial year 2017/18 total
		(X) Financial year 2018/19 total
		(Y) Annual change 

<br />

**Sheet: Table 6: Housing Options activities by Q
Title: Table 6 Housing Options activities by Quarter change to Table 6 Housing Options assistance activities by quarter**

(B - U) Period - change to Quarters year 
Remove column V as derivative

Add column Housing Option activity type with the following categories:
General Housing advice/Tenancy rights advice
Client informed of rights under homelessness legislation
Help to move property
Rent/repairs/referrals/negotiation with landlords
Financial assistance/advice
Other
Referral to health/Social Work/employment services
Help to remain in accommodation
Tenancy/social care support/adaptations to property
Mediation/outreach work
Mortgage/home ownership advice
Add column Total (all activities)
 
Add column with value Percent or Count
Add column Annual change with the value Change, Financial year total and % change


Add Measure Type column 
	
		Activities annual change
		Activities annual percentage change
		Financial year total

Add Unit column

		(B:V) Count
		(Z) Percent Change
		(W) Financial year 2017/18 total
		(X) Financial year 2018/19 total
		(Y) Annual change

<br />

**Sheet: Table 7a and 7b Housing Options activities by Local Authority, during 1 April 2018 to 31 March 2019 (number and percentage)
Title: Table 7 Housing Options activities by Quarter change to Table 7 Housing Options assistance activities by Local Authority**

(A) Local authority change to ONS code and add Local Authority as attribute - display Local Authority on PMD if possible
(Row 29 and 70) Add footnote as attribute - 1 There is a known issue with the number of approaches for Q1 2018/19 and Q3 2018/19 for Perth&Kinross, for this reason please treat any results with caution.

Add column named Housing Options activity with the following categories:
General Housing advice/Tenancy rights advice
Client informed of rights under homelessness legislation
Help to move property
Rent/repairs/referrals/negotiation with landlords
Financial assistance/advice
Other
Referral to health/Social Work/employment services
Help to remain in accommodation
Tenancy/social care support/adaptations to property
Mediation/outreach work
Mortgage/home ownership advice
Add Total to replace All

Add column Unit with value Percent or Count
Add column Period change to financial year 1 April 2018 to 31st March 2019


Add Measure Type column 
	
		Approaches annual change
		Approaches percentage change
		Financial year total

Add Unit column

		(X:Y) Count
		(AA) Percent Change
		(X) Financial year 2017/18 total
		(Y) Financial year 2018/19 total
		(Z) Annual change

<br />

**Sheet: Table 8 - Outcomes by Quarter
Title: Table 8a and 8b  Outcomes by Quarter (number and percentage) change to Table 8 outcomes by Quarter**

(B - U) Period - change to Quarters year
Add column named Outcomes by Quarter with the following categories:
Made homelessness application to local authority
Remained in current accommodation
Lost Contact/ Not known
Other (known)
Local Authority or Registered Social Landlord Tenancy
Private Rental Sector Tenancy
Moved-in with friends/ relatives

Add column with value Percent or Count
Add column Annual change with the value Change, Financial year and % change


Add Measure Type column 
	
		Approaches annual change
		Approaches percentage change
		Financial year total

Add Unit column

		(X:Y) Count
		(AA) Percent Change
		(X) Financial year 2017/18 total
		(Y) Financial year 2018/19 total
		(Z) Annual change

<br />

**Sheet: Table 9 - Outcomes by LA
Title: Table 9: Outcomes by LA: 1 April 2018 to 31 March 2019 change to Table 9: Outcomes by Local Authority - 1 April 2018 to 31 March 2019**

(A) Local authority change to ONS code and add Local Authority as attribute - display Local Authority on PMD if possible
(Row 29 and 68) Add footnote as attribute - 1 There is a known issue with the number of approaches for Q1 2018/19 and Q3 2018/19 for Perth&Kinross, for this reason please treat any results with caution. 

Add column named Outcomes by Quarter with the following categories:
Made homelessness application to local authority
Remained in current accommodation
Lost Contact/ Not known
Other (known)
Local Authority or Registered Social Landlord Tenancy
Private Rental Sector Tenancy
Moved-in with friends/ relatives
Add column with value Percent or Count
Add Total column


Add Measure Type column 
	
		Approaches annual change
		Approaches percentage change
		Financial year total

Add Unit column

		(X:Y) Count
		(AA) Percent Change
		(X) Financial year 2017/18 total
		(Y) Financial year 2018/19 total
		(Z) Annual change

<br />

**Sheet: Table 10 - Table 10 Repeat Approaches
Title: Table 10: Households making Repeat Approaches change to Table 10: Households making Repeat Approaches to homelessness services**

(A) Local authority change to ONS code and add Local Authority as attribute - display Local Authority on PMD if possible
(Row 30) Add footnote as attribute - 1 There is a known issue with the number of approaches for Q1 2018/19 and Q3 2018/19 for Perth&Kinross, for this reason please treat any results with caution.

Add column Households making Repeat Approaches change to Repeat Approaches by household with the following categories:
Made homelessness application to local authority
Remained in current accommodation
Lost Contact/ Not known
Other (known)
Local Authority or Registered Social Landlord Tenancy
Private Rental Sector Tenancy
Moved-in with friends/ relatives
Add unit as count
Add Total for All Households
Add Proportioning of Households making Repeat Approaches measure Percent


Add Measure Type column 
	
		Approaches annual change
		Approaches percentage change
		Financial year total

Add Unit column

		(X:Y) Count
		(AA) Percent Change
		(X) Financial year 2017/18 total
		(Y) Financial year 2018/19 total
		(Z) Annual change


