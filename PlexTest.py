import json
import requests
import datetime
from types import SimpleNamespace

def getMostRecentJobData(jsonData):
    for element in jsonData:
        print(element.workcenterStatus)
        if(element.workcenterStatus == 'Production' or element.workcenterStatus == 'Setup' or element.workcenterStatus == 'Idle'):
            return element
    return "WNIS"

def get_workstationData(workcenterID):
    header = {'Content-Type': 'application/json',
               'X-Plex-Connect-Api-Key': 'sb5GlSUdLsb1DGksq9BPz0wBQwEuKXJp'}

    workcenterEntriesBase = "https://connect.plex.com/production/v1/production-history/workcenter-status-entries"
    partBase = "https://connect.plex.com/mdm/v1/parts/"
    jobBase = "https://connect.plex.com/scheduling/v1/jobs/"

    end = str(datetime.datetime.now()).replace(' ', 'T') + 'Z'
    begin = str((datetime.datetime.now()) - datetime.timedelta(hours=12)).replace(' ', 'T') + 'Z'

    workcenterStr = workcenterEntriesBase + '?beginDate=' + begin + '&endDate=' + end + '&workcenterId=' + workcenterID

    response = requests.get(workcenterStr, headers=header)
    wrksttnData = json.loads(str(response.content)[2:-1], object_hook=lambda d: SimpleNamespace(**d))
    newData = getMostRecentJobData(wrksttnData)
    print(newData)
    partstr = partBase + str(newData.partId)
    response = requests.get(partstr, headers=header)
    partData = json.loads(str(response.content)[2:-1], object_hook=lambda d: SimpleNamespace(**d))
    print(partData)
    jobStr = jobBase + str(newData.jobId)
    response = requests.get(jobStr, headers=header)
    jobData = json.loads(str(response.content)[2:-1], object_hook=lambda d: SimpleNamespace(**d))
    print(jobData)
    return ("{part_id: " + str(partData.id) + ",Job_Id : " + str(newData.jobId) + ", Part_type: " + str(partData.type) +  ",Part_Capactity: " +str(jobData.quantity) + "}")

