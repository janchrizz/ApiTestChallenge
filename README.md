# UP42 API Test Overview

This automation test is written using Python with the PyTest framework that executes several end-to-end test that covers the following:
* Create workflow consisting of specified blocks
* Create and run job based on created workflow
* Monitor job until successful
* Delete created workflow

# Getting the Project
1. Open the command line or terminal
2. Clone this repository using `git clone https://github.com/janchrizz/ApiTestChallenge`

# How to Configure
For this purpose, the only configuration needed to be set up is the config.ini file
1. Open config.ini with any editor
2. Edit project_id value to your project's id
3. Edit project_api_key value to your project's api key value
4. Note: project id and api key correspond to the ids found on the Developer section of UP42 project

# Preconditions
* Python 3 should be installed on the device
* pytest module, use `pip install pytest` on Windows, or check https://docs.pytest.org 
* requests module, use `pip install requests` on Windows, or check https://pypi.org/project/requests/

# Running the Test
1. Open command line or terminal
2. Navigate to the working directory of the test project
3. Run `python -m pytest`