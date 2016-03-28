class VerificationResults(object):
	

	def VerificationFailed(self):
		return "Actual interactions do not match expected interactions.\n%s"


	def VerificationPassed(self):
		return "Iteractions matched."