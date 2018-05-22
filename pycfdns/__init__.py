"""
Python module updating Cloudflare DNS records
This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import json
import requests

class CloudflareUpdater:
    """This class is used to update Cloudflare DNS records."""
    BASE_URL = 'https://api.cloudflare.com/client/v4/zones'
    GET_EXT_IP_URL = 'https://api.ipify.org'

    def __init__(self):
        """Initialize"""

    def set_header(self, email, key):
        """Set header data to be used in API calls."""
        headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': key,
        'Content-Type': 'application/json'
        }
        return headers

    def get_zoneID(self, headers, zone):
        """Get the zone id for the zone."""
        zoneIDurl = self.BASE_URL + '?name=' + zone
        zoneIDrequest = requests.get(zoneIDurl, headers=headers)
        zoneID = zoneIDrequest.json()['result'][0]['id']
        return zoneID

    def get_recordInfo(self, headers, zoneID, zone, records):
        """Get the information of the records."""
        if 'None' in records: #If ['None'] in record argument, query all.
            recordQueryEnpoint = '/' + zoneID + '/dns_records&per_page=100'
            recordUrl = self.BASE_URL + recordQueryEnpoint
            recordRequest = requests.get(recordUrl, headers=headers)
            recordResponse = recordRequest.json()['result']
            dev = []
            num = 0
            for value in recordResponse:
                recordName = recordResponse[num]['name']
                dev.append(recordName)
                num = num + 1
            records = dev
        updateRecords = []
        for record in records:
            if zone in record:
                recordFullname = record
            else:
                recordFullname = record + '.' + zone
            recordQuery = '/' + zoneID + '/dns_records?name=' + recordFullname
            recordUrl = self.BASE_URL + recordQuery
            recordInfoRequest = requests.get(recordUrl, headers=headers)
            recordInfoResponse = recordInfoRequest.json()['result'][0]
            recordID = recordInfoResponse['id']
            recordType = recordInfoResponse['type']
            recordProxy = str(recordInfoResponse['proxied'])
            recordContent = recordInfoResponse['content']
            if recordProxy == 'True':
                recordProxied = True
            else:
                recordProxied = False
            updateRecords.append([recordID, recordFullname, recordType,
                recordContent, recordProxied])
        return updateRecords

    def update_records(self, headers, zoneID, updateRecords):
        """Update DNS records."""
        IP = requests.get(self.GET_EXT_IP_URL).text
        message = True
        errorsRecords = []
        sucessRecords = []
        for record in updateRecords:
            updateEndpoint = '/' + zoneID + '/dns_records/' + record[0]
            updateUrl = self.BASE_URL + updateEndpoint
            data = json.dumps({
                'id': zoneID,
                'type': record[2],
                'name': record[1],
                'content': IP,
                'proxied': record[4]
                })
            if record[3] != IP and record[2] == 'A':
                result = requests.put(updateUrl,
                    headers=headers, data=data).json()
                if result['success'] == True:
                    sucessRecords.append(record[1])
                else:
                    errorsRecords.append(record[1])
                if errorsRecords != []:
                    message = ("There was an error updating these records: "
                        + str(errorsRecords) + " , the rest is OK.")
                else:
                    message = ("These records got updated: "
                        + str(sucessRecords))
        return message