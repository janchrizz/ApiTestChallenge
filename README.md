# UP42 API Test 

This automation test is written using Python with the PyTest framework that executes several end-to-end test that covers the following:
* Create workflow consisting of specified blocks
* Create and run job based on created workflow
* Monitor job until successful
* Delete created workflow

# Getting the Project
1. Open the command line or terminal
2. Navigate to your intended directory
3. Clone this repository using `git clone https://github.com/janchrizz/ApiTestChallenge`
4. Alternatively, you can download the zip instead

# How to Configure
For this purpose, the only configuration needed to be set up is the config.ini file.
First, you need the project id and the project api key of your associated project from the UP42 console developer section.
1. Open config.ini with any editor
2. Edit **project_id** value to your project's id
3. Edit **project_api_key** value to your project's api key value

<br/>Note: When filling the values, no quotes are needed, for example
<br/>`project_id = abcd123-efg45`

# Preconditions
* Python 3 should be installed on the device
* pytest module, use `pip install pytest` on Windows, or check https://docs.pytest.org 
* requests module, use `pip install requests` on Windows, or check https://pypi.org/project/requests/

# Running the Test
1. Open command line or terminal
2. Navigate to the working directory of the test project (ApiTestChallenge root folder)
3. Run `python -m pytest -rA` to execute the tests and view the results in the console. A short summary of the name of each test and result will be displayed.
<br/> You can also add the `-s` flag to view (if any) stdout of each test
4. To run individual tests, first list the tests available by running 
<br/>`python -m pytest --collect-only`
<br/> Remember the name of the test you want, and run 
<br/>`python -m pytest -k {name_of_test}`

# Quick Overview of the Tests
* **test_delete_workflow_should_not_exist** = Verification that deleting workflow is successful by checking if the workflow still exists
* **test_delete_workflow_twice** = Verification that deleting a workflow twice will result in a 404 the 2nd time
* **test_add_modis_and_sharpening_tasks_to_workflow_valid** = Verification that adding MODIS and Sharpening tasks to workflow result in success code
* **test_add_modis_and_sharpening_tasks_to_workflow_invalid_parentid** = Verification that adding tasks with invalid Sharpening parentid request payload to workflow result in 400 Bad Request
* **test_create_and_run_modis_sharpening_job_invalid_schema** = Verification that trying to create and run job with invalid parameter results in a 400 Bad Request
* **test_create_and_run_modis_sharpening_job_complete** = Full end-to-end verification from workflow creation to the execution of MODIS and Sharpening job, and finally waiting for its completion
* **test_create_workflow_with_255_char_name** = Just a demonstration of a test failure. Attempts to create 255 char workflow name