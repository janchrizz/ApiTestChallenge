import requests
import json
import asyncio
import time

GET_ACCESSTOKEN_URL = 'https://%s:%s@api.up42.com/oauth/token'
CREATE_WORKFLOW_URL = 'https://api.up42.com/projects/%s/workflows'
GET_SPECIFIC_WORKFLOW_URL = 'https://api.up42.com/projects/%s/workflows/%s'
CHECK_JOB_STATUS_URL = 'https://api.up42.com/projects/%s/jobs/%s'
DELETE_WORKFLOW_URL = 'https://api.up42.com/projects/%s/workflows/%s'
ADD_TASK_TO_WORKFLOW_URL = 'https://api.up42.com/projects/%s/workflows/%s/tasks'
CREATE_RUN_JOB_FOR_WORKFLOW_URL = 'https://api.up42.com/projects/%s/workflows/%s/jobs'

def get_access_token(project_id, project_api_key):
	"""
	Retrieves an Access Token from UP42 token endpoint
		Parameters:
			project_id (string): the project id associated to the project on UP42 console developer
			project_api_key (string): the api key associated to the project, obtained from UP42 console developer section

		Returns: 
			The Access Token as a string
	"""
	url = GET_ACCESSTOKEN_URL % (project_id, project_api_key)
	#url = f'https://{project_id}:{project_api_key}@api.up42.com/oauth/token'
	headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
	body = 'grant_type=client_credentials'
	response = requests.post(url, headers=headers, data=body)

	#If for whatever reason, response code is not 200, returns empty string
	if(response.status_code != 200):
		return ''

	#Otherwise, extracts the token
	token = response.json()['data']['accessToken']
	return token

def create_workflow(token, project_id, name, description):
	"""
	Calls the Create Workflow endpoint to create a workflow inside a Project
		Parameters:
			token (string): Access Token associated to the project
			project_id (string): The id associated to the project on UP42 console developer
			name (string): Name of the workflow
			description (string): Description of the workflow

		Returns: 
			The response object 
	"""
	url = CREATE_WORKFLOW_URL % (project_id)
	#url = f'https://api.up42.com/projects/{project_id}/workflows/'
	headers = {'Authorization': f'Bearer {token}', 'Content-Type' : 'application/json'}
	body = {"name": f"{name}", "description": f"{description}"}
	response = requests.post(url, headers=headers, json=body)
	return response

def get_specific_workflow(token, project_id, workflow_id):
	"""
	Calls the Get Specific Workflow endpoint to check if a workflow exists
		Parameters:
			token (string): Access Token associated to the project
			project_id (string): The id associated to the project on UP42 console developer
			workflow_id (string): The id associated to the workflow being queried

		Returns: 
			The response object 
	"""
	url = GET_SPECIFIC_WORKFLOW_URL % (project_id, workflow_id)
	headers = {'Authorization': f'Bearer {token}'}
	response = requests.get(url, headers=headers)
	return response

def check_job_status(token, project_id, job_id):
	"""
	Calls the Check Job Status endpoint to retrieve the status of a job inside a project
		Parameters:
			token (string): Access Token associated to the project
			project_id (string): The id associated to the project on UP42 console developer
			job_id (string): The id associated to the job inside the project

		Returns: 
			The response object 
	"""
	url = CHECK_JOB_STATUS_URL % (project_id, job_id)
	#url = f'https://api.up42.com/projects/{project_id}/jobs/{job_id}'
	headers = {'Authorization': f'Bearer {token}'}
	response = requests.get(url, headers=headers)
	return response

def add_tasks_to_workflow(token, project_id, workflow_id, request_body):
	"""
	Calls the Add Tasks to Workflow endpoint which attempts to add one or more tasks to the workflow inside the project
		Parameters:
			token (string): Access Token associated to the project
			project_id (string): Id associated to the project
			workflow_id (string): Id associated to the workflow inside the project
			request_body (json): Request payload that dictates the type of task(s) intended to be added

		Returns:
			The response object 
	"""
	url = ADD_TASK_TO_WORKFLOW_URL % (project_id, workflow_id)
	headers = {'Authorization': f'Bearer {token}', 'Content-Type' : 'application/json'}
	response = requests.post(url, headers=headers, data=request_body)
	return response

def create_and_run_job_for_workflow(token, project_id, workflow_id, request_body):
	"""
	Calls the Create and Run Job endpoint.
	Attempts to create and run a job for the specified Workflow inside the project.
	The nature of the job is related to the configured task(s) in the Workflow.
		Parameters:
			token (string): Access Token associated to the project
			project_id (string): Id associated to the project
			workflow_id (string): Id associated to the workflow inside the project
			request_body (json): Request payload that dictates the parameter configurations to be executed

		Returns:
			The response object 
	"""
	url = CREATE_RUN_JOB_FOR_WORKFLOW_URL % (project_id, workflow_id)
	headers = {'Authorization': f'Bearer {token}', 'Content-Type' : 'application/json'}
	response = requests.post(url, headers=headers, json=request_body)
	return response

def delete_workflow(token, project_id, workflow_id):
	"""
	Calls the Delete Workflow endpoint to remove an existing workflow from a project
		Parameters:
			token (string): Access Token associated to the project
			project_id (string): Id associated to the project
			workflow_id (string): Id associated to the workflow inside the project

		Returns:
			The response object 
	"""
	url = DELETE_WORKFLOW_URL % (project_id, workflow_id)
	#url = f'https://api.up42.com/projects/{project_id}/workflows/{workflow_id}'
	headers = {'Authorization': f'Bearer {token}'}
	response = requests.delete(url, headers=headers)
	return response