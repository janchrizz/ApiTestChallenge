import pytest
import sys
import asyncio

from Modules.api_helper import *
from Modules.api_objects import *
from Modules.utility import *
from Modules.constants import *

#Note: Currently all the API tests are in one file. Obviously when testing gets larger, we want to compartmentalize them into separate files.

def test_delete_workflow_should_not_exist(project_id, project_api_key):
	"""
		This test aims to verify that calling the Delete Workflow endpoint
		with valid parameters should successfully delete it from the system.
		Use Get Specific Workflow to check it no longer exists.
		-Create Workflow
		-Delete Workflow
		-Check if Workflow exists and Verify
		-Cleanup/Delete Workflow
	"""	
	access_token = get_access_token(project_id, project_api_key)

	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Failure with status {res.status_code}"
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now, delete the workflow
		res = delete_workflow(access_token, project_id, workflow_id)
		assert res.status_code == 204, f"Delete Workflow: Failure with status {res.status_code}"

		#Finally, check Get Specific Workflow
		res = get_specific_workflow(access_token, project_id, workflow_id)
		assert res.status_code == 404, f"Get Specific Workflow: Unexpected status code of {res.status_code}"

	finally:
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_delete_workflow_twice(project_id, project_api_key):
	"""
		This test aims to verify that calling the Delete Workflow endpoint
		with valid parameters should successfully delete it from the system.
		Use Get Specific Workflow to check it no longer exists.
		-Create Workflow
		-Delete Workflow
		-Check if Workflow exists and Verify
		-Cleanup/Delete Workflow
	"""	
	access_token = get_access_token(project_id, project_api_key)

	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Failure with status {res.status_code}"
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now, delete the workflow
		res = delete_workflow(access_token, project_id, workflow_id)
		assert res.status_code == 204, f"Delete Workflow: Unexpected status of {res.status_code}"

		#Try to delete the workflow one more time
		res = delete_workflow(access_token, project_id, workflow_id)
		assert res.status_code == 404, f"Delete Non-Existing Workflow: Unexpected status of {res.status_code}"

	finally:
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_add_modis_and_sharpening_tasks_to_workflow_valid(project_id, project_api_key):
	"""
		This test aims to verify the successful response when adding
		valid MODIS and Sharpening tasks to an existing workflow
		-Create Workflow
		-Add Tasks and Verify
		-Cleanup/Delete Workflow
	"""
	access_token = get_access_token(project_id, project_api_key)

	#Construct the request body based on Modis and Sharpening tasks
	task1 = WorkflowTaskRequest('nasa-modis:1', None, NASA_MODIS_BLOCK_ID)
	task2 = WorkflowTaskRequest('sharpening:1', 'nasa-modis:1', SHARPENING_FILTER_BLOCK_ID)
	js1 = json.dumps(task1.__dict__)
	js2 = json.dumps(task2.__dict__)
	task_request_body = json.dumps([task1.__dict__, task2.__dict__])
	
	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Failure with status {res.status_code}"

		#Verify workflow id is returned
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now Add Tasks to Workflow and verify 
		res = add_tasks_to_workflow(access_token, project_id, workflow_id, task_request_body)
		assert res.status_code == 200, f"Add Tasks: Unexpected status code of {res.status_code}"

	finally:
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_add_modis_and_sharpening_tasks_to_workflow_invalid_parentid(project_id, project_api_key):
	"""
		This test aims to verify the 400 Bad Request response when adding
		MODIS and invalid Sharpening tasks parentid to an existing workflow
		-Create Workflow
		-Add Invalid Tasks and Verify Status Code
		-Cleanup/Delete Workflow
	"""
	access_token = get_access_token(project_id, project_api_key)

	#Construct the request body based on Modis and Sharpening tasks
	task1 = WorkflowTaskRequest('nasa-modis:1', None, NASA_MODIS_BLOCK_ID)
	#Set the parentId to NULL for the sharpening
	task2 = WorkflowTaskRequest('sharpening:1', None, SHARPENING_FILTER_BLOCK_ID)
	js1 = json.dumps(task1.__dict__)
	js2 = json.dumps(task2.__dict__)
	task_request_body = json.dumps([task1.__dict__, task2.__dict__])
	
	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Failure with status {res.status_code}"

		#Verify workflow id is returned
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now Add Invalid Task to Workflow and verify 
		res = add_tasks_to_workflow(access_token, project_id, workflow_id, task_request_body)
		assert res.status_code == 400, f"Add Invalid Tasks: Unexpected status code of {res.status_code}"

	finally:
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_create_and_run_modis_sharpening_job_invalid_schema(project_id, project_api_key):
	"""
		This test aims to verify creating and running the MODIS and Sharpening tasks
		but with bad schema payload
		-Create Workflow
		-Add MODIS and Sharpening Tasks
		-Create and Run the Job with invalid payload
		-Cleanup/Delete Workflow
	"""
	access_token = get_access_token(project_id, project_api_key)

	#Construct the request body based on Modis and Sharpening tasks
	task1 = WorkflowTaskRequest('nasa-modis:1', None, NASA_MODIS_BLOCK_ID)
	task2 = WorkflowTaskRequest('sharpening:1', 'nasa-modis:1', SHARPENING_FILTER_BLOCK_ID)
	js1 = json.dumps(task1.__dict__)
	js2 = json.dumps(task2.__dict__)
	task_request_body = json.dumps([task1.__dict__, task2.__dict__])
	
	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow and extract the id returned
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Failure with status {res.status_code}"
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now Add MODIS and Sharpening Tasks to Workflow and verify 
		res = add_tasks_to_workflow(access_token, project_id, workflow_id, task_request_body)
		assert res.status_code == 200, f"Add Tasks: Unexpected status code of {res.status_code}"

		#Now Create and Run job 
		f = open(MODIS_SHARPENING_TEST_JSON_FILE_INVALID)
		job_request_body = json.load(f)
		res = create_and_run_job_for_workflow(access_token, project_id, workflow_id, job_request_body)
		assert res.status_code == 400, f"Create and Run Invalid Job: Unexpected status code of {res.status_code}"		

	finally:
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_create_and_run_modis_sharpening_job_complete(project_id, project_api_key):
	"""
		This test aims to verify creating and running the MODIS and Sharpening tasks
		as jobs until completion
		-Create Workflow
		-Add MODIS and Sharpening Tasks
		-Create and Run the Job
		-Wait for maximum of 5 minutes until Job Complete
		-Cleanup/Delete Workflow
	"""
	access_token = get_access_token(project_id, project_api_key)

	#Construct the request body based on Modis and Sharpening tasks
	task1 = WorkflowTaskRequest('nasa-modis:1', None, NASA_MODIS_BLOCK_ID)
	task2 = WorkflowTaskRequest('sharpening:1', 'nasa-modis:1', SHARPENING_FILTER_BLOCK_ID)
	js1 = json.dumps(task1.__dict__)
	js2 = json.dumps(task2.__dict__)
	task_request_body = json.dumps([task1.__dict__, task2.__dict__])
	
	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow and extract the id returned
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Failure with status {res.status_code}"
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now Add MODIS and Sharpening Tasks to Workflow and verify 
		res = add_tasks_to_workflow(access_token, project_id, workflow_id, task_request_body)
		assert res.status_code == 200, f"Add Tasks: Unexpected status code of {res.status_code}"

		#Now Create and Run job 
		f = open(MODIS_SHARPENING_TEST_JSON_FILE)
		job_request_body = json.load(f)
		res = create_and_run_job_for_workflow(access_token, project_id, workflow_id, job_request_body)
		assert res.status_code == 200, f"Create and Run Job: Unexpected status code of {res.status_code}"
		
		#Extracts job_id
		job_id = res.json()['data']['id']

		#Wait for a maximum of 5 minutes/300 seconds before job is completed
		assert wait_until_job_is_complete(access_token, project_id, job_id, 300) == True, f"Job fails to complete in 300 seconds!"

	finally:
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_create_workflow_with_255_char_name(project_id, project_api_key):
	"""
		This test aims to verify that calling the Create Workflow endpoint
		with valid token, project_id, and a long name in the request (can use max spec length if available)
		successfully returns a 200 status code and returns a workflow_id
	"""	
	access_token = get_access_token(project_id, project_api_key)

	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(255)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Call and verify the status
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Fail to create workflow with 255 char name! System returns status of {res.status_code}"

		#Verify the workflow_id
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

	finally:
		#Attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)
