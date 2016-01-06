# original example command curl -u username:password -H 'Content-Type: application/json' -H 'User-Agent: MyApp (yourname@example.com)' -d '{ "name": "My new project!" }' https://basecamp.com/999999999/api/v1/projects.json

import requests
from requests.auth import HTTPBasicAuth
import json
import time

pw = {}
pw['username']='username'
pw['password']='password'
pw['basecampId']='somenumber'

auth=HTTPBasicAuth(pw['username'], pw['password'])
headers = {'User-Agent': 'BasecampExporter Jeremiah@JLMarks.org'}


eps=["/projects.json", "/projects/drafts.json", "/projects/archived.json", "/project_templates.json", "/stars.json", "/people.json", "/groups.json", "/events.json?since=2012-03-24T11:00:00-06:00", "/topics.json", "/topics/archived.json", "/todolists.json", "/todolists/completed.json", "/todolists/trashed.json", "/documents.json", "/calendars.json", "/forwards.json"]

allresults={}
for eachendpoint in eps:
    print eachendpoint
    allresults[eachendpoint] = requests.get('https://basecamp.com/'+pw['basecampId']+'/api/v1'+ eachendpoint, auth=auth, headers=headers)

import csv
# for eachresult in allresults:
#     fname = eachresult.strip('/').replace('/','').replace('=','').replace('?','').replace(':','')
#     fpart = fname[:-5]
#     fdir="C:\\users\\jeremiah.marks\\Desktop\\"
#     with open(fdir+fname, 'wb') as outfile:
#         outfile.write(allresults[eachresult].content)
#     asjson = json.loads(allresults[eachresult].content)
#     thesekeys=set()
#     for eachthing in asjson:
#         for eachkey in eachthing:
#             thesekeys.add(eachkey)
#     with open(fdir+fpart+".csv", 'wb') as csvout:
#         thiswriter = csv.DictWriter(csvout, list(thesekeys))
#         thiswriter.writeheader()
#         for eachotherthing in asjson:
#             thiswriter.writerow(eachotherthing)


class baseCamp(object):
    """baseCamp is the object that acts as the interactor with
    the API. It is here to serve two purposes:
        1. Limit API usage. Initial settings will be set to do
        12 API calls with a 6 second pause.
        2. Because I am too lazy to RTFM regarding how to
        store the headers in a request.
    """
    def __init__(self):
        super(baseCamp, self).__init__()
        self.counter = 1
        self.auth=HTTPBasicAuth(pw['username'], pw['password'])
        self.headers = {'User-Agent': 'BasecampExporter Jeremiah@JLMarks.org'}
        self.baseurl = 'https://basecamp.com/'+pw['basecampId']+'/api/v1'
        self.filepath = "C:\\users\\jeremiah.marks\\Desktop\\basecamp\\"

    def call(self, endpoint=None, url=None, output=None):
        if url:
            callurl=url
        else:
            callurl=self.baseurl+endpoint
        if self.counter%12==0:
            time.sleep(6)
        self.counter+=1
        thereturn=requests.get(callurl, auth=self.auth, headers=self.headers)
        if output:
            with open(self.filepath+output, 'wb') as outfile:
                outfile.write(thereturn.content)
        return thereturn

    def getavatar(self, avatarurl, filename):
        avatar = requests.get(avatarurl)
        with open(self.filepath+filename, 'wb') as outfile:
            outfile.write(avatar.content)

interactor=baseCamp()

projectdata={}
for eachproject in json.loads(allresults["/projects.json"].content):
    projectdata[eachproject['id']] = interactor.call(url=eachproject['url'], output=str(eachproject['id'])+".json")


persondata={}
for eachperson in json.loads(allresults["/people.json"].content):
    personpage=interactor.call(url=eachperson['url'], output='person_'+str(eachperson['id'])+"_"+str(eachperson['identity_id']))
    interactor.getavatar(eachperson['fullsize_avatar_url'], str(eachperson['id'])+'.gif')

groupdata={}
for eachgroup in json.loads(allresults["/groups.json"].content):
    grouppage=interactor.call("/groups/"+str(eachgroup['id']) + ".json", output="group_"+str(eachgroup['id'])+".json")
    groupdata[eachgroup['id']] = grouppage
