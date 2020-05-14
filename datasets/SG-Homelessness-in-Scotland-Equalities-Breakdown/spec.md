**Homelessness in Scotland:  Equalities Breakdown**

https://www2.gov.scot/Topics/Statistics/Browse/Housing-Regeneration/RefTables#Publications

**Flowchart**

https://gss-cogs.github.io/gss-data-docs/architecture/homelessness/familymappings.html?sghomelessnessequalities.ttl

10 sheets with 40 tables to be joined and dataset ID to be named SG Homelessness Equalities Breakdown - Applications & Assessments

**End table structure:**

Period, Age, Sex, Household Composition, Ethnicity, Rough Sleeping Occurrence, Accommodation Type, Armed Forces Membership, Previous Application to LA, Reason for Application, Failing to Maintain Accommodation Reasons, Assessment Decision, Reassessed as Homeless within same Year, Identified Support Need, Measure Type, Unit, Marker, Value


****Sheet: Table 1 Number of Applications under the Homeless Legislation


**Add the following to all 4 tables:**

Add Rough Sleeping Occurrence column with value Total

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

Add Measure Type column with value Applications

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Unit column with value Count

Add Accommodation Type column with value All

<br />

**a)**

(B6:L6) Year- rename Period and format as required

(A7:A13) Age - rename Scotland as Total, ignore column M - Percentage

Add Sex column with value All

Add Household composition total with value All

Add Ethnicity column with value All

**b)**

(B18:L18) Year- rename Period and format as required

(A19:A21) Gender - rename Sex and change scotland to Total (T | M | F), ignore column M - Percentage

Add Age column with value All

Add Household composition total with value All

Add Ethnicity column with value All

**c)**

(B26:L26) Year- rename Period and format as required

(A27:A35) Household Type - rename Household Composition and change Scotland to Total, ignore column M - Percentage

Add Sex column with value All


Add Age total with value All

Add Ethnicity column with value All

**d)**

(B40:L40) Year- rename Period and format as required

(A41:A52) Ethnicity - change Scotland to Total, ignore column M - Percentage

Add Sex column with value All

Add Household composition total with value All

Add Age column with value All

**Changing Scotland to Total will create duplicates, make sure to remove.**

****

**Sheet: Table 2 Number of Homeslessness applications where rough sleeping occurred prior to Application**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(B5:F7) Rough Sleeping Occurrence:

		All Applications -> Total (can be ignored as in previous dataset)
		At least once during the last 3 months
		The night before
		Of all who slept rough in the last 3 months
		Of all who slept rough the night before
Add Accommodation Type column with value All

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

Add Reason for Application column with value All


Add Failing to Maintain Accommodation Reasons column with value All

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Measure Type column with value Applications and Percentage

Add Unit column with value Count and Percent

**a)**


(A8:14) Age - change Scotland to Total

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**


(A21:A23) Gender - rename Sex and change Scotland to Total

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**


(A30:A38) household type - rename Household Composition and change Scotland to Total

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**


(A45:A56) Ethnicity - change Scotland to Total

Add Age column with value All

Add Household Composition column with value All

Add Sex column with value All

**Changing Scotland to Total will create duplicates, make sure to remove.**

<br />

**Sheet: Table 3: Type of Property where the applicant became homeless/threatened with homelessness**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(A6:A30) Type of Property - change to Accommodation Type and change All to Total

Add Rough Sleeping Occurrence column with value N/A

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Measure Type column with value Applications and Percentage

Add Unit column with value Count and Percent

**a)**

(B5:H5, J5:P5) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B35:D35, F35:H35) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(B65:J65, L65:T65)) Household Type - change to Household Composition and change Scotland to All

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B95:M95, P95:AA95) Ethnicity - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 4: Number of Homelessness applicants formerly in the Armed Services**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(A7:A16) Armed Forces Membership - change All applications to All and Total (Previous member of armed services ) to Total (Ignore All applications row as in other 
tables)

Add Accommodation Type column with value All

Add Rough Sleeping Occurrence column with value N/A

Add Previous Application to LA  column with value N/A

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Measure Type column with value Applications and Percentage

Add Unit column with value Count and Percent

**a)**

(B5:H5) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B20:D20) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**


(B35:J35) Household Type - change to Household Composition and change Scotland to All

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B50:M50) Ethnicity - change Scotland to Total

Add Age column with value All

Add Household Composition column with value All

Add Sex column with value All

****

**Sheet: Table 5: Number of Applicants formerly looked after by the Local Authority**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

Add Armed Forces Membership  column with value N/A

Add Accommodation Type column with value All

Add Rough Sleeping Occurrence column with value N/A

(A7:A17) Previous Application to LA - change All application to Total (Ignore All applications row as in other tables)

Add Reason for Application column with value All

Add Failing to Maintain Accommodation Reasons column with value All

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Measure Type column with value Applications and Percentage

