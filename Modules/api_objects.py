class WorkflowTaskRequest:
	def __init__(self, name, parentName, blockId):
		self.name = name
		self.parentName = parentName
		self.blockId = blockId