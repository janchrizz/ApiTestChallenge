import pytest
import sys

from Modules.api_helper import *
from Modules.api_objects import *
from Modules.utility import *

def test_create_workflow_valid(project_id, project_api_key):
	"""
		This test aims to verify that calling the Create Workflow endpoint
		with valid token, project_id, and request should
		successfully return 200 Ok and check if it exists
	"""	
	access_token = get_access_token(project_id, project_api_key)

	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Call and verify the status
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, f"Create Workflow: Status code is {res.status_code}, not 200"

		#Verify the workflow_id
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Calls Get Specific Workflow to check if exists
		res = get_specific_workflow(access_token, project_id, workflow_id)
		assert res.status_code == 200, f"Get Workflow: Status code is {res.status_code}, not 200"

	finally:
		#Attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_create_workflow_with_long_name(project_id, project_api_key):
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

def test_delete_workflow_should_not_exist(project_id, project_api_key):
	"""
		This test aims to verify that calling the Delete Workflow endpoint
		with valid parameters should successfully delete it from the system.
		Use Get Specific Workflow to check it no longer exists.
	"""	
	access_token = get_access_token(project_id, project_api_key)

	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, "Fail to create workflow"
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

def test_add_task_to_workflow_valid(project_id, project_api_key):
	block_id1 = 'ef6faaf5-8182-4986-bce4-4f811d2745e5'
	block_id2 = 'e374ea64-dc3b-4500-bb4b-974260fb203e'
	task1 = WorkflowTaskRequest('nasa-modis:1', None, block_id1)
	task2 = WorkflowTaskRequest('sharpening:1', 'nasa-modis:1', block_id2)

	js1 = json.dumps(task1.__dict__)
	js2 = json.dumps(task2.__dict__)
	task_request_body = json.dumps([task1.__dict__, task2.__dict__])
	
	access_token = get_access_token(project_id, project_api_key)

	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, "Fail to create workflow"
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now Add Tasks to Workflow and verify 
		res = add_tasks_to_workflow(access_token, project_id, workflow_id, task_request_body)
		assert res.status_code == 200, f"Add Tasks: Unexpected status code of {res.status_code}"

	finally:
		pass
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)

def test_create_and_run_job(project_id, project_api_key):

	#Tasks request body
	block_id1 = 'ef6faaf5-8182-4986-bce4-4f811d2745e5'
	block_id2 = 'e374ea64-dc3b-4500-bb4b-974260fb203e'
	task1 = WorkflowTaskRequest('nasa-modis:1', None, block_id1)
	task2 = WorkflowTaskRequest('sharpening:1', 'nasa-modis:1', block_id2)

	js1 = json.dumps(task1.__dict__)
	js2 = json.dumps(task2.__dict__)
	task_request_body = json.dumps([task1.__dict__, task2.__dict__])
	
	access_token = get_access_token(project_id, project_api_key)

	#Initialize workflow info
	workflow_name = generate_random_alphanumeric(5)
	workflow_desc = generate_random_alphanumeric(5)
	workflow_id = ''

	try:
		#Create a workflow
		res = create_workflow(access_token, project_id, workflow_name, workflow_desc)
		assert res.status_code == 200, "Fail to create workflow"
		workflow_id = res.json()['data']['id']
		assert len(workflow_id) > 0, "No workflow id returned!"

		#Now Add Tasks to Workflow and verify 
		res = add_tasks_to_workflow(access_token, project_id, workflow_id, task_request_body)
		assert res.status_code == 200, f"Add Tasks: Unexpected status code of {res.status_code}"

		#Now Create and Run job 
		f = open('TestData/modis_sharpening_job.json')
		job_request_body = json.load(f)
		res = create_and_run_job_for_workflow(access_token, project_id, workflow_id, job_request_body)
		assert res.status_code == 200, f"Create and Run Job: Unexpected status code of {res.status_code}"
		job_id = res.json()['data']['id']

		#Check job status
		res = check_job_status(access_token, project_id, job_id)
		print(res.content)

	finally:
		#No matter if fail or succeed, attempts clean up by deleting the workflow
		res = delete_workflow(access_token, project_id, workflow_id)
		task.cancel()

