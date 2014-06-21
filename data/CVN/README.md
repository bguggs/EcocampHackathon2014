# Code Violation Notices
A code violation notice is issued when a person has violated one or more codes in the City of Philadelphia or violated one or more Streets Department rules and regulations. A code violation notice (CVN) is a penalty punishable by a fine up to $300.00.

Addresses have been generalized to the hundred-block level (ie. 1234 Market Street becomes 1200 block of Market Street)

Pardon the field names! We were under a time crunch.

### Data Dictionary

| Field | Description  
| ----- | :----------
| FID |  
| Ticket_Num |  Ticket number
| Property_B |  Whether or not the ticket is for a property-based violation (boolean)
| Violation_ | Violation type ID
| Violation1 | Section of Philadelphia Code where violation is defined. Lookup at [phillycode.com](http://phillycode.com/10/10-700/)
| Violatio_1 | Violation description
| Fine_Amoun | Amount of the penalty/fine (max $300.00)
| Warning | Whether or not it was a warning (boolean)
| Vioded | Whether or not it was voided (boolean)
| Date_Added | Date of CVN
| Issued | 
| Comments | Details of violation type
| Evidence_F | Whether or not evidence was found (boolean)
| L_HUNDRED | Numeric portion of hundred-block address
| R_HUNDRED | Numeric portion of hundred-block address
| SEG_ID | Segment ID, which can be used to link to street [centerline](https://github.com/CityOfPhiladelphia/StreetsDept-geodata/tree/master/Streets_Centerline)
| STNAME | Street name portion of hundred-block address
