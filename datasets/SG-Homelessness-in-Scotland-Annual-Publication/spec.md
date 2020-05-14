**Homelessness in Scotland: Annual Publication**

https://www2.gov.scot/Topics/Statistics/Browse/Housing-Regeneration/RefTables#Publications

**Flowchart**

https://gss-cogs.github.io/gss-data-docs/architecture/homelessness/familymappings.html?sghomelessnessannual.ttl

Use the following codes for conversion from Local Authority to ONS Geography Code

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

**End table structure**

Period, ONS Geography Code, Rough Sleeping Occurrence, Accommodation Type,  Homelessness Breakdown, Armed Service Membership, Previous Application to LA, Sex, Age, Household Composition, Ethnicity, Reason for Application, Failing to Maintain Accommodation Reasons, Measure Type, Unit, Value

**Sheet: Table 1 Number of applications under the Homes persons legislation by Local Authority**

(B3:R4) Year -rename to Period and format as required (Financial/calendar?)

(A5:A37) Local Authority - rename to ONS Geography Code and change to codes

(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values 

Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All

Add Homelessness Breakdown column with value Applicants

Add Armed Service Membership column with value N/A

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 
	
		(B:R)(S) Households

(T) Percentage Change

Add Unit column

		(B:R) Count
		(S:T) Percent Change

<br />

**Sheet: Table2 
Table 2a Number of homelessness applications where rough sleeping occurred prior to application in scotland**


(B3:R4) Year - rename Period and format as required

(A5:A10) Rough Sleeping Occurrence (Split count and percentage)

		Row 5 should replicate data from table 1
		At least once during last 3 months
		The night before

(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values 

Add ONS Geography Code column with value S04000001

Add Homelessness Breakdown column with value Rough Sleeping

Add Accommodation Type column with value All

Add Armed Service Membership column with value N/A

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B:R) Households and Percentage
	(S) Households
	(T) Percentage change
Add Unit column

	(B:R) Count and Percent
	(S) Change
	(T) Percent Change

<br />
**Table 2b Number of homelessness applications where rough sleeping occurred prior to application in Scotland by Local Authority**

(B17:G18) Year - rename Period and format as required

(A19:A51) rename to ONS Geography Code and change to codes

(B18:I18) Rough Sleeping Occurrence(Split count and percentage)

		At least once during last 3 months
		The night before

(H:I) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values 

Add Accommodation Type column with value All

Add Homelessness Breakdown column with value Rough Sleeping

Add Armed Service Membership column with value N/A

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B, C, F, G) Households and Percentage
	(D and H) Households
	(E and I) Percentage change
Add Unit column

	(B, C, F, G) Count and Percent
	(D and H) Change
	(E and I) Percent Change

<br />

**Sheet: Table 3 Type of Property where the applicant became homeless/threatened with homelessness**

(B3:M4) Year - rename Period and format as required

(A6:A29) Accommodation Type (Scotland row can be ignored as it is in Table 1)

Add ONS Geography Code column with value S04000001

(N:O) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values 

Add Rough Sleeping Occurrence column with value N/A

Add Armed Service Membership column with value N/A

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add Household Composition column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Homelessness Breakdown column with value Homeless or Threatened with Homelessness

Add Ethnicity column with value All

Add Reason for Application column with value All

Add Measure Type column 

	(B:M)(N) Households
	(O) Percentage Change
Add Unit column

	(B:M) Count
	(N) Change
	(O) Percent Change

<br />

**Sheet: Table 4 Number of homelessness applicants formerly in the armed services in Scotland**

(B3:M4) Year - rename Period and format as required

(A6:A15) Armed Service Membership (columns.csv to point to General Time Period codelist) (All applicants row can be ignored as it is in Table 1)

		Total in Armed Forces
		Less than 5 years ago
		5 or more years ago
		Never been in the Armed Forces
		Not known or refused

(N:O) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values


Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All


Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add ONS Geography Code column with value S04000001

Add Household Composition column with value All

Add Homelessness Breakdown column with value Armed Forces Membership

