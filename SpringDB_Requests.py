#This class should decode JSON data and make the appropriate DB calls
import SpringDB as DB

def new_data(dataMessage):
    jobData = dataMessage.split(',', 1)
    DB.insert_job(jobData[0], jobData[1], jobData[2])
    print("newData")
    # DoSomething