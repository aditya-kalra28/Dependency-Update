# Dependency Update

## Setting Up the Environment

```
git clone https://github.com/aditya-kalra28/Dependency-Update.git
cd Dependency-Update
pip install -r requirements.txt
```

## Create .env file inside the folder

```
USER_NAME = <YOUR_GITHUB_USERNAME>
KEY = <GITHUB_KEY>
```

## Running the Application

```
python .\dyte.py index.csv axios@0.23.0
```

## Using the Update Feature

```
python .\dyte.py index.csv axios@0.23.0 -update
```

## Sample Inputs

### Checking the Version

![2](https://user-images.githubusercontent.com/58948739/171419778-b88b7e1f-9c6c-4b72-8561-9d4f774ace62.PNG)

![1](https://user-images.githubusercontent.com/58948739/171419703-07b7926d-05f0-499f-a293-3bde556e48dd.PNG)


### Updating 

![3](https://user-images.githubusercontent.com/58948739/171419822-cb5b773b-1643-424b-a155-6f5ea5934753.PNG)

![4](https://user-images.githubusercontent.com/58948739/171419845-28624838-4758-47ef-8e24-a60e9ca923e8.PNG)