Add Ethnicity column with value All

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B:M)(N) Households and Percentage
	(O) Percentage Change

Add Unit column

	(B:M) Count and Percent
	(N) Change
	(O) Percent Change

<br />

**Sheet: Table 5 Number of applicants formerly looked after by the Local Authority in Scotland**

(B3:M4) Year - rename Period and format as required

(A6:A15) Previous Application to LA (columns.csv to point to General Time Period codelist) (All applicants row can be ignored as it is in Table 1)

		Total previously looked after
		Less than 5 years ago
	5 or more years ago
	Never been in the Armed Forces
	Not known or refused


(N:O) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All

Add Armed Service Membership column with value N/A

Add Homelessness Breakdown column with value Previous Application to LA

Add ONS Geography Code column with value S04000001

Add Sex column with value All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B:M)(N) Households and Percentage
	(O) Percentage Change
Add Unit column

	(B:M) Count and Percent
	(N) Change
	(O) Percent Change

<br />

**Sheet: Table 6
Table 6a Age and Gender of all main applicants (Counts)**

(C3:S4)  Year - rename Period and format as required
(
A6:A19) Gender - rename Sex (Male = M, Female = F)

(B6:B19) Age band - rename Age - change:

		Total Males to Total
		Total Females to Total
(
T:U) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All

Add Armed Service Membership column with value N/A

Add Homelessness Breakdown column with value Gender

Add Previous Application to LA column with value N/A

Add Household Composition column with value All

Add Ethnicity column with value All

Add ONS Geography Code column with value S04000001

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B:M)(T) Households and Percentage
	(U) Percentage Change
Add Unit column

	(B:M) Count and Percent
	(T) Change
	(U) Percent Change

<br />

**Table 6b Age and Gender of all main applicants (Percentages)**

Do the same as for Table 6a but without columns T and U. Measure Type will be Percentage and Unit will be Percent

<br />

**Sheet: Table 7
Table 7a Household type of homelessness applicants (Counts)**


(B3:R4)  Year - rename Period and format as required

(A6:A19) Household Composition

(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All

Add Armed Service Membership column with value N/A

Add Homelessness Breakdown column with value Household Type 

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

Add ONS Geography Code column with value S04000001

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B:M)(S) Households and Percentage
	(T) Percentage Change
Add Unit column

	(B:M) Count and Percent
	(S) Change
	(T) Percent Change

<br />

**Table 7b Household type of homelessness applicants (Percentages)**

Do the same as for Table 7a but without columns S and T. Measure Type will be Percentage and Unit will be Percent

<br />

**Sheet: Table 8
Table 7a Ethnicity of all main applicants (Counts)**

(B3:R4)  Year - rename Period and format as required

(A6:A19) Ethnicity (remove the letter at start???)

(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All

Add Armed Service Membership column with value N/A

Add Homelessness Breakdown column with value Ethnicity

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add ONS Geography Code column with value S04000001

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B:M)(S) Households and Percentage
	(T) Percentage Change
Add Unit column

	(B:M) Count and Percent
	(S) Change
	(T) Percent Change

<br />

**Table 8b Ethnicity of all main applicants (Percentages)**

Do the same as for Table 8a but without columns S and T. Measure Type will be Percentage and Unit will be Percent

<br />

**Sheet: Table 9
Table 9a Main reason for making application for homelessness to LA (Count)**

(B3:M4)  Year - rename Period and format as required

(A6:A25) Reason for Application

		Add Accommodation no longer available to start of A7:A17
		Add Had to leave Accommodation to start of A19:A25
(N:O) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All

Add Armed Service Membership column with value N/A

Add Homelessness Breakdown column with value Application Reasons

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

Add ONS Geography Code column with value S04000001

Add Failing to Maintain Accommodation Reasons column with value All

Add Measure Type column 

	(B:M)(S) Households and Percentage
	(T) Percentage Change
Add Unit column

	(B:M) Count and Percent
	(S) Change
	(T) Percent Change

<br />

