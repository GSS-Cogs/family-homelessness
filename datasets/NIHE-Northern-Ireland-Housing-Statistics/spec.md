**Northern Ireland Housing Statistics**

https://www.communities-ni.gov.uk/topics/housing-statistics#toc-2

**JOIN**

**Flowchart**

https://gss-cogs.github.io/family-homelessness/datasets/specflowcharts.html?NIHE-Northern-Ireland-homelessness-bulletin/flowchart.ttl

*Only transform sheets T3_8, T3_9, T3_10, T3_11. 

*This data has a lot of similarities with tables  1_1 to 1_6 in dataset NIHE - Homelessness Presentations for ETL Northern Ireland homelessness bulletin and should be joined up with it. For this add these columns :**

Add ONS Geography code with value N07000001

Add Accommodation not Reasonable breakdown column with value N/A

Add Intimidation breakdown column with value N/A

Add Loss of rented Accommodation reason column with value All

Add Legislative test Outcome with value N/A

Add Repeat Homeless Presentations with value N/A

**End Table Structure**
Period, ONS geography code, Household composition, Accommodation not reasonable breakdown, Intimidation breakdown, Reason for homelessness, Loss of rented accommodation reason, Assessment decision, Legislative test outcome, Repeat homeless presentations, Measure Type, Unit, Marker, Value

**Sheet: T3_8 Households presenting as homeless by reason**

(C3:Q3) Year - Change name to Period and format years accordingly (Financial/calendar?)

(A4:A18) Reason for Homelessness

Add Household Composition column with value All

Add Household Homeless Status column with value Presenting as Homeless

Add Assessment Decision column with value All

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: T3_9 Households parenting as homeless by household type**

(C3:Q3) Year - rename Period and format years accordingly (Financial/calendar?)

(A4:A18) Household Composition 

		Single Male 16-17 yrs (joined A with B)
		Single Male 18-25 yrs (joined A with B)
		Single Male 26-59 yrs (joined A withB)
		Single Male Total (joined A withB)
Single Female 16-17 yrs (joined A with B)

		Single Female 18-25 yrs (joined A with B)
		Single Female 26-59 yrs (joined A with B)
		Single Female Total (joined A with B)
		Couples 
Families

		Pensioner Household 
		Undefined 
		Total 
Add Reason for Homelessness column with value All

Add Household Composition column with value All

Add Assessment Decision column with value All

Add Household Homeless Status column with value Presenting as Homeless

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: T3_10 Households presenting as Homeless by outcome**

(B3:H3) Year- rename Period and format years accordingly (Financial/calendar?)

(A4:A12) Assessment Decision

Add Reason for Homelessness column with value All

Add Household Composition column with value All

Add Household Homeless Status column with value Presenting as Homeless

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**Sheet: T3_11 Homeless Households accepted as full duty applicants by reason**

(B3:P3) Year- rename Period and format years accordingly (Financial/calendar?)

(A4:A20) Reason for Homelessness

Add Household Composition column with value All

Add Household Homeless Status column with value Accepted as Full Duty

Add Assessment Decision column with value All

Add Measure Type column with value Households

Add Unit column with value Count

&nbsp;

**5 tables to be joined up with name NIHE Homelesssness Presentations and joined up with other dataset as mentioned above**









