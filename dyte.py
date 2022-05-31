import argparse
import pandas as pd
import requests
from packaging import version


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
    else:
        versions.append("Module not used in application.")
        version_satisfied.append("-")
print(args.update)
df["version"] = versions
df["version_satisfied"] = version_satisfied
df.to_csv("updated.csv")