**Table 9b Main reason for making application for homelessness to LA (Percentages)**

Do the same as for Table 9a but without columns S and T. Measure Type will be Percentage and Unit will be Percent

<br />

**Sheet: Table 10
Table 10a Reasons for failing to maintain accommodation prior to application (Counts)**

(B3:M4)  Year - rename Period and format as required

(A6:A16) Failing to Maintain Accommodation Reasons

(N:O) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Rough Sleeping Occurrence column with value N/A

Add Accommodation Type column with value All

Add Armed Service Membership column with value N/A

Add Homelessness Breakdown column with value Loss of Accommodation Reason

Add Previous Application to LA column with value N/A

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

Add ONS Geography Code column with value S04000001

Add Reason for Application with value All

Add Measure Type column 

	(B:M)(S) Households and Percentage
	(T) Percentage Change
Add Unit column

	(B:M) Count and Percent
	(S) Change
	(T) Percent Change

<br />

**Table 10b Reasons for failing to maintain accommodation prior to application (Percentages)**

Do the same as for Table 10a but without columns S and T. Measure Type will be Percentage and Unit will be Percent

**10 tables can now be joined up and named SG - Homelessness Applications 
Annual Publication** 

****

**End table structure**

Period, ONS Geography Code, Assessment Decision, Support Needs of Household, Measure Type, Unit, Value, Marker

**Sheet: Table 11
Table 11 a**

(B3:R4)  Year - rename Period and format as required

(A5:A18) Assessment Decision

		Change (A5) Scotland to All Assessments

