class VerificationResults(object):
    def VerificationFailed(self, msg=None):
        if not msg:
            msg = ''
        return 'Actual interactions do not match expected interactions.\n%s' % str(msg)

    def VerificationPassed(self):
        return 'Iteractions matched.'
