**Statutory homelessness Detailed local authority-level**

https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness

**Flowchart**

https://gss-cogs.github.io/family-homelessness/datasets/specflowcharts.html?MHCLG-Statutory-homelessness-Detailed-local-authority-level/flowchart.ttl

Important points from the notes on each sheet need to be added to the metadata.

Marker column

		R = Revised Data
		P = Provisional data, to be revised next quarter
		
Remove Rest of England row in all sheets - no geography code for this

&nbsp;

**End table structure:**

Period, ONS Geography Code, Duty Type Owed, Initial Circumstance Assessment, Reason for loss or threat of loss of home, Support needs of household, Accommodation Type, Household Composition, Referral Public Body, Eligibility for Homelessness Status, Measure Type, Unit

The following applies to all sheets

(A) ONS Code - change name to ONS Geography code

(B) Local Authority - Not needed as we have ONS Code

(C) Higher level Local Authority - Not needed as we have ONS Code

(D) Higher level Local Authority code - Not needed as we have ONS Code

(A1) Period: Single value QUARTER as defined in cell

&nbsp;

### Sheet: A1 - Number of households by initial assessment of homelessness circumstances and needs

	Add Duty Type Owed column (Values applied as below)
	(G5:P5) Initial Assessment: (
		Total Initial Assessments - Duty Type = N/A
		Total owed a prevention of relief duty - Duty Type Owed = Relief
	Threatened with homelessness within 56 days - Duty Type = Prevention 
	Due to service of valid Section 21 Notice - Duty Type = Prevention
		(People are classed as threatened with homelessness) 
	Homeless - Duty Type = Relief
	Not homeless nor threatened with homelessness within 56 days - Duty Type = No duty owed
	Number of Households in area (000s) - Duty Type = All
	Households assessed as threatened with homelessness per(000s) - Duty Type = N/A
	Households assessed as homeless per(000s) ) - Duty Type = N/A
	Add Reason for loss or threat of loss of home column with value All
	Add Support needs of household column with value All
	Add Accommodation Type column with value All
	Add Household Composition columns with value All
	Add Referral Public Body column with value N/A
	Add Eligibility for Homelessness Status column with value All
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: A2P & A2R_ - Number of households owed a homelessness duty by reason for loss, or threat of loss, of last settled home

	This is for the 2 sheets mentioned above, one is for Prevention duty and the other is for Relief duty
	(E3:) Reason for loss or threat of loss of home: 

		D5, V5 to Z5, AK5 to AM5 - use value in cell
		F4 - use value in cell and add G3 to start of string
		H6 to L6 - use value in cell and add G3 and I5 to start of string
		O5 to T5 - use value in cell and add G3 to start of string
	AB4 to AE4 - use value in cell and add AB3 to start of string
	AG4 to AJ4 - use value in cell and add AG3 to start of string
	Add Duty Type column with values:
		A2P = Prevention
		A2R_ = Relief
	Add Initial Assessment column column with value all
	Add Support needs of household column with value All
	Add Accommodation Type column with value All
	Add Household Composition columns with value All
	Add Referral Public Body column with value N/A
	Add Eligibility for Homelessness Status column with value All
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: A3 - Number of households owed a homelessness duty by support needs of household

	(E3:AG3) Support needs of household:
	E3, F3 M3 to AG3 to take value in each cell
 	H, I4, J4, K4 should be changed to the following values:
		Total households with support needs
		Households with one support need
		Households with two support needs
		Households with three or more support needs
		
	Add Duty Type column with value All
	Add Initial Assessment column column with value all
	Add Reason for loss or threat of loss of home column with value All
	Add Accommodation Type column with value All
	Add Household Composition columns with value All
	Add Referral Public Body column with value N/A
	Add Eligibility for Homelessness Status column with value All
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: A4P & A4R - Number of households owed a homelessness duty by accommodation at time of application

	This is for the 2 sheets mentioned above, one is for Prevention duty and the other is for Relief duty
	(E3) Accomodation type

	E3, Q3 to X3, AE3 to take value in cell

	G4 to J4 to have following values:
  	 	Private rented sector total (joining of F3 and F4)
  	 	Private rented sector self-contained (joining F3 and G4)
  	 	Private rented sector house in multiple occupation joining of F3 and H4)
  	 	Private rented sector lodging (not with friends and family) (joining of F3 and I4)

	L4 to O4 to have following values:
  		Social rented sector total (joining of K3 and K4)
  	 	Social rented sector council tenant (joining of K3 and L4)
  	 	Social rented sector registered provider tenant (joining of K3 and M4)
   	 	Social rented sector supported housing or hostel (joining of K3 and N4)

	Z4 to AC4 to have following values:
  		Homeless on departure from institution total (joining of Y3 and Y4)
  		Homeless on departure from institution custody (Joining of Y3 and Z4)
   		Homeless on departure from institution general hospital (joining of Y3 and AA4)
   		Homeless on departure from institution psychiatric hospital joining of Y3 and AB4)

	Add Duty Type column with values:
		A4P = Prevention
		A4R = Relief
	Add Initial Assessment column column with value all
	Add Reason for loss or threat of loss of home column with value All
	Add Support needs of Household column with value All
	Add Household Composition columns with value All
	Add Referral Public Body column with value N/A
	Add Eligibility for Homelessness Status column with value All
	Add Measure Type column with value Households
	Add Unit column with values count


