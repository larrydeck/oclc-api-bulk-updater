# if the schemas section of the patron record does not have the wsillinfo namespace, add it
# otherwise, pass the original record -- '.' is the identity filter, it does nothing
if .schemas | index("urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101") == null 
	then 
		.schemas |= . + ["urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101"] 
	else 
		. 
end
|
# if the borrower is CU - Alumni, change their expiration date to 2035-12-31 and change their illPatronType to Alumni
if ."urn:mace:oclc.org:eidm:schema:persona:wmscircpatroninfo:20180101".circulationInfo.borrowerCategory == "CU - Alumni"
	then
		."urn:mace:oclc.org:eidm:schema:persona:persona:20180305".oclcExpirationDate 
			= "2035-12-31T00:00:00Z"
		| ."urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101".illInfo.illPatronType 
			= "Alumni" 
	else
		."urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101".illInfo.illPatronType =
			(."urn:mace:oclc.org:eidm:schema:persona:additionalinfo:20180501".oclcKeyValuePairs[] | select(.key = "customdata1") | .value)
end
# make the ILLId the same as the barcode
| ."urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101".illInfo.illId 
	= ."urn:mace:oclc.org:eidm:schema:persona:wmscircpatroninfo:20180101".circulationInfo.barcode 
# set ILL 'isBlocked' to true and ILL 'isApproved' to false
| ."urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101".illInfo.isBlocked 
	= true 
| ."urn:mace:oclc.org:eidm:schema:persona:wsillinfo:20180101".illInfo.isApproved
	= false