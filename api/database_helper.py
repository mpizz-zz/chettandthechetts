from urllib import request, parse
from urllib.error import URLError
import json

BASE_URL = 'http://senior-design.timblin.org'

class DatabaseHelper():

	def register(self, email, password, firstname, lastname):
		endpoint = '/api/register'

		register_request_info = {
			'email': email,
			'password': password,
			'firstname': firstname,
			'lastname': lastname
		}

		# Convert request info (type Dict) to a JSON string
		# The 's' in dumps in json.dumps stands for string
		request_body = json.dumps(register_request_info).encode('utf-8')

		# Post Method is invoked if data != None
		req =  request.Request(BASE_URL + endpoint, data=request_body, headers={'content-type': 'application/json'}, method='POST')

		try:
			# Make the request and save the response into a variable
			resp = request.urlopen(req)

			if resp.getcode() == 200:
				return 'Success'

			# As of now there isn't any other successful codes for this login
			# Success codes range from 100-299
			# If the database API would add more success codes, they would be handled here

		except URLError as e:
			# The server could return several different error codes. These include 401, 404, and 500.
			# 404 shouldn't need to be handled unless the enpoint changes. 401 needs to be handled.
			# A 500 error code will be returned if the database API throws any exception. Therefore, it
			# should be handled gracefully here.
			# Error codes range from 400-599

			if e.code == 401:
				# Verify that 401 is only returned when account already exists.
				return {
					'error_message': 'Error: account already exists for this email.'
				}

			elif e.code == 500:
				return {
					'error_message': 'A server error occurred. If this continues, please contact a system administrator for assistance.'
				}

			else:
				return {
					'error_message': 'An unknown error occurred. If this continues, please contact a system administrator for assistance.'
				}

	def login(self, email, password):
		endpoint = '/api/login'

		login_request_info = {
			'email': email,
			'password': password
		}

		# Convert request info (type Dict) to a JSON string
		# The 's' in dumps in json.dumps stands for string
		request_body = json.dumps(login_request_info).encode('utf-8')

		# Post Method is invoked if data != None
		req =  request.Request(BASE_URL + endpoint, data=request_body, headers={'content-type': 'application/json'}, method='POST')

		try:
			# Make the request and save the response into a variable
			resp = request.urlopen(req)

			if resp.getcode() == 200:
				json_response = json.loads(resp.read().decode('utf8'))
				return {
					'token': json_response['accessToken']
				}

			# As of now there isn't any other successful codes for this login
			# Success codes range from 100-299
			# If the database API would add more success codes, they would be handled here

		except URLError as e:
			# The server could return several different error codes. These include 401, 404, and 500.
			# 404 shouldn't need to be handled unless the enpoint changes. 401 needs to be handled.
			# A 500 error code will be returned if the database API throws any exception. Therefore, it
			# should be handled gracefully here.
			# Error codes range from 400-599

			if e.code == 401:
				return {
					'error_message': 'Login attempt failed. Check your username and password.'
				}

			elif e.code == 500:
				return {
					'error_message': 'A server error occurred. If this continues, please contact a system administrator for assistance.'
				}

			else:
				return {
					'error_message': 'An unknown error occurred. If this continues, please contact a system administrator for assistance.'
				}

	def list_users(self, access_token=None):
		if access_token == None:
			return {
				'error_message': 'Please provide an access token.'
			}

		endpoint = '/api/user?accessToken=' + access_token
		req =  request.Request(BASE_URL + endpoint, method='GET')

		try:
			# Make the request and save the response
			resp = request.urlopen(req)

			if resp.getcode() == 200:
				# Parse JSON response
				json_response = json.loads(resp.read().decode('utf8'))
				return json_response

		except URLError as e:
			# Unauthorized Error
			if e.code == 401:
				return {
					'error_message': 'Invalid access token. Please login again.'
				}
			# Internal Server Error
			elif e.code == 500:
				return {
					'error_message': 'A server error occurred. If this continues, please contact a system administrator for assistance.'
				}
			else:
				return {
					'error_message': 'An unknown error occurred. If this continues, please contact a system administrator for assistance.'
				}

	def create_project(self, owner_id, name, description, due_date):
		endpoint = '/api/project'

		request_info = {
			'owner_id': owner_id,
			'name': name,
			'description': description,
			'due_date': due_date
		}

		request_body = json.dumps(request_info).encode('utf-8')
		req =  request.Request(BASE_URL + endpoint, data=request_body, headers={'content-type': 'application/json'}, method='POST')

		try:
			resp = request.urlopen(req)

			if resp.getcode() == 200:
				return "Success"

		except URLError as e:
			if e.code == 500:
				return {
					'error_message': 'A server error occurred. If this continues, please contact a system administrator for assistance.'
				}
			else:
				return {
					'error_message': 'An unknown error occurred. If this continues, please contact a system administrator for assistance.'
				}

	def get_project(self, project_id, access_token=None):
		endpoint = '/api/project/' + str(project_id) + '?accessToken=' + access_token

		req =  request.Request(BASE_URL + endpoint, method='GET')

		try:
			resp = request.urlopen(req)

			if resp.getcode() == 200:
				json_response = json.loads(resp.read().decode('utf8'))
				return json_response
			else:
				return 'Something went wrong. A project with this id probably doesn\'t exist.'

		except URLError as e:
			if e.code == 401:
				return {
					'error_message': 'Invalid access token. Please login again.'
				}
			elif e.code == 500:
				return {
					'error_message': 'A server error occurred. If this continues, please contact a system administrator for assistance.'
				}
			else:
				return {
					'error_message': 'An unknown error occurred. If this continues, please contact a system administrator for assistance.'
				}

	def delete_project(self, project_id, access_token=None):
		endpoint = '/api/project/' + str(project_id) + '?accessToken=' + access_token

		req =  request.Request(BASE_URL + endpoint, method='DELETE')

		try:
			resp = request.urlopen(req)

			if resp.getcode() == 200:
				return "Project deleted successfully."

		except URLError as e:
			if e.code == 401:
				return {
					'error_message': 'Invalid access token. Please login again.'
				}
			elif e.code == 500:
				return {
					'error_message': 'A server error occurred. If this continues, please contact a system administrator for assistance.'
				}
			else:
				return {
					'error_message': 'An unknown error occurred. If this continues, please contact a system administrator for assistance.'
				}
