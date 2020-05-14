**Statutory homelessness in England**

https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness

**Flowchart**

https://gss-cogs.github.io/gss-data-docs/architecture/homelessness/familymappings.html?mhclgtatutoryhomelessnessengland.ttl

This data can be joined up with the dataset MHCLG - Statutory homelessness Detailed local authority-level apart from a few small differences they should have exactly the same format. Some duplication will be caused from this so remove duplicates before outputting to csv. 

Important points from the notes on each sheet need to be added to the metadata.
Remove Rest of England row in all sheets - no geography code for this

**End table structure:**

Period, ONS Geography Code, Duty Type Owed, Initial Assessment, Reason for loss or threat of loss of home, Support needs of household, Accommodation Type, Household Composition, Referral Public Body, Eligibility for Homelessness Status, Measure Type, Unit

<br />
**Sheet: A1 - Number of households by initial assessment of homelessness circumstances and needs**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

Add Duty Type column (Values as below)Add Duty Type Owed column (Values applied as below)

(G5:P5) Initial Assessment: 

		Total Initial Assessments - Duty Type = N/A
		Total owed a prevention of relief duty - Duty Type Owed = Relief
Threatened with homelessness within 56 days - Duty Type = Prevention 

Due to service of valid Section 21 Notice - Duty Type = Prevention

(People are classed as threatened with homelessness) 

Homeless - Duty Type = Relief

Not homeless nor threatened with homelessness within 56 days - Duty Type = No duty owed

Add Reason for loss or threat of loss of home column with value All

Add Support needs of household column with value All

Add Accommodation Type column with value All

Add Household Composition columns with value All

Add Referral Public Body column with value N/A

Add Eligibility for Homelessness Status column with value All

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Sheet: A2 - Number of households owed a homelessness duty by reason for loss, or threat of loss, of last settled home**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

(E3:) Reason for loss or threat of loss of home: 

		E5, V5 to Z5, AL5 to AN5 - use value in cell
		G4 - use value in cell and add G3 to start of string
		I6 to M6 - use value in cell and add G3 and I5 to start of string
		O5 to T5 - use value in cell and add G3 to start of string
AB4 to AE4 - use value in cell and add AB3 to start of string

AG4 to AJ4 - use value in cell and add AG3 to start of string

Add Duty Type column with value All

Add Initial Assessment column column with value all


Add Support needs of household column with value All

Add Accommodation Type column with value All

Add Household Composition columns with value All

Add Referral Public Body column with value N/A

Add Eligibility for Homelessness Status column with value All

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Sheet: A3 - Number of households owed a homelessness duty by support needs of household**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

(E3:AG3) Support needs of household:

 		E3, F3 M3 to AG3 to take value in each cell
		H, I4, J4, K4 should have the following values:
		Total households with support needs
		Households with one support need (Joining of G3 and H4)
		Households with two support needs (joining of G3 and I4)
		Households with three or more support needs (Joining of G3 and J4)
Add Duty Type column with value All

Add Initial Assessment column column with value all

Add Reason for loss or threat of loss of home column with value All

Add Accommodation Type column with value All

Add Household Composition columns with value All

Add Referral Public Body column with value N/A

Add Eligibility for Homelessness Status column with value All

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Sheet: A4 - Number of households owed a homelessness duty by accommodation at time of application**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

(E3) Accommodation type

E3, Q3 to X3, AE3 to take value in cell

G4 toJ4 to have following values:

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
Add Duty Type column with value All

Add Initial Assessment column column with value all

Add Reason for loss or threat of loss of home column with value All

Add Support needs of Household column with value All

Add Household Composition columns with value All

Add Referral Public Body column with value N/A

Add Eligibility for Homelessness Status column with value All

Add Measure Type column with value Households

Add Unit column with values count

<br />

**Sheet: A5P - Number of households owed a prevention duty by household composition
Need to split counts and percentages**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

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
Add Duty Type column with value Prevention

Add Initial Assessment column column with value all

Add Reason for loss or threat of loss of home column with value All

Add Support needs of Household column with value All

Add Accommodation Type columns with value All

Add Referral Public Body column with value N/A

Add Eligibility for Homelessness Status column with value All

Add Measure Type column with value Households

Add Unit column with values count and percentage

<br />

**Sheet: A5R - Number of households owed a relief duty by household composition
Need to split counts and percentages**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

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
Add Duty Type column with value Relief

Add Initial Assessment column column with value all

Add Reason for loss or threat of loss of home column with value All

Add Support needs of Household column with value All

Add Accommodation Type columns with value All

Add Referral Public Body column with value N/A

Add Eligibility for Homelessness Status column with value All

Add Measure Type column with value Households

Add Unit column with value count and percentage

<br />

**Sheet: A7 - Number of households assessed as a result of a referral, including under the Duty to Refer**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

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

<br />

**Sheet: A11 - Number of households owed a homelessness duty by eligibility for homelessness assistance**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

(E3) Eligibility for Homelessness Assistance

		E3, F3, V3 to take cell values
		H4 to M5 to take following values:
			EEA citizen total (joining G3 with H4)
EEA citizen worker (joining G3 with I4)

EEA citizen permanent right to reside (joining G3 with J4)

EEA citizen eligible family member  (joining G3 with K4)

