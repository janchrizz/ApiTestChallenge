#QA Test Overview

This automation test is written using Python with the PyTest framework that executes a SINGLE end-to-end test that covers the following steps:
* Create workflow consisting of specified blocks
* Create and run job based on created workflow
* Monitor job until successful
* Delete created workflow

#How to get the project
1. sasa

#How to Configure
For this purpose, the only configuration needed to be set up is the config.ini file
1. Open config.ini with any editor
2. Edit project_id value to your project's id
3. Edit project_api_key value to your project's api key value
4. Note: Both project id and api key can be found on UP42 console on the Developer section of your project

#Python Precondition
* Python 3
* pytest module, use pip install pytest on Windows, or check https://docs.pytest.org 
* requests module, use pip install requests on Windows, or check https://pypi.org/project/requests/

#Running the test
1. Open Command Line/Terminal as Administrator
2. Navigate to the working directory of the test project
3. Run python -m pytest