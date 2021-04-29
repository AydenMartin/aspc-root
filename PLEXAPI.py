import json
import requests
import datetime
from types import SimpleNamespace
from requests.auth import HTTPBasicAuth

def getMostRecentJobData(jsonData):
    """
    Ensures that the most recent job associated with a workstation is selected

    :return: most recent job, or resurns error if there are no jobs in setup mode associated with given workstation
    """
    for element in jsonData:
        if(element.workcenterStatus == 'Setup'):
            return element
    return "error"

def get_workstationData(workcenterID):
    """
    Makes the needed api calls to get job data for the sensors

    :return: Json string containing the data for the sensots
    """
    header = {'Content-Type': 'application/json',
               'X-Plex-Connect-Api-Key': 'sb5GlSUdLsb1DGksq9BPz0wBQwEuKXJp'}

    # URL bases for the three API calls
    workcenterEntriesBase = "https://connect.plex.com/production/v1/production-history/workcenter-status-entries"
    partBase = "https://connect.plex.com/mdm/v1/parts/"
    jobBase = "https://connect.plex.com/scheduling/v1/jobs/"

    # Get DateTime objects as bookends for 12 hour period prior to the moment of the call
    end = str(datetime.datetime.now()).replace(' ', 'T') + 'Z'
    begin = str((datetime.datetime.now()) - datetime.timedelta(hours=12)).replace(' ', 'T') + 'Z'

    # Build request body to get work center entries for the past 12 hours
    workcenterStr = workcenterEntriesBase + '?beginDate=' + begin + '&endDate=' + end + '&workcenterId=' + workcenterID

    # Send request body and decode result into dictionary for easy field access.
    response = requests.get(workcenterStr, headers=header)
    wrksttnData = json.loads(str(response.content)[2:-1], object_hook=lambda d: SimpleNamespace(**d))

    # Select job that is in setup state
    newData = getMostRecentJobData(wrksttnData)

    # Use partID derived from newData (the job in setup state) to form a request for part info
    partstr = partBase + str(newData.partId)

    # Send request body and decode result into dictionary for easy field access.
    response = requests.get(partstr, headers=header)
    partData = json.loads(str(response.content)[2:-1], object_hook=lambda d: SimpleNamespace(**d))

    # Use jobId from newData (the job in setup state) to form a request for Job info
    jobStr = jobBase + str(newData.jobId)

    # Send request body and decode result into dictionary for easy field access.
    response = requests.get(jobStr, headers=header)
    jobData = json.loads(str(response.content)[2:-1], object_hook=lambda d: SimpleNamespace(**d))

    # form Json with the data needed by leaf node and return
    return ("{part_id: " + str(partData.id) + ",Job_Id : " + str(newData.jobId) + ", Part_type: " + str(partData.type) +  ",Part_Capactity: " +str(jobData.quantity) + "}")


def updateScrap():
    """
    Attempts to update scrap using the old PLEX API, not currently functional

    :return: None
    """
    user = "AutoSpringIIoTWs@plex.com"
    passwrd = "4b04edc-103a-4"
    url = "https://test.cloud.plex.com/api/datasources/10363/execute"
    res = requests.post(url, headers={"Accept": "application/json", "Accept-Encoding": "gzip,deflate",
                                      "Content-Type": "application/json;charset=utf-8"},
                        auth=HTTPBasicAuth(user, passwrd),
                        json={"Inputs": {"Quantity": 0}})
    print("Header: " + str(res.request.headers))
    print("Body: " + str(res.request.body))
    print("Status Code: " + str(res.status_code))
    print("Response Message: " + str(res.json()))
