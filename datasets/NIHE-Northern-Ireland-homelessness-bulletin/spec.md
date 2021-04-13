**Northern Ireland homelessness bulletin**

https://www.communities-ni.gov.uk/topics/housing-statistics#toc-2

**JOIN**


**Flowchart**

https://gss-cogs.github.io/family-homelessness/datasets/specflowcharts.html?NIHE-Northern-Ireland-homelessness-bulletin/flowchart.ttl

**NIHE Homelesssness Presentations** 

**End table structure:** 
Period, Reason for Homelessness, Accommodation not Reasonable breakdown, Intimidation breakdown, Loss of Rented Accommodation reason, Household Composition, ONS Geography, Assessment Decision, Legislative test Outcome, Repeat Homeless Presentations, Measure Type, Unit, Value

Following column needs to be added so dataset from Northern Ireland Housing Statistics can be joined:
Household Homeless Status column with value Presenting as Homeless

**Sheet: 1_1 - Homeless presenters by reason**

(A) Period - format with relevant year and quarter

(B2:P2) Reason for Homelessness

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add Household Composition with value All

Add ONS Geography code with value N07000001

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**Sheet 1_1A - Homeless presenters: Accommodation not reasonable breakdown**

(A) Period - format with relevant year and quarter

(B2:J2) Accommodation not Reasonable breakdown

Add Reason for Homelessness column with value All

Add Intimidation breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add Household Composition with value All

Add ONS Geography code with value N07000001

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**Sheet 1_1B - Homeless presenters: Intimidation Breakdown**

(A) Period - format with relevant year and quarter

(B2:H2) Intimidation breakdown

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add Household Composition with value All

Add ONS Geography code with value N07000001

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**Sheet 1_1C - Homeless presenters: Loss of rented Accommodation**

(A) Period - format with relevant year and quarter

(B2:M2) Loss of rented Accommodation reason

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Household Composition with value All

Add ONS Geography code with value N07000001

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**Sheet 1_2 - Homeless presenters by Household typ**e

(A) Period - format with relevant year and quarter

(B2:N2) Household Composition 

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
Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add ONS Geography code with value N07000001

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**Sheet 1_3 Homeless presenters by local government district**

(B2:H2) Period - Calendar quarter unless stated

DO NOT need a main column for this one, represented in Unit and Measure Type Columns

(A5:A17) ONS Geography code - Values to be changed to following codes:

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
		
Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add Household Composition with value All

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count and Per 1,000 population

&nbsp;

**Sheet 1_4 Homeless presenters by Decision**

(B2:E4) Period - Calendar quarter unless stated

(A4:A13) Assessment Decision (as per cell values) 

Add ONS Geography code with value N07000001

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add Household Composition with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**Sheet 1_5 Homeless presenters by legislative test outcome**

(A3:A14) Period - Calendar quarter unless stated

(B2:G2) Legislative test Outcome (as per cell values) 

Add ONS Geography code with value N07000001

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add Household Composition with value All

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**Sheet 1_6 Repeat Homeless Presentations**

(A3:A14) Period - Calendar quarter unless stated

(B2:G2) Repeat Homeless Presentations 
		Total 
Add ONS Geography code with value N07000001

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Loss of rented Accommodation reason column with value All

Add Household Composition with value All

Add Assessment Decision column with value All

Add Legislative test Outcome with value All

Add Repeat Homeless Presentations with value N/A

Add Measure Type column with value Household

Add Unit Column with values Count

&nbsp;

**All 9 tables can be joined as one dataset with the title - NIHE Homelesssness Presentations**


******************


**NIHE - Homelessness Acceptances**

**End table structure:**
Period, Reason for Homelessness, Accommodation not Reasonable breakdown, Intimidation breakdown, Household Composition, ONS Geography code, Priority need Category, Housing Assessment Outcome, Age Bracket, Assessment Decision, Measure Type, Unit, Value

**Sheet: 2_1 Households accepted as homeless by reason**

(A6:A21) Period - Calendar quarter unless stated

(B2:O2) Reason for Homelessness - Values as in cells apart from

		P4 and Q4
			Status of Household Duty Discharged
			Status of Household Live full duty applicants
			
Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Household Composition column with value All

Add ONS Geography code column with value N07000001

Add Priority need Category column with value all

Add Housing Assessment Outcome column with value All

Add Age Bracket column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_1A Households accepted as homeless: Accommodation not reasonable breakdown**

(A3:A14) Period - Calendar quarter unless stated

(B2:J2) Accommodation not Reasonable breakdown

Add Reason for Homelessness column with value All

Add Intimidation breakdown column with value All

Add Household Composition column with value All

Add ONS Geography code column with value N07000001

Add Priority need Category column with value all

Add Housing Assessment Outcome column with value All

Add Age Bracket column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_1B Households accepted as homeless: Intimidation Breakdown**