EEA citizen self-employed (joining G3 with L4)

EEA citizen other

		O4 to T4 to take following values:
			Non-UK-EEA citizen total (joining N3 with N4)
Non-UK-EEA citizen indefinite leave to remain (joining N3 with O4)

Non-UK-EEA citizen limited leave to remain (joining N3 with P4)

Non-UK-EEA citizen granted refugee status (joining N3 with Q4)

Non-UK-EEA citizen exceptional leave to remain (joining N3 with R4)

Non-UK-EEA citizen other protection (e.g. humanitarian discretionary) (joining N3 with S4)

Add Duty Type column with value All

Add Initial Assessment column column with value all

Add Reason for loss or threat of loss of home column with value All

Add Support needs of Household column with value All

Add Accommodation Type columns with value All

Add Household Composition columns with value All

Add Referral Public Body column with value N/A

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Tables A1, A2, A3, A4, A5P, A5R, A7 and A11 can now be joined together as one datasets with the name 
MHCLG Homelessness - Households initially assessed as threatened with homelessness (owed prevention duty) or homeless (owed relief duty)**


******

**End table structure:**

Period, ONS Geography code, Reason Duty ended, Duty Type, Accommodation, Measure Type, Unit

**Sheet: P1 - Number of households whose prevention duty ended by reason for duty end**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

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

<br />

**Sheet: P2 - Number of households whose prevention duty ended by type of accommodation secured**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

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

<br />

**Sheet: R1 - Number of households whose relief duty ended by reason for duty end**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

(E3) Reason Duty ended

		E3 to O3 to take value in cells
Add Duty Type column with value Relief

Add Accommodation Type columns with value All

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Sheet: R2 - Number of households whose relief duty ended by type of accommodation secured**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

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
Add Duty Type column with value Relief

Add Reason Duty ended column with value All

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Table P1, P2, R1, R2 can now be joined as one dataset with the name**
MHCLG Homelessness - Households whose Prevention or Relief duty ended by reason and accommodation type


****

**End table structure:**

Period, ONS Geography code, Decision on Duty owed,  Reason for duty end, Priority Need, Measure Type, Unit

**Sheet: MD1 - Number of households by decision on duty owed at end of relief duty**

Add Period column

		Rows 5 to 25 formatted as year/2000
		Rows 27 to 47 formatted as financial year
		Rows 49 to 111 formatted as quarters (Jan to Dec)
Add ONS Geography code column with value E92000001

(A3:O3) Decision on Duty owed

Add Reason for duty end column with value All

Add Priority Need column with value All

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Sheet: MD2 - Number of households whose main duty ended by reason for duty end**

Add Period column

		Rows 4 to 24 formatted as year/2000
		Rows 26 to 46 formatted as financial year
		Rows 48 to 134 formatted as quarters (Jan to Dec)
Add ONS Geography code column with value E92000001

(A3:O3) Reason for duty end

		A3, M3 to Q3 to take value in cell
		G4:H4 to take following values
	   		Housing Act 1996 Pt6 social housing offer Accepted (joined F3 with F4)
			Housing Act 1996 Pt6 social housing offer Refused (joined F3 with G4)
		J4:K4 to take following values
   			Private rented sector offer Accepted (joined I3 with I4)
   			Private rented sector offer Refused (joined I3 with J4)
Add Decision on Duty owed column with value All

Add Priority Need column with value All

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Sheet: MD3 - Number of households owed a main duty by priority need
Need to split counts and percentages**

Add Period column

		Rows 6 to 26 formatted as year/2000
		Rows 28 to 48 formatted as financial year
		Rows 50 to 112 formatted as quarters (Jan to Dec)
Add ONS Geography code column with value E92000001

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

<br />

**Tables MD1, MD2, MD3 can now be added together as one dataset with the name
MHCLG Homelessness - Households assessed, following relief duty end, as unintentionally homeless and priority need (owed main duty)**


****

**Sheet: TA1 - Number of households by type of temporary accommodation provided**

**End table structure:**

Period, ONS Geography code, Accommodation Type, Household Composition, UnitMeasure Type, Unit, Value

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

(E2:AI3) Accommodation Type

		E2 to I2, AF2 to take values in cells
		K3:O3 to take following values:
			B&B hotels total
			B&B hotels total with children
			B&B hotels total with children and resident more than 6 weeks
			B&B hotels total with children and resident more than 6 weeks and pending review or appeal
			B&B hotels total with 16 or 17 year old main applicant 
		Q3:R3 value in cell Q2 with values total and total with children added
		T3:U3 value in cell T2 with values total and total with children added
		W3:X3 value in cell W2 with values total and total with children added
		Z3:AA3 value in cell Z2 with values total and total with children added
		AC3:AD3 value in cell AC2 with values total and total with children added
Add Household Composition column with value all

Add Measure Type column with value Households

Add Unit column with value count

<br />

**Sheet: TA2 - Number of households in temporary accommodation by household composition
Counts and percentages need to be split out**

Add Period column with relevant quarter (Jan to Dec)

Add ONS Geography code column with value E92000001

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

<br />

**Tables TA1 and TA22 can now be joined as one dataset with the name
MHCLG Homelessness - Households in temporary accommodation by household composition and accommodation type**
