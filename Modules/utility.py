import random
import string

def generate_random_alphanumeric(length):
	"""
	Generates a random alphanumeric sequence of a certain length
		Parameters:
			length (int): Intended length of the string

		Returns: 
			A generated string of the specified length	
	"""
	result = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(length))
	return result