Add Unit column with value Count and Percent

**a)**

(B5:H5) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B21:D21) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(B37:J37) Household Type - change to Household Composition and change Scotland to All

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B53:M53) Ethnicity - change Scotland to Total

Add Age column with value All

Add Household Composition column with value All

Add Sex column with value All

<br />

**Sheet: Table 6 Main reason for making an application for homelessness to a Local Authority**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

Add Accommodation Type column with value All

Add Rough Sleeping Occurrence column with value N/A

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

(A7:A26) Reason for Application (ignore row 6 as data in other tables

		Join A7 to A8, A9, A10, A11, A12, A13, A14, A15, A16, A17, A18

		Join A19 to A20, A21, A22, A23, A24, A25, A26

Add Failing to Maintain Accommodation Reasons column with value All

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Measure Type column with value Applications and Percentage

Add Unit column with value Count and Percent

**a)**



(B5:H5, J5:P5) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B31:D31, F31:H31) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(B56:J56, L56:T56) Household Type - change to Household Composition and change Scotland to All

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B82:M82, P82:AA82) Ethnicity - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All
Add Age column with value All

<br />

**Sheet: Table 7 Reasons for failing to maintain accommodation prior to application**

The following to be added to all 4 tables:
(A1) Year - single value in title, rename Period, reformat as required

Add Accommodation Type column with value All

Add Rough Sleeping Occurrence column with value N/A

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

Add Reason for Application column with value All

(A7:A17) Failing to Maintain Accommodation Reasons

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Measure Type column with value Applications and Percentage

Add Unit column with value Count and Percent

**a)**

(B5:H5, J5:P5) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B22:D22, F22:H22) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(B39:J39, L39:T39) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B56:M56, P56:AA56) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 8 All homelessness assessment decisions**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

Add Accommodation Type column with value All

Add Rough Sleeping Occurrence column with value N/A

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

Add Reason for Application column with value All

(A6:A17) Assessment Decision - change scotland to Total

Add Reassessed as Homeless within same Year column with value N/A

Add Identified Support Need column with value N/A

Add Measure Type column with value Applications and Percentage

Add Unit column with value Count and Percent

**a)**

(B5:H5, J5:P5) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B23:D23, F23:H23) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(B41:J41, L41:T41) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B59:M59, P59:AA59) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 9 Repeated homelessness - Households reassessed as homeless within the same year**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

Add Accommodation Type column with value All

Add Rough Sleeping Occurrence column with value N/A

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

Add Reason for Application column with value All

Add Assessment Decision column with value N/A

(B5:D5) Reassessed as Homeless within same Year

		Total assessed as Homeless or threatened with Homelessness
		Repeat Homelessness Cases
		% of total - change to Repeat Homelessness Cases

Add Identified Support Need column with value N/A

Add Measure Type column with value Households

Add Unit column with value Count and Percent

**a)**

(A6:A12) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A18:A20) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A26:A34) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(A40:A51) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 10 Support needs Identified for those homeless (or threatened with homelessness) households**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

Add Accommodation Type column with value All

Add Rough Sleeping Occurrence column with value N/A

Add Armed Forces Membership column with value N/A

Add Previous Application to LA  column with value N/A

Add Reason for Application column with value All

Add Assessment Decision column with value N/A

Add Reassessed as Homeless within same Year column with value N/A

(A6:A14) Identified Support Need

Add Measure Type column with value Households

Add Unit column with value Count and Percent

**a)**

(B5:H5, J5:P5) Age - change Scotland to All

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B19:D19, F19:H19) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(B34:J34, L34:T34) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B49:M49, P49:AA49) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All


**40 tables can now be joined into 1 dataset**

******

**7 sheets with 52 tables to be joined and dataset ID to be named SG Homelessness Equalities Breakdown - Temporary Accommodation**

**Add to Metadata:**

Entering and exiting statistics are based on counts of unique households entering and exiting temporary accommodation in a given year.
Average stay statistics are based on the average total duration of all individual placements within the same household application.
A household can have multiple applications

**End table structure:**

Period, Age, Sex, Household Type, Ethnicity, Temporary Accommodation Breakdown, Household Composition, Placement Type, Number of Placements, Applications Refused, Measure Type, Unit, Marker, Value

**Sheet: Table 11 Number of Households entering and exiting temporary accommodation by Local Authority**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(B7:E7) Temporary Accommodation Breakdown

		Households entering TA - change to Entering TA
		Households exiting TA - change to Exiting TA 
		% Entering - change to Entering TA
		% Exiting - change to Exiting TA
		Ignore columns G and H
Add Household Composition column with value All

Add Placement Type column with value All

Add Number of Placements column with value N/A

Add Applications Refused column with value N/A

Add Measure Type column with value Households

Add Unit column with value Count and Percent

**a)**

