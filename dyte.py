import argparse
import os
import pandas as pd
import requests
from packaging import version
import base64
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USER_NAME')
KEY = os.getenv('KEY')


# Function to create pull request.

def create_pull_request(project_name, repo_name, title, description, head_branch, base_branch, git_token):
    git_pulls_api = "https://api.github.com/repos/{0}/{1}/pulls".format(
        project_name,
        repo_name)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    payload = {
        "title": title,
        "body": description,
        "head": head_branch,
        "base": base_branch,
    }

    r = requests.post(
        git_pulls_api,
        headers=headers,
        data=json.dumps(payload))
    # if not r.ok:
    #     print("Request Failed: {0}".format(r.text))


# Function to fork a repository

def create_fork(owner, repo_name, git_token ):
    git_fork_api = "https://api.github.com/repos/{0}/{1}/forks".format(
        owner,
        repo_name)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    

    r = requests.post(
        git_fork_api,
        headers=headers
    )
    # if not r.ok:
    #     print("Request Failed: {0}".format(r.text))


# Function to add a file to a repository.

def create_file(owner, repo_name, git_token , message, content):
    git_update_api = "https://api.github.com/repos/{0}/{1}/contents/package.json".format(
        owner,
        repo_name)
    headers = {
        "Authorization": "token {0}".format(git_token),
        "Content-Type": "application/json"}

    payload = {
        "message": message,
        "content": content,
    }

    
    r = requests.put(
        git_update_api,
        headers=headers,
        data=json.dumps(payload)
        )
    # if not r.ok:
    #     print("Request Failed: {0}".format(r.text))

# Function to delete a file from a repository

def delete_file(owner, repo_name, git_token , message):
    git_update_api = "https://api.github.com/repos/{0}/{1}/contents/package.json".format(
        owner,
        repo_name
    )
    headers = {
            "Authorization": "token {0}".format(git_token),
            "Content-Type": "application/json"}

    data = requests.get(
        git_update_api,
        headers=headers
    ).json()

    payload = {
        "message": message,
        "sha": data['sha'],
    }


    r = requests.delete(
        git_update_api,
        headers=headers,
        data=json.dumps(payload)
        )
    # if not r.ok:
    #     print("Request Failed: {0}".format(r.text))


# Main program

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help="Enter valid file name.")
parser.add_argument('version', type=str, help="Enter dependency name and version.")
parser.add_argument('-update', action="store_true")

args = parser.parse_args()

df = pd.read_csv(args.file)

name = list(df['name'])
repo = list(df['repo'])

versions = []
version_satisfied = []
update_pr = []

for i in range(len(name)):
    r = requests.get(repo[i].replace("github.com","raw.githubusercontent.com")+"master/package.json").json()

    dependencies = r['dependencies']
    reqd_dependency, reqd_version = args.version.split("@")
    
    if reqd_dependency in dependencies:
        curr_version = dependencies[reqd_dependency]
        if curr_version[0]=="^":
            curr_version = curr_version.strip("^")

        versions.append(curr_version)
        version_satisfied.append(version.parse(reqd_version) <= version.parse(curr_version))
        print(reqd_dependency, reqd_version, curr_version, version.parse(reqd_version) <= version.parse(curr_version))

        if args.update == True and not (version.parse(reqd_version) <= version.parse(curr_version)):
            
            create_fork(
                repo[i].split("/")[3],
                repo[i].split("/")[4],
                KEY
            )

            r['dependencies'][reqd_dependency] = str(reqd_version)
            data = json.dumps(r)
            data = str(base64.b64encode(data.encode('utf-8')))
            data = data[2:len(data)-1]
            
            delete_file(
                USERNAME,
                repo[i].split("/")[4],
                KEY,
                "Delete",
            )

            create_file(
                USERNAME,
                repo[i].split("/")[4],
                KEY,
                "Update package.json",
                data
            )

            create_pull_request(
                repo[i].split("/")[3], # owner
                repo[i].split("/")[4], # repo_name
                "Update "+ reqd_dependency, # title
                "Update" + reqd_dependency + " to " + reqd_version, # description
                USERNAME+":main", # head_branch
                "main", # base_branch
                KEY, # git_token
            )
            webpage = requests.get(repo[i]+"pulls/" + USERNAME)
            parsed = BeautifulSoup(webpage.content, "html5lib")
            link = parsed.select_one(".Box-row a").get('href')
            update_pr.append("https://github.com" + link)
        else:
            update_pr.append(" ")
    else:
        versions.append("Module not used in application.")
        version_satisfied.append("-")
        update_pr.append(" ")
        print("Module not used in application.")
df["version"] = versions
df["version_satisfied"] = version_satisfied
df["update_pr"] = update_pr
df.to_csv("updated.csv")


