# oclc-api-bulk-updater
The beginnings of a generic bulk-updater for assorted OCLC APIs.

The present example updates patron records using the [Identity Management API](https://developer.api.oclc.org/idm), but (almost) the same principles can apply to the Acquisitions APIs ([Purchase Orders](https://developer.api.oclc.org/wms-acq-po) and [Invoices](https://developer.api.oclc.org/wms-acq-invoices)), the [Collection Management API](https://developer.api.oclc.org/wms-collection-management) for LHRs, the [License Management API](https://developer.api.oclc.org/lman) and even, _mutatis mutandis_, the [Metadata API](https://developer.api.oclc.org/wc-metadata#/Bibliographic%20Records/update-bib).


## Prerequisites

You will need:

* A `WSKEY` and associated `secret` for the API you want to use
  * For the Identity Management API, you will have to request a WSKEY by emailing [devnet@oclc.org.](mailto:devnet@oclc.org.) as explained [here](https://www.oclc.org/developer/api/oclc-apis/worldshare-identity-management-api.en.html)
  * For the other APIs, users who have the role [WSKEY Admin](https://help.oclc.org/WorldShare/WorldShare_Admin/Roles/Web_Service_Keys_WSKeys_role) at their institution can request a WSKEY from OCLC through the [online form](https://platform.worldcat.org/wskey/) in the WSKEY Management interface
  * *NOTE:* the method you will use to [_authenticate_](https://www.oclc.org/developer/api/keys/oauth.en.html) when you use an OCLC API depends on the "Application Type" you select in the request form. To use [`client credentials grant`](https://www.oclc.org/developer/api/keys/oauth/client-credentials-grant.en.html) as we do in this application, be sure to choose _"Machine-to-Machine (M2M) App"_ when you request the WSKEY
* The proper `scope` identifier for the API you want to use
  * For the Identity Management API, the scope is `SCIM`
  * For other APIs, the scope names can be found in WSKEY Management record for the WSKEY -- for example, the Collection Management API's scope is `WMS_COLLECTION_MANAGEMENT`
* Your `institution ID`, which can be found using the [WorldCat Registry](https://www.worldcat.org/webservices/registry/Institutions/)
* A `jq` script to control the modifications to the records
  * the [jq Manual](https://stedolan.github.io/jq/manual/) has all the details
* A list of record identifiers
  * for the Identity Management example, this will be a list of `patron barcodes`, one barcode per line, in a file called, e.g., barcodes.txt

## Setup
Install the dependencies that have to be imported:
```
python3 -m pip install .
```
(or you may prefer to install the dependencies manually).

In the root directory, add a file called `.env` with the WSKEY, secret, and institution ID, e.g.:
```
WSKEY=NVuKm3Z...bRty4m
SECRET=MnVZt...3jwkL
INSTID=12345
```