(A3:A14) Period - Calendar quarter unless stated

(B2:G2) Intimidation breakdown

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Household Composition column with value All

Add ONS Geography code column with value N07000001

Add Priority need Category column with value all

Add Housing Assessment Outcome column with value All

Add Age Bracket column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_2 Households accepted as homeless by household type**

(A5:A16) Period - Calendar quarter unless stated

(B2:N2) Household Composition 

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
Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add ONS Geography code column with value N07000001

Add Priority need Category column with value all

Add Housing Assessment Outcome column with value All

Add Age Bracket column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_3 Households accepted as homeless by local government district**

(B2) Period - Calendar quarter unless stated

DO NOT need a main column for this one, represented in Unit and Measure Type Columns

(A5:A17) ONS Geography code - Values to be changed to following codes:

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
Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Household Composition column with value All

Add Priority need Category column with value all

Add Housing Assessment Outcome column with value All

Add Age Bracket column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_4 Total households discharged by local government district**

(B2:H2) Period - Financial year 2018/19

Add Assessment Decision column with value Discharged

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Household Composition column with value All

Add ONS Geography code column with value N07000001

Add Priority need Category column with value all

Add Housing Assessment Outcome column with value All

Add Age Bracket column with value All

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_5 Households accepted as homeless by priority need category**

(A4:A15) Period - Calendar quarter unless stated

(B2:G2) Priority Need Category

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Household Composition column with value All

Add ONS Geography code column with value N07000001

Add Housing Assessment Outcome column with value All

Add Age Bracket column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_6 Households accepted as homeless by Outcome**

(A4:A15) Period - Calendar quarter unless stated

(B2:G2) Housing Assessment Outcome

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Household Composition column with value All

Add ONS Geography code column with value N07000001

Add Priority need Category column with value all

Add Age Bracket column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: 2_7 Households accepted as homeless by Age Bracket**

(B2:E3) Period - Calendar quarter unless stated

(A4:A11) Age Bracket

Add Reason for Homelessness column with value All

Add Accommodation not Reasonable breakdown column with value All

Add Intimidation breakdown column with value All

Add Household Composition column with value All

Add ONS Geography code column with value N07000001

Add Priority need Category column with value all

Add Housing Assessment Outcome column with value All

Add Assessment Decision column with value Accepted

Add Measure Type column with value Children

Add Unit column with value Count

&nbsp;

**All 9 tables can be joined as one dataset with the title NIHE - Homelessness Acceptances** 



********



**NIHE - Temporary Accommodation** 

**End table structure:**
Period, Accommodation Type, Household Composition, Age Bracket, Measure Type, Unit, Value

**Sheet: 3_1 Placements in temporary accommodation by household type**

(A4:A15) Period (calendar year unless stated)

(B2:M2) Household Composition 

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
		Total (M2)
Add Measure Type column with value Placements

Add Accommodation Type column with value All

Add Age Bracket column with value All

Add Unit column with value Count

&nbsp;

**Sheet: 3_2 Placements in temporary accommodation by accommodation**

(A4:A15) Period (calendar year unless stated)

(B2:G3) Accommodation Type

Add Household Composition column with value All

Add Age Bracket column with value All

Add Measure Type column with value Placements

Add Unit column with value Count

&nbsp;

**Sheet: 3_3 Children in temporary accommodation by type of accommodation**

(A4:A9) Period (calendar year unless stated)

(B2:F3) Accommodation Type

Add Household Composition column with value All

Add Age Bracket column with value All

Add Measure Type column with value Children

Add Unit column with value Count

&nbsp;

**Sheet: 3_4 Children in temporary accommodation by age category**

(A2:D3) Period (month)

(A4:A9) Age Bracket

Add Household Composition column with value All

Add Accommodation Type column with value All

Add Measure Type column with value Children

Add Unit column with value Count

&nbsp;

**Sheet: 3_5 Households in temporary accommodation by banded length of stay and accommodation type**

(A4:A21) Period (calendar year unless stated)

(B4:B9) Accommodation Type

(C2:J3) Length of Stay

		<6 months -> less than 6 Months
		6 Months to <12 Months -> 6 to 12 months
		1 to <2 Years -> 1 to 2 years
		2 to <3 Years -> 2 to 3 years
		3 to <4 Years -> 3 to 4 years
		4 to <5 Years -> 5 to 5 years
		5 Years + -> 5 years plus
		Total = total
Add Household Composition column with value All

Add Measure Type column with value Households

Add Age Bracket column with value All

Add Unit column with value Count

Any values with * should be replaced with a zero (0) and “Statistical disclosure” should be put in marker column cell

&nbsp;

**All 5 tables can be joined as one dataset with the title NIHE - Temporary Accommodation**


When changing Geographical locations to codes try to use the codelist file rather than hard coding (This needs to be created and put in its own file within the GH Repo)