(A8:A15) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A21:A24) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A30:A39) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(A45:A57) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 12 Number of households entering and exiting temporary accommodation, by household type and local authority**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(B9:I9,M9:T9) Household Composition

(B8,M8) Temporary Accommodation Breakdown

		(B8:I8) Entering TA
		(M8:T8) Exiting TA
Add Placement Type column with value All

Add Number of Placements column with value N/A

Add Applications Refused column with value N/A

Add Measure Type column with value Households

Add Unit column with value Count and Percent

**a)**

(A10:A17) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A24:A27) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A33:A42) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(A49:A61) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 13 Number of households entering and exiting temporary accommodation, by placement type and local authority**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(B9:K9,N9:W9) Placement Type

(B8,N8) Temporary Accommodation Breakdown

		(B8:K8) Entering TA
		(N8:W8) Exiting TA
Add Household Composition column with value All

Add Number of Placements column with value N/A

Add Applications Refused column with value N/A

Add Measure Type column with value Households 

Add Unit column with value Count and Percent

**a)**

(A10:A17) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A24:A27) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A33:A42) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(A49:A61) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 14 Average length of time (days) in temporary accommodation (across all placements)**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(B7:L7) Household Composition

		Average for households with children - change to With Children
		Average for households without children - change to Without Children

(B7) Temporary Accommodation Breakdown column with value Average length of Stay

Add Placement Type column with value All

Add Number of Placements column with value N/A

Add Applications Refused column with value N/A

Add Measure Type column with value Households 

Add Unit column with value Days

Ignore columns N, O, P

**a)**

(A8:A15) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A21:A24) Gender- change to Sex and change Scotland to All

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

Ignore this table as it is just comparing the same thing against itself

**d)**

(A45:A57) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 15 Number of temporary accommodation placements**

The following to be added to all 4 tables:
(A1) Year - single value in title, rename Period, reformat as required


(B5:H5, J5:P5) Number of Placements

Add Household Composition column with value All

Add Temporary Accommodation Breakdown column with value Accommodation Placements

Add Placement Type column with value All

Add Applications Refused column with value N/A

Add Measure Type column with value Placements

Add Unit column with value Count

**a)**

(A5:A13) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A19:A22) Gender- change to Sex

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A28:A37) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(A43:A55) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 16 Number of applications that have not been offered accommodation**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(B6:E6) Applications Refused

		% not offered - change to Not Offered 
		Ignore column G

Add Household Composition column with value All

Add Temporary Accommodation Breakdown column with value Accommodation Placements

Add Placement Type column with value All


Add Measure Type column with value Applications

Add Unit column with value Count and Percent

**a)**

(A7:A14) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A19:A22) Gender- change to Sex

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A27:A36) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(A41:A53) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 17 Number of placements that have been in breach of the Unsuitable Accommodation Order**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

Add Applications Refused column with value N/A

Add Household Composition column with value All

(B6:C6, F6,G6) Temporary Accommodation Breakdown 

Breach of the Unsuitable Accommodation Order

Add Placement Type column with value All

Add Measure Type column with value Placements

Add Unit column with value Count and Percent

**a)**

(A7:A13) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A19:A21) Gender- change to Sex 

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A27:A35) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**
(A41:A52) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

******

2 sheets with 8 tables to be joined and dataset ID to be named SG Homelessness Equalities Breakdown - Outcomes

**Add to Metadata:**

Cases assessed as homeless or threatened with homelessness only

**End table structure:**

Period, Age, Sex, Household Type, Ethnicity, Assessment Outcome Type, Post Assessment Contact, Measure Type, Unit, Marker, Value

**Sheet: Table 18 Outcomes for households assessed as unintentionally homeless or threatened with homelessness** 

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

(A7:A16) Assessment Outcome Type - change All

Add Post Assessment Contact column with value N/A

Add Measure Type column with value Households

Add Unit column with value Count and Percent

**a)**

(B6:H6, J6:P6) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(B21:D21, F21:H21) Gender- change to Sex

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(B36:I36, L36:P36) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(B51:M51, O51:Y51) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All

<br />

**Sheet: Table 19 Number of applications where not known or lost contact post-assessment**

The following to be added to all 4 tables:

(A1) Year - single value in title, rename Period, reformat as required

Add Assessment Outcome Type column with value All

(B6:E6) Post Assessment Contact

		Percent where contact was maintained - change to Contact Maintained

Add Placement Type column with value All

Add Measure Type column with value Applications

Add Unit column with value Count and Percent

**a)**

(A7:A13) Age

Add Sex column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**b)**

(A19:A21) Gender- change to Sex 

Add Age column with value All

Add Household Composition column with value All

Add Ethnicity column with value All

**c)**

(A27:A35) Household Type - change to Household Composition

Add Sex column with value All

Add Age column with value All

Add Ethnicity column with value All

**d)**

(A41:A52) Ethnicity 

Add Sex column with value All

Add Household Composition column with value All

Add Age column with value All
