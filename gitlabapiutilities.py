import requests
import json
import os

with open('config.json') as json_data:
    config = json.load(json_data)
    json_data.close()

baseUrl = config['gitlabURL'] + 'api/v4/'
basePayload = {'private_token': config['gitlabToken']}

def removeUserFromProject(userId, projectId):
    url = baseUrl + 'projects/' + str(projectId) + '/members/' + userId
    requests.delete(url, params=basePayload)

def getGroupProjects(groupId):
    url = baseUrl + 'groups/' + str(groupId) + '/projects?per_page=100'
    return requests.get(url, params=basePayload)

def getGroupProjectIdByName(groupId, projectName):
    url = baseUrl + 'groups/' + str(groupId) + '/projects'
    projects = requests.get(url, params=addToBasePayload('search', projectName))
    return next((x['id'] for x in projects.json() if x['name'] == projectName), None)

def getProjectUsers(projectId):
    url = baseUrl + 'projects/' + str(projectId) + '/users'
    return requests.get(url, params=basePayload)

def cloneForks(projectId, directory):
    forks = getForks(projectId)
    for fork in forks.json():
        cloneName = generateCloneName(fork)
        clone(fork['ssh_url_to_repo'], cloneName, directory)

def generateCloneName(fork):
        forkId = fork['id']
        users = getProjectUsers(forkId).json()
        cloneName = fork['owner']['username']
        for user in users:
            if user['username'] != fork['owner']['username'] and config['gitlabUsername'] != user['username']:
                cloneName = cloneName + '-' + user['username']
        return cloneName

def clone(projectUrl, cloneName, directory):
    os.chdir(directory)
    os.system('git clone ' + projectUrl + ' ' + cloneName)

def getForks(projectId):
    url = baseUrl + 'projects/' + str(projectId) + '/forks?per_page=100'
    return requests.get(url, params=basePayload)

def getUserId(gitlabUsername):
    url = baseURL + 'users'
    userInfo = requests.get(url, params=addToBasePayload('username', gitlabUsername))
    return userInfo.json()[0]['id']

def getGroupId(groupName):
    url = baseUrl + 'groups'
    groupInfo = requests.get(url, params=addToBasePayload('search', groupName))
    return groupInfo.json()[0]['id']

def addToBasePayload(key, value):
    payload = basePayload.copy()
    payload[key] = value
    return payload