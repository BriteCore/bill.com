"""This is the DTD provided in the Bill.com developer API documentation.
"""

DTD = """
<!ENTITY % BDCID "(#PCDATA)"> <!ENTITY % DATE "(#PCDATA)"> <!--"MM/dd/yy format" --> <!ENTITY % BOOLEAN "(#PCDATA)"> <!-- "0" or "1" --> <!ENTITY % BDC_ENUM_NUM "(#PCDATA)"> <!-- enum number in DBC --> <!ENTITY % DATETIME "(#PCDATA)"> <!--"MM/dd/yy hh:mm a" format -->
<!ELEMENT username ( #PCDATA ) > <!ELEMENT password ( #PCDATA ) > <!ELEMENT orgID %BDCID; > <!ELEMENT sessionId %BDCID; > <!ELEMENT id %BDCID; > <!ELEMENT isActive %BDC_ENUM_NUM; > <!ELEMENT name ( #PCDATA ) > <!ELEMENT shortName ( #PCDATA ) > <!ELEMENT processDate %DATE;> <!ELEMENT amount ( #PCDATA ) > <!ELEMENT amountDue ( #PCDATA ) > <!ELEMENT billId %BDCID; > <!ELEMENT vendorCreditId %BDCID; > <!ELEMENT createdTime %DATETIME; > <!ELEMENT updatedTime %DATETIME; > <!ELEMENT currentTime ( #PCDATA ) >
<!ELEMENT vendorId ( #PCDATA ) > <!ELEMENT taxId ( #PCDATA ) > <!ELEMENT track1099 %BOOLEAN; > <!ELEMENT isToBePrinted %BOOLEAN; > <!ELEMENT isToBeEmailed %BOOLEAN; > <!ELEMENT email ( #PCDATA ) > <!ELEMENT fax ( #PCDATA ) > <!ELEMENT phone ( #PCDATA ) > <!ELEMENT address1 ( #PCDATA ) > <!ELEMENT address2 ( #PCDATA ) > <!ELEMENT address3 ( #PCDATA ) > <!ELEMENT address4 ( #PCDATA ) > <!ELEMENT addressCity ( #PCDATA ) > <!ELEMENT addressState ( #PCDATA ) > <!ELEMENT addressZip ( #PCDATA ) > <!ELEMENT addressCountry ( #PCDATA ) > <!ELEMENT nameOnCheck ( #PCDATA ) > <!ELEMENT accNumber ( #PCDATA ) >
<!--"yyyy-MM-dd'T'HH:mm:ssz" format. Example: "2010-09-23T14:45:34PDT" -->
<!ELEMENT description ( #PCDATA ) > <!ELEMENT vendor_id ( #PCDATA ) >
<!ELEMENT paymentStatus %BDC_ENUM_NUM; > <!ELEMENT creditStatus %BDC_ENUM_NUM; > <!ELEMENT paymentType %BDC_ENUM_NUM; > <!ELEMENT toPrintCheck %BOOLEAN; > <!ELEMENT syncReference ( #PCDATA ) > <!ELEMENT txnNumber ( #PCDATA ) > <!ELEMENT billPayProcessDate %DATE; > <!ELEMENT invoiceNumber ( #PCDATA ) > <!ELEMENT poNumber ( #PCDATA ) > <!ELEMENT refNumber ( #PCDATA ) > <!ELEMENT approvalStatus %BDC_ENUM_NUM; > <!ELEMENT invoiceDate %DATE; >
<!ELEMENT creditDate %DATE; > <!ELEMENT dueDate %DATE; > <!ELEMENT glPostingDate %DATE; > <!ELEMENT integrationId ( #PCDATA ) > <!ELEMENT externalId ( #PCDATA ) > <!ELEMENT lastSyncTime %DATETIME; >
<!ELEMENT accountNumber ( #PCDATA ) > <!ELEMENT accountType %BDC_ENUM_NUM; > <!ELEMENT parentChartOfAccountId %BDCID; >
<!ELEMENT filename ( #PCDATA ) > <!ELEMENT document (#PCDATA) > <!-- document should be base64-encoded -->
<!ELEMENT errormessage ( #PCDATA ) > <!ELEMENT errorcode ( #PCDATA ) > <!ELEMENT status ( #PCDATA ) > <!ELEMENT chartOfAccountId %BDCID; > <!ELEMENT departmentId %BDCID; > <!ELEMENT locationId %BDCID; > <!ELEMENT jobId %BDCID; >
<!ELEMENT jobBillable %BOOLEAN; > <!ELEMENT parentDepartmentId %BDCID; > <!ELEMENT parentJobId %BDCID; > <!ELEMENT parentLocationId %BDCID; > <!ELEMENT allowExport %BOOLEAN; >
<!ELEMENT itemSalesTax %BDCID; <!ELEMENT salesTaxPercentage ( #PCDATA ) > <!ELEMENT terms ( #PCDATA ) > <!ELEMENT FOB ( #PCDATA ) > <!ELEMENT shipDate %DATE; > <!ELEMENT shipMethod ( #PCDATA ) > <!ELEMENT invoiceId %BDCID; > <!ELEMENT itemId %BDCID; > <!ELEMENT quantity ( #PCDATA ) > <!ELEMENT price ( #PCDATA ) > <!ELEMENT serviceDate %DATE; > <!ELEMENT ratePercent ( #PCDATA <!ELEMENT billAddress1 ( #PCDATA <!ELEMENT billAddress2 ( #PCDATA <!ELEMENT billAddress3 ( #PCDATA <!ELEMENT billAddress4 ( #PCDATA ) > <!ELEMENT billAddressCity ( #PCDATA ) > <!ELEMENT billAddressState ( #PCDATA ) >
) > ) > ) > ) >
<!ELEMENT billAddressCountry ( #PCDATA ) > <!ELEMENT billAddressZip ( #PCDATA ) > <!ELEMENT shipAddress1 ( #PCDATA ) > <!ELEMENT shipAddress2 ( #PCDATA ) > <!ELEMENT shipAddress3 ( #PCDATA ) > <!ELEMENT shipAddress4 ( #PCDATA ) > <!ELEMENT shipAddressCity ( #PCDATA ) > <!ELEMENT shipAddressState ( #PCDATA ) > <!ELEMENT shipAddressCountry ( #PCDATA ) > <!ELEMENT shipAddressZip ( #PCDATA ) > <!ELEMENT altPhone ( #PCDATA ) > <!ELEMENT companyName ( #PCDATA ) > <!ELEMENT contactFirstName ( #PCDATA ) > <!ELEMENT contactLastName ( #PCDATA ) > <!ELEMENT paymentDate %DATE;>
<!ELEMENT customerId %BDCID; > <!ELEMENT purDescription ( #PCDATA ) > <!ELEMENT expenseAccount %BDCID; > <!ELEMENT hasPurInfo %BOOLEAN; > <!ELEMENT purCost ( #PCDATA ) > <!ELEMENT salesRep ( #PCDATA ) > <!ELEMENT salesTaxTotal ( #PCDATA ) > <!ELEMENT taxable %BOOLEAN; > <!ELEMENT type %BDC_ENUM_NUM; > <!ELEMENT percentage ( #PCDATA ) > <!ELEMENT parentItemId        %BDCID; > <!ELEMENT lineType %BDC_ENUM_NUM; > <!ELEMENT unitPrice ( #PCDATA ) > <!ELEMENT isOnline %BOOLEAN; > <!ELEMENT depositToAccountId %BDCID; > <!ELEMENT linkTo %BDCID; >
<!ELEMENT convFeeAmount ( #PCDATA ) > <!ELEMENT hasAP %BOOLEAN; > <!ELEMENT hasAR %BOOLEAN; >
<!ELEMENT request (operationbatch | login | operation | logout | getorglist | getcurrenttime | checksyncclientversion)>
<!ATTLIST request version CDATA #REQUIRED> <!-- should be 1.0 or 1.1 (for GMT Dates)--> <!ATTLIST request applicationkey CDATA #REQUIRED> <!ELEMENT getcurrenttime (#PCDATA)> <!ATTLIST getcurrenttime sessionId CDATA #REQUIRED>
<!ELEMENT checksyncclientversion (#PCDATA)> <!-- value of the version--> <!ATTLIST checksyncclientversion sessionId CDATA #REQUIRED> <!ATTLIST checksyncclientversion year CDATA #IMPLIED> <!--"yyyy" format -->
<!ELEMENT login ( username, password, orgID ) > <!-- if you don't know orgID, please use getorglist to get list of orgIDs -->
<!ELEMENT logout (#PCDATA)> <!ATTLIST logout sessionId CDATA #REQUIRED>
<!ELEMENT getorglist ( username, password) >
<!ELEMENT operationbatch (operation+)> <!-- operation batch is series of operations to be executed in one request-->
<!ATTLIST operationbatch sessionId CDATA #REQUIRED> <!-- session Id passed by BDC during login request -->
<!ATTLIST operationbatch transaction CDATA #IMPLIED>
<!-- transaction = "true" means all the operations in this batch will be executed as a single transaction -->
<!ENTITY % LIST_OBJECTS "vendor | bill | vendorCredit | billpay | org_info | chartOfAccount | department | job | location | orgDetail | receivedPay | invoice | customer | item | convFee" >
<!ENTITY % SUPPORTED_OPERATIONS "create_vendor | update_vendor | pay_bill | create_bill | create_vendorcredit | upload_document | upload_attachment | get_list |
create_chartofaccount | update_chartofaccount | create_job | update_job | create_department | update_department | set_external_id | create_offlinepayment | create_location | update_location | set_allow_export | get_org_detail | create_customer | update_customer | update_item | create_item | create_invoice | link_vendor | delink_vendor">
<!ELEMENT operation (%SUPPORTED_OPERATIONS;)> <!ATTLIST operation transactionId CDATA #REQUIRED >
<!-- some string ID to identify this operation --> <!ATTLIST operation sessionId CDATA #IMPLIED>
<!-- need sessionId if this is the only operation; not used in operation batch -->
<!ELEMENT filter ( expression+ ) > <!-- used for get_list to apply filters for returned objects -->
<!ELEMENT expression ( field, operator, value ) > <!ELEMENT field ( #PCDATA ) > <!ELEMENT operator ( #PCDATA ) > <!ELEMENT value ( #PCDATA ) >
<!ELEMENT get_list ( filter ) > <!-- please look at LIST_OBJECTS for supported Object type for get_list -->
<!ELEMENT org_info (orgID, name) >
<!ELEMENT orgDetail (name, address1, address2, address3, address4, addressCity, addressState, addressZip, phone, fax, hasAP, hasAR) >
<!ELEMENT pay_bill ( billId, amount, processDate ) >
<!ELEMENT create_offlinepayment ( billId, amount, processDate, chartOfAccountId?, allowExport?, toPrintCheck?, syncReference?, description?) >
<!ATTLIST get_list object CDATA #REQUIRED > <!-- supported object values vendor, bill, billpay, chartofaccount, department, job,
org_info, location -->
<!ELEMENT vendor (id?, isActive?, vendor_id?, name, taxId?, track1099?, email?, fax?, phone?, address1?, address2?, addressCity, addressState, addressZip,
addressCountry, nameOnCheck, accNumber?, description?, createdTime?, updatedTime?, integrationId?, lastSyncTime?, externalId?, allowExport? )>
<!ELEMENT set_external_id (id, externalId)> <!ELEMENT set_allow_export (id, allowExport)>
<!ELEMENT create_vendor (vendor) > <!ELEMENT update_vendor (vendor) > <!-- id is mandatory for update_vendor -->
<!ELEMENT create_chartofaccount (chartOfAccount) > <!ELEMENT update_chartofaccount (chartOfAccount) > <!-- id is mandatory for update -->
<!ELEMENT create_department (department) > <!ELEMENT update_department (department) > <!-- id is mandatory for update -->
<!ELEMENT create_job (job) > <!ELEMENT update_job (job) > <!-- id is mandatory for update -->
<!ELEMENT create_location (location) > <!ELEMENT update_location (location) > <!-- id is mandatory for update -->
<!ELEMENT billpay (id, billId, name, amount, paymentStatus, description?, billPayProcessDate, txnNumber, createdTime?, updatedTime?,
integrationId?, lastSyncTime?, paymentType, syncReference?, toPrintCheck, chartOfAccountId, externalId?, allowExport)>
<!ELEMENT bill (id?, isActive?, vendorId, invoiceNumber, approvalStatus, paymentStatus, amount, invoiceDate, dueDate, glPostingDate?, description?, createdTime?, updatedTime?, integrationId?, lastSyncTime?, externalId?, allowExport?, billLineItems? )>
<!ELEMENT vendorCredit (id, isActive?, vendorId, refNumber, approvalStatus, creditStatus, amount, creditDate, glPostingDate?, description?, createdTime?,
updatedTime?, integrationId?, lastSyncTime?, externalId?, allowExport?, vendorCreditLineItems? )>
<!ELEMENT billLineItems (billLineItem*) > <!ELEMENT vendorCreditLineItems (vendorCreditLineItem*) >
<!ELEMENT billLineItem (id?, billId?, amount, chartOfAccountId?, departmentId?, locationId?, jobId?, customerId?, jobBillable?, description?, createdTime?, updatedTime?, integrationId?,
lastSyncTime?, externalId?, lineType?, itemId?, quantity?, unitPrice? )> <!ELEMENT vendorCreditLineItem (id, vendorCreditId, amount, chartOfAccountId?,
departmentId?, locationId?, jobId?, jobBillable?, description?, createdTime?, updatedTime?, integrationId?, lastSyncTime?, externalId? )>
<!ELEMENT create_bill (bill) > <!ELEMENT create_vendorcredit (vendorCredit) > <!ELEMENT chartOfAccount (id?, isActive?, name, accountNumber, accountType, description?,
parentChartOfAccountId, createdTime?, updatedTime?, integrationId?, lastSyncTime?, externalId?, allowExport? )>
<!ELEMENT department (id?, isActive?, name,     description?, parentDepartmentId, createdTime?, updatedTime?, integrationId?, lastSyncTime?,
<!ELEMENT job (id?, isActive?, name, description?, parentJobId, createdTime?, updatedTime?, integrationId?, lastSyncTime?, externalId?, allowExport? )>
<!ELEMENT location (id?, isActive?, name, shortName?, description?, parentLocationId, createdTime?, updatedTime?, integrationId?, lastSyncTime?,
<!ELEMENT loginresult (status, sessionId?, orgID?, errormessage?, errorcode?)> <!ELEMENT logoutresult (status, sessionId?, orgID?, errormessage?, errorcode?)>
externalId?, allowExport? )>
externalId?, allowExport? )>
<!ELEMENT getorglistresult (status, errormessage?, errorcode?, org_info*) > <!ELEMENT applicationkeyerror (errormessage, errorcode)> <!ELEMENT versionerror (errormessage, errorcode)> <!ELEMENT getcurrenttimeresult (currentTime) >
<!ELEMENT checksyncclientversionresult (status, errormessage, errorcode) >
<!ELEMENT customer (id?, isActive?, createdTime?, updatedTime?, name, parentCustomerID?,integrationId?, externalId?, taxId?, billAddress1?, billAddress2?, billAddress3?, billAddress4?,
billAddressCity?, billAddressState?, billAddressCountry?, billAddressZip?, shipAddress1?, shipAddress2?, shipAddress3?, shipAddress4?, shipAddressCity?, shipAddressState?, shipAddressCountry?, shipAddressZip?, email?, phone?, altPhone?, fax?, accNumber?, description?, lastSyncTime?, allowExport?, companyName?, contactFirstName?, contactLastName?)>
<!ELEMENT item (id?, isActive?, type, name, chartOfAccountId?, description?, price?, percentage?, parentItemId?, createdTime?, updatedTime?, integrationId?, externalId?, allowExport?, hasPurInfo?, expenseAccount?, purDescription?, purCost?, taxable?, lastSyncTime?, shortName?)>
<!ELEMENT receivedPay (id,createdTime,updatedTime,customerId,status, paymentDate, amount, depositToAccountId?, paymentType?, isOnline?, description?,
refNumber?,convFeeAmount?, lastSyncTime?,allowExport?, externalId?,
integrationId?, paidTransactions?)> <!ELEMENT paidTransactions (paidTransaction*) >
<!ELEMENT paidTransaction (id, invoiceId, externalId?, amount)>
<!ELEMENT invoice (id?, isActive?, createdTime?, updatedTime?, customerId,jobId?, invoiceNumber, invoiceDate, dueDate, amount?, amountDue?, paymentStatus?,
description?, poNumber?, isToBePrinted?, isToBeEmailed?, itemSalesTax?, salesTaxPercentage?, salesTaxTotal?, terms?, salesRep?, FOB?, shipDate?, shipMethod?, departmentId?, integrationId?, lastSyncTime?, allowExport?, externalId?, invoiceLineItems? )>
<!ELEMENT invoiceLineItems (invoiceLineItem+) > <!ELEMENT invoiceLineItem (id?, createdTime?, updatedTime?, invoiceId, itemId?, quantity?,
amount?, price?, serviceDate?, ratePercent?, departmentId?, description?, taxable?, integrationId?, lastSyncTime?, externalId? )>
<!ELEMENT convFee (id?, createdTime?, refNumber, amount, paymentDate, chartOfAccountId, lastSyncTime?,allowExport?, externalId?, integrationId?,) >
<!ELEMENT create_customer (customer) > <!ELEMENT update_customer (customer) > <!ELEMENT create_item (item) > <!ELEMENT update_item (item) > <!ELEMENT create_invoice (invoice) >
<!ELEMENT upload_document (billId?, filename, document)> <!ELEMENT upload_attachment (id, filename, description?, document)>
<!ELEMENT link_vendor (vendorId, linkTo)> <!ELEMENT delink_vendor (vendorId)>
<!ELEMENT operationresult (loginresult?, status, id?, data?, errormessage?, errorcode?)>
<!ATTLIST operationresult transactionId CDATA #REQUIRED > <!ELEMENT data (%LIST_OBJECTS;)*> <!ELEMENT response (operationbatchresult | loginresult | operationresult | logoutresult |
getorglistresult | getcurrenttimeresult | applicationkeyerror |
versionerror | checksyncclientversionresult)> <!ELEMENT operationbatchresult (loginresult, operationresult*)>
"""
"""This DTD can be used to validate XML that will be sent to Bill.com."""
