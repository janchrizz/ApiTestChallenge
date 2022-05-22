import requests, json, time
from Modules.constants import *

def get_access_token(project_id, project_api_key):
	"""
	Retrieves an Access Token from UP42 token endpoint
		Parameters:
			project_id (string): the project id associated to the project on UP42 console developer
			project_api_key (string): the api key associated to the project, obtained from UP42 console developer section

		Returns: 
			The Access Token as a string
	"""
	url = f'https://{project_id}:{project_api_key}@{BASE_URI}/oauth/token'
	#url = GET_ACCESSTOKEN_URL % (project_id, project_api_key)
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
	url = f'https://{BASE_PROJECT_URI}/{project_id}/workflows'
	#url = CREATE_WORKFLOW_URL % (project_id)
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
	url = f'https://{BASE_PROJECT_URI}/{project_id}/workflows/{workflow_id}'
	#url = GET_SPECIFIC_WORKFLOW_URL % (project_id, workflow_id)
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
	url = f'https://{BASE_PROJECT_URI}/{project_id}/jobs/{job_id}'
	#url = CHECK_JOB_STATUS_URL % (project_id, job_id)
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
	url = f'https://{BASE_PROJECT_URI}/{project_id}/workflows/{workflow_id}/tasks'
	#url = ADD_TASK_TO_WORKFLOW_URL % (project_id, workflow_id)
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
	url = f'https://{BASE_PROJECT_URI}/{project_id}/workflows/{workflow_id}/jobs'
	#url = CREATE_RUN_JOB_FOR_WORKFLOW_URL % (project_id, workflow_id)
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
	url = f'https://{BASE_PROJECT_URI}/{project_id}/workflows/{workflow_id}'
	#url = DELETE_WORKFLOW_URL % (project_id, workflow_id)
	headers = {'Authorization': f'Bearer {token}'}
	response = requests.delete(url, headers=headers)
	return response

def wait_until_job_is_complete(token, project_id, job_id, max_wait_seconds):
	"""
	Periodically checks the job status of an existing Job inside a Project
		Parameters:
			token (string): Access Token associated to the project
			project_id (string): Id associated to the project
			job_id (string): Id associated to the job that is being checked
			max_wait_seconds (int): Maximum amount of time (in seconds) user is willing to wait

		Returns:
			Boolean. True if job is completed in the max time alotted. False if otherwise.
	"""
	is_complete = False
	start_time = time.time()
	try:
		while not (is_complete):
			#Check if elapsed time exceeds max waiting time
			elapsed = time.time() - start_time
			if(elapsed > max_wait_seconds):
				return False

			#Calls the Check Job Status API
			res = check_job_status(token, project_id, job_id)

			#If response body status is SUCCEEDED, job has completed
			if(res.json()['data']['status'] == 'SUCCEEDED'):
				return True

			#Wait 3 seconds before checking again
			time.sleep(3)

	except Exception as e:
		#If any exception is encountered, return False
		print("Wait For Job: Exception Occurs - " + e)
		return False
	return is_complete