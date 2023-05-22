'''Base Driver Wrapper.'''
from abc import ABC, abstractmethod

class BaseWrapper(ABC):
	'''Abs class for all testing drivers.'''
	gpt_model: str
	verbose: bool = False

	@abstractmethod
	def run(self) -> str:
		'''Run UI Automation Testing With GPT.'''