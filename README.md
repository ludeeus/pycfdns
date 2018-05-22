# A module for updating Cloudflare DNS records.

#### Notes
This has been tested with python 3.6  
This module require a Cloudflare username and API key.  
This module uses these external libararies:
- json
- requests

#### Install
```bash
pip install pycfdns
```

#### Usage:
```python
from pycfdns import CloudflareUpdater

cfupdate = CloudflareUpdater()
email = 'user@example.com'
key = 'fks343489734jkhfsfk387dfjksh78'
zone = 'example.com'
records = ['None']

#Set headers:
headers = cfupdate.set_header(email,key)

#Get zoneID:
zoneID = cfupdate.get_zoneID(headers, zone)

#Get records to update:
updateRecords = cfupdate.get_recordInfo(headers, zoneID, zone, records)

#Update records:
result = cfupdate.update_records(headers, zoneID, updateRecords)

#Print the result:
print(result)
```