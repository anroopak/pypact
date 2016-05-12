class VerificationResults(object):


    def VerificationFailed(self, interactions=None):
        interactions = interactions if interactions else ''
        return "Actual interactions do not match expected interactions.\n%s" % interactions


    def VerificationPassed(self):
        return "Iteractions matched."