(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add ONS Geography Code column with value S04000001

Add Identified Support Need column with value N/A

Add Measure Type column 

	(B:R)(S) Households
	(T) Percentage Change
Add Unit column
	(B:R) Count
	(S) Change
	(T) Percent Change

<br />

**Table 11b Reasons for failing to maintain accommodation prior to application (Percentages)**

Do the same as for Table 11a but without columns S and T. Measure Type will be Percentage and Unit will be Percent. Remove Scotland Row as these are all just 100%.

<br />

**Sheet: Table 11c Homelessness assessment decisions by Local Authority (Count)
Table 11c** 

(B3:J4)  Year - rename Period and format as required

(A5:A37) Local Authority - rename ONS Geography Code and replace with code

(B3:K4) Assessment Decision:

		(B3 + B4) Homeless Unintentional
		(B3 + C4) Homeless Intentional
		(D3 + D4) Threatened with Homelessness Unintentional
		(D3 + E4) Threatened with Homelessness Intentional
		(F3:J3) Keep the same
		(K3) Total

Add Identified Support Need column with value N/A

Add Measure Type column with value Households

Add Unit column with value Count

<br />

**Table 11d Homelessness assessment decisions by Local Authority (Percentages)**

Do the same as for Table 11c. Measure Type will be Percentage and Unit will be Percent. Remove Scotland Row as these are all just 100%.

<br />

**Sheet: Table 12 All homelessness assessments by Local Authority** 

(B3:H4)  Year - rename Period and format as required

(A5:A37) Local Authority - rename ONS Geography Code and replace with code

(B3:H4) Assessment Decision (Split out counts and percentages:

		(B3) Total Intentionally Homeless
		(D3) Total Unintentionally Homeless
		(F3) Not Intentionally or Unintentionally Homeless
		(H3) Total (Same values as in table 11c but will be removed when duplicates are dropped later on)

Add Identified Support Need column with value N/A

Add Measure Type column with value Households and Percentages

Add Unit column with value Count and Percent

<br />

**Sheet: Table 13 Applications assessed as homeless or threatened with homelessness by Local Authority**

(B3:R4)  Year - rename Period and format as required

(A5:A37) Local Authority - rename ONS Geography Code and replace with code

(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Identified Support Need column with value N/A

Add Assessment Decision column with value Homeless or Threatened with Homelessness

Add Measure Type column 

	(B:R)(S) Households and Percentage
	(T) Percentage Change
Add Unit column

	(B:R) Count and Percent
	(S) Change
	(T) Percent Change

<br />

**Sheet: Table 14  
Table 14a Repeated Homelessness: Households re-assessed as homeless within the same year** 

Ignore this table as the information is all in Table 14b.
Note: The values in Table 14a row 5 are different by 1 or 2 to the values in Table 14b row 11when they should be the same?

<br />

**Table 14b Repeated Homelessness: Households re-assessed as homeless within the same year by Local Authority**

(B10:R10) Year - rename Period and format as required

(A1:A43) Local Authority - rename ONS Geography Code and replace with code

(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Assessment Decision column with value Repeated Homelessness cases

Add Identified Support Need column with value N/A
Add Measure Type column 

	(B:R)(S) Households and Percentage
	(T) Percentage Change
Add Unit column
	(B:R) Count and Percent
	(S) Change
	(T) Percent Change

<br />

**Sheet: Table 15 Support need identified for those homeless (or threatened with homelessness) households**

(B10:M10) Year - rename Period and format as required

(A4:A11)(A14)(A17:A24) Identified Support Need (Ignore row 13 as data is iin Table 13)

(N:O) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add ONS Geography Code column with value S04000001

Add Assessment Decision column with value Homeless or Threatened with Homelessness

Add Measure Type column 

	(B:M)(N) Households and Percentage
	(O) Percentage Change
Add Unit column

	(B:M) Count and Percent
	(N) Change
	(O) Percent Change

<br />

**Sheet: Table 16 At least one support need identified for those assessed as homeless (or threatened with homelessness) by Local Authority**

(B10:M10) Year - rename Period and format as required

(A5:A37) Local Authority - rename ONS Geography Code and replace with code

(N:O) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Assessment Decision column with value N/A 

Add Identified Support Need column with value One Support Need Identified

Add Measure Type column 

	(B:M)(N) Households and Percentage
	(O) Percentage Change
Add Unit column
	(B:M) Count and Percent
	(N) Change
	(O) Percent Change

<br />

**7 tables can now be added together as one dataset with name SG - Homelessness Assessment Decisions Annual Publication**


****

**End table structure:**

Period, ONS Geography Code, Temporary Accommodation Breakdown, Accommodation Type, Placement Type, Measure Type, Unit, Value, Marker

**Sheet: Table 17 Households in temporary Accommodation at 31 march each year**

(B3:S4) Date - rename Period and format as required (31st March)

(A5:A37) Local Authority - rename ONS Geography Code and replace with code

(T:U) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Temporary Accommodation Breakdown column with value All

Add Accommodation Type column with value All

Add Placement Type column with value N/A

Add Measure Type column 

	(B:S)(T) Households and Percentage
	(U) Percentage Change
Add Unit column

	(B:S) Count and Percent
	(T) Change
	(U) Percent Change

<br />

**Sheet: Table 18 Number of households with a Pregnant woman or children who are in temporary accommodation**

(B3:S4) Date - rename Period and format as required (31st March)

(A5:A37) Local Authority - rename ONS Geography Code and replace with code

(T:U) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Temporary Accommodation Breakdown column with value 

Pregnant Woman or Children

Add Accommodation Type column with value All

Add Placement Type column with value N/A

Add Measure Type column 

	(B:S)(T) Households and Percentage
	(U) Percentage Change
Add Unit column
	(B:S) Count and Percent
	(T) Change
	(U) Percent Change

<br />

**Sheet: Table 19 Number of children in temporary accommodation**

(B3:S4) Date - rename Period and format as required (31st March)

(A5:A37) Local Authority - rename ONS Geography Code and replace with code

(T:U) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Temporary Accommodation Breakdown column with value Number of children

Add Accommodation Type column with value All

Add Placement Type column with value N/A

Add Measure Type column 

	(B:S)(T) Children and Percentage
	(U) Percentage Change
Add Unit column
	(B:S) Count and Percent
	(T) Change
	(U) Percent Change

<br />

**Sheet: Table 20 Households in temporary accommodation by type of accommodation, by Local Authority**

(B3:CM3) Date - rename Period and format as required (31st March)

(B4:CM4) Accommodation Type:

		Social Sector Accommodation
		Hostal
		Bed & Breakfast
		Other
		Total
(A5:A37) Local Authority - rename ONS Geography Code and replace with code

Add Temporary Accommodation Breakdown column with value TA Accommodation

Add Placement Type column with value N/A

Add Measure Type column Households

Add Unit column Count

<br />

**Sheet: Table 21 Households with children or pregnant woman in temporary accommodation by type of accommodation, by Local Authority**

(B3:CM3) Date - rename Period and format as required (31st March)

(B4:CM4) Accommodation Type:

		Social Sector Accommodation
		Hostal
		Bed & Breakfast
		Other
		Total
(A5:A37) Local Authority - rename ONS Geography Code and replace with code

Add Temporary Accommodation Breakdown column with value 

		Pregnant Woman or Children

Add Placement Type column with value N/A

Add Measure Type column Households

Add Unit column Count

<br />

**Sheet: Table 22 Number of children in temporary accommodation by type of accommodation, by Local Authority**

(B3:CM3) Date - rename Period and format as required (31st March)

(B4:CM4) Accommodation Type:

		Social Sector Accommodation
		Hostal
		Bed & Breakfast
		Other
		Total
(A5:A37) Local Authority - rename ONS Geography Code and replace with code

Add Temporary Accommodation Breakdown column with value 

		Number of Children
Add Placement Type column with value N/A

Add Measure Type column Children

Add Unit column Count

<br />

**Sheet: Table 23 Number of households entering and exiting temporary accommodation by Local Authority**

(B6:C7) Date - rename Period and format as required (Financial year)

(B5:C5) Temporary Accommodation Breakdown

		Entering TA
		Exiting TA
(A8:A40) Local Authority - rename ONS Geography Code and replace with code

(E:F) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add Accommodation Type column with value All

Add Placement Type column with value N/A

Add Measure Type column 

	(B:S)(T) Households and Percentage
	(U) Percentage Change
Add Unit column

	(B:S) Count and Percent
	(T) Change
	(U) Percent Change

<br />

**Sheet: Table 24 Number of households entering and exiting temporary accommodation by type of accommodation, by Local Authority**

(B6, L6) Date - rename Period and format as required (Financial year)

(B5, L5) Temporary Accommodation Breakdown

		Entering TA
		Exiting TA
(B7:I7, L7:S7) Household Composition

(A8:A40) Local Authority - rename ONS Geography Code and replace with code

Add Placement Type column with value N/A

Add Accommodation Type column with value N/A

Add Measure Type column Households

Add Unit column Count

<br />

**Sheet: Table 25 Number of households entering and exiting temporary accommodation by placement type and by Local Authority**

(B6, M6) Date - rename Period and format as required (Financial year)

(B5, K5) Temporary Accommodation Breakdown

		Entering TA
		Exiting TA
(B7:K7, M7:V7) Placement Type (to reference Accommodation Type in Ref data)

(A8:A40) Local Authority - rename ONS Geography Code and replace with code

		Change Total (All) to Scotland code
Add Accommodation Type column with value N/A

Add Temporary Accommodation Breakdown column with value Placement

Add Measure Type column Households

Add Unit column Count

<br />

**Sheet: Table 26 Number of households entering and exiting temporary accommodation by household and placement type**

(B5, K5) Date - rename Period and format as required (Financial year)

(B6, K6) Temporary Accommodation Breakdown

		Entering TA
		Exiting TA
(A9:A18) Placement Type (to reference Accommodation Type in Ref data)

(B8:I8, K8:R8) Household Composition

Add Accommodation Type column with value N/A

Add ONS Geography Code column with value S04000001

Add Measure Type column with values Households and Percentage

Add Unit column Count and Percent

<br />

**Sheet: Table 27 Average length of time (days) in accommodation (across all placements)**

(B5, L5) Date - single value in title, rename Period and format as required

(B5:L5,N5:P5) Household Composition

		No need to worry about cell N3 as these figures will have all involved exits anyway
(A6:A38) Local Authority - rename ONS Geography Code and replace with code

Add Temporary Accommodation Breakdown column with value Average length of Stay

Add Placement Type column with value All

Add Accommodation Type column with value N/A

Add Measure Type column Day(s)

Add Unit column Average

<br />

Sheet: Table 28 Number of applications that have been offered temporary accommodation

(B5:I5) Date - values in quarters, rename Period and format as required

(A6:A19) Local Authority - rename ONS Geography Code and replace with code

		Change All to Scotland geography code
Add Temporary Accommodation Breakdown column with value Offered Temporary Accommodation

Add Placement Type column with value N/A

Add Accommodation Type column with value N/A

Add Measure Type column Applications

Add Unit column Count

<br />

**Sheet: Table 29 Number of placements that have been in breach of the Unsuitable Accommodation Order**

(B5:I5) Date - values in quarters, rename Period and format as required

(A6:A17) Local Authority - rename ONS Geography Code and replace with code

		Change All to Scotland geography code
Add Temporary Accommodation Breakdown column with value In Breach of Unsuitable Accommodation Order

Add Placement Type column with value N/A

Add Accommodation Type column with value N/A

Add Measure Type column Placements

Add Unit column Count

<br />

**12 tables can now be added together as one dataset with name SG - Homelessness Temporary Accommodation Annual Publication**

****

**End table structure:**

Period, ONS Geography Code, Outcome Type, Assessment Outcome Type, Post Assessment Contact, Measure Type, Unit, Value, Marker

**Sheet: Table 30 Outcome of Households assessed as homeless or threatened with homelessness intentionality**

(B3:R4) Year - rename Period and format as required

(A5, A14) Outcome Type

(A3, A16) Assessment Outcome Type 

(A5:A14) Unintentionally Homeless or Unintentionally Threatened with Homelessness

		(A18:A26) All other Homelessness Assessments
(S:T) Format as observations in the Value column and relevant date in Period column but change measure Type and Unit values

Add ONS Geography Code column with value S04000001

Add Post Assessment Contact column with value N/A

Add Measure Type column 

	(B:R)(S) Households
	(T) Percentage Change
Add Unit column

	(B:R) Count
	(S) Change
	(T) Percent Change

<br />

**Sheet: Table 31 Outcomes for households assessed as unintentionally homeless or unintentionally threatened with homelessness by Local Authority**

(A1) Period - and format as required

(B3:J3,L3) Outcome Type

		Change All outcomes to Total
(A4:A36) Local Authority - rename ONS Geography Code and change to code

Add Assessment Outcome Type column with value Unintentionally Homeless or Unintentionally Threatened with Homelessness

Add Post Assessment Contact column with value N/A

Add Measure Type column Households and Percentage

Add Unit column Count and Percent

<br />

**Sheet: Table 32 Outcomes for Households assessed as intentionally homeless and threatened with homelessness by Local Authority**

(A1) Period - and format as required

(B3:J3,L3) Outcome Type

		Change All outcomes to Total
(A4:A36) Local Authority - rename ONS Geography Code and change to code

Add Assessment Outcome Type column with value Intentionally Homeless and Threatened with Homelessness
Add Post Assessment Contact column with value N/A

Add Measure Type column Households and Percentage

Add Unit column Count and Percent

<br />

**Sheet: Table 33 Number of applications where not known or lost contact post-assessment**

(A1) Date - rename Period and format as required

(B3:J3,L3) Post Assessment Contact

		Scotland = Total
		Contact Maintained
Not Known or Lost Contact

Add ONS Geography Code column with value S04000001

Add Outcome Outcome Type column with value All

Add Assessment Type column with value Post-Assessment

Add Measure Type column Applications and Percentages

Add Unit column Count and Percent

<br />

**4 tables can now be added together as one dataset with name SG - Homelessness Assessment Outcomes Annual Publication**





