### Sheet: A5P & A5R - Number of households owed a prevention duty by household composition
	Need to split counts and percentages**

	(E3) Household composition
		E3, V3 to AD3 to take on value in cell
		H4, J4, K4 to have following values:
	   	Single male parent with dependant children (joining of G3 with G4)
	  	 Single female parent with dependant children (joining of G3 with I4)
	   	Single parent with dependant children gender unknown (joining of G3 with K4)
		O4, Q4, S4 to have following values:
	   	Single male adult (joining of N3 with N4)
	   	Single female adult (joining of N3 with P3) 
	   	Single adult gender unknown (joining of N3 with R4)
		
	Add Duty Type column with values:
		A5P = Prevention
		A5R = Relief
	Add Initial Assessment column column with value all
	Add Reason for loss or threat of loss of home column with value All
	Add Support needs of Household column with value All
	Add Accommodation Type columns with value All
	Add Referral Public Body column with value N/A
	Add Eligibility for Homelessness Status column with value All
	Add Measure Type column with value Households
	Add Unit column with values count and percentage

### Sheet: A7 - Number of households assessed as a result of a referral, including under the Duty to Refer

	(E3:T3) Referral Public Body 
	Add Duty Type column with value All
	Add Initial Assessment column column with value all
	Add Reason for loss or threat of loss of home column with value All
	Add Support needs of Household column with value All
	Add Accommodation Type columns with value All
	Add Household Composition columns with value All
	Add Eligibility for Homelessness Status column with value All
	Add Measure Type column with value Households
	Add Unit column with value count

	Tables A1, A2P, A2R, A3, A4P, A4R, A5P, A5R, A7 and A11 can now be joined together as one datasets with the name 
		MHCLG Homelessness - Households initially assessed as threatened with homelessness (owed prevention duty) or homeless (owed relief duty)

********

### End table structure:
### Period, ONS Geography,  Age, Ethnicity, Ethnic Group, Employment Status, Sexual Identification

### Sheet: A6 - Age of main Applicants assessed as owed a prevention or relief duty by local authority

	Ignore percentages
	(A) Geography (Remove Rest of England row as it does not have a geography code)
	(E3:W3) Age (including total and not known)

	Add Duty Type column with value all
	Add Ethnicity column with value total
	Add Ethnic Group column with value total
	Add Employment Status column with value total
	Add Sexual Identification column with value total

	Measure Type = Applicant
	Unit = count

### Sheet A8 -  Ethinicty of main Applicants assessed as owed a prevention or relief duty by local authority

	Ignore percentages
	(A) Geography (Remove Rest of England row as it does not have a geography code)
	(E3:BH3) Ethnicity (including total and not known)
	(E3:BH3) Ethnic Group (including total and not known)

	Add Duty Type column with value all
	Add Age column with value total
	Add Employment Status column with value total
	Add Sexual Identification column with value total

	Measure Type = Applicant
	Unit = count

### Sheet A10 -  Employment Status of main Applicants assessed as owed a prevention or relief duty by local authority

	Ignore percentages
	(A) Geography (Remove Rest of England row as it does not have a geography code)
	(E3:O3) Employment Status (including total and not known)

	Add Duty Type column with value all
	Add Age column with value total
	Add Ethnicity column with value total
	Add Ethnic Group column with value total
	Add Sexual Identification column with value total

	Measure Type = Applicant
	Unit = count

### Sheet A12 -  Number of Households owed homelessness duty by sexual identification of lead applicant

	Ignore percentages
	Period from title
	(A) Geography (Remove Rest of England row as it does not have a geography code)
	(E2:K2) Sexual Identification

	Add Duty Type column with value all
	Add Age column with value total
	Add Ethnicity column with value total
	Add Ethnic Group column with value total
	Add Employment Status column with value total

	Measure Type = Applicant
	Unit = count

	Tables A6, A8, A10, A12 can now be joined with title:
		MHCLG Homelessness - Age, Ethnicity, Employment Status and Sexual Identification of main applicant owed a prevention or relief duty by Local Authority. 
	
	
********

### End table structure:
### Period, ONS Geography, Reason Duty ended, Duty Type,  Accommodation Type, Measure Type, Unit

