import random
import string

def generate_random_alphanumeric(length):
	result = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(length))
	return result