### Sheet: P1 - Number of households whose prevention duty ended by reason for duty end

	(E3) Reason Duty ended

		E3, K3 to R3 to take values in cells
		G4 to I4 to take following values:
		  Secured accommodation for 6+months total (joined F3 with F4)
	 	  Secured accommodation for 6+months stayed in existing (joined F3 with G4)
 	Secured accommodation for 6+months moved to alternative  (joined F3 with H4)
	Add Duty Type column with value Prevention
	Add Accommodation Type columns with value All
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: P2 - Number of households whose prevention duty ended by type of accommodation secured

	(E3) Accommodation Type
	E3, P3 to T3 to take value in cells
	F4 to I4 to have following values:
		Private rented sector total (joined F3 with F4)
		Private rented sector self-contained (joined F3 with G4 )
	Private rented sector house in multiple occupation (joined F3 with H4 )
	Private rented sector lodging (not with friends and family) (joined F3 with I4) 

	K4 to N4 to have following values:

		Social rented sector total (joined K3 with K4)
		Social rented sector council tenant (joined K3 with L4)
		Social rented sector registered provider tenant (joined K3 with M4)
		Social rented sector supported housing or hostel (joined K3 with N4)
	Add Duty Type column with value Prevention
	Add Reason Duty ended column with value All
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: R1 - Number of households whose relief duty ended by reason for duty end

	(E3) Reason Duty ended
		E3 to O3 to take value in cells
	Add Duty Type column with value Relief
	Add Accommodation Type columns with value All
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: R2 - Number of households whose relief duty ended by type of accommodation secured

	(E3) Accomodation Type
	E3, P3 to T3 to take value in cells
	F4 to I4 to have following values:
		Private rented sector total
		Private rented sector self-contained
	Private rented sector house in multiple occupation
	Private rented sector lodging (not with friends and family)
	K4 to N4 to have following values:
		Social rented sector total
		Social rented sector council tenant
		Social rented sector registered provider tenant
		Social rented sector supported housing or hostel
	Add Duty Type column with value Relief
	Add Reason Duty ended column with value All
	Add Measure Type column with value Households
	Add Unit column with value count

	Table P1, P2, R1, R2 can now be joined as one dataset with the name
		MHCLG Homelessness - Households whose Prevention or Relief duty ended by reason and accommodation type


**********

### End table structure:
	Period, ONS Geography, Decision on Duty owed, Reason for duty end, Priority Need, Measure, Unit

### Sheet: MD1 - Number of households by decision on duty owed at end of relief duty

	(A3:O3) Decision on Duty owed
	Add Reason for duty end column with value All
	Add Priority Need column with value All
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: MD2 - Number of households whose main duty ended by reason for duty end

	(A3:O3) Reason for duty end
	A3, M3 to Q3 to take value in cell
	G4:H4 to take following values
	  	Housing Act 1996 Pt6 social housing offer Accepted (joined F3 with F4)
		Housing Act 1996 Pt6 social housing offer Refused (joined F3 with G4)
	J4:K4 to take following values
  		Private rented sector offer Accepted (joined I3 with I4)
   		Private rented sector offer Refused (joined I3 with J4)
	Add Decision after Relief duty ended column with value All
	Add Priority Need column with value All
	Add Measure Type column with value Households
	Add Unit column with value count


### Sheet: MD3 - Number of households owed a main duty by priority need
	Need to split counts and percentages

	(E3:AA4) Priority Need
		E3, G3, I3, AA3 to take value in cell
	 L4: X4 to take following values:
    	  Household member vulnerable as a result of Total (K33 to K4)
   	  Household member vulnerable as a result of old age (K33 to L4) 
    	  Household member vulnerable as a result of physical disability or ill health (K33 to M4)
    	  Household member vulnerable as a result of mental health problems (K33 to N4)
    	  Household member vulnerable as a result of young applicant  (K33 to O4)
    	  Household member vulnerable as a result of domestic abuse  (K33 to P4)
    	  Household member vulnerable as a result of other reasons (K33 to Q4)
	Add Decision after Relief duty ended column with value All
	Add Reason for duty end column with value All
	Add Measure Type column with value Households
	Add Unit column with value count and percentage


	Tables MD1, MD2, MD3 can now be added together as one dataset with the name
		MHCLG Homelessness - Households assessed, following relief duty end, as unintentionally homeless and priority need (owed main duty)

**********

### End table structure:
	Period, ONS Geography, Accommodation Type, Household Composition , Measure Type, Unit

### Sheet: TA1 - Number of households by type of temporary accommodation provided

	(E2:AI2) Accommodation Type
		All values in Row 2 (Any with nothing in a cell should be N/A)
	(H3:AI3) Household Composition column with value all
		All values in Row 3 (Any with nothing in a cell should be N/A)
	Add Measure Type column with value Households
	Add Unit column with value count

### Sheet: TA2 - Number of households in temporary accommodation by household composition
	Counts and percentages need to be split out

	(E3:Y4) Household Composition

		E3, G3, X3 to take values in cells
		J4 to N4 to have following values:
			Single male parent with dependant children
			Single female parent with dependant children
			Single parent with dependant children gender unknown
	Q4 to U4 to have following values:

			Single male adult
			Single female adult
			Single adult gender unknown
	Add Accommodation Type column with value all

	Add Measure Type column with value Households

	Add Unit column with value count


	Tables TA1 and TA22 can now be joined as one dataset with the name
		MHCLG Homelessness - Households in temporary accommodation by household composition and accommodation type
