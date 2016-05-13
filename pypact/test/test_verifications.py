import pypact


def test_verificationFailed():
    vr = pypact.VerificationResults()
    assert vr.VerificationFailed() is not None


def test_verificationPassed():
    vr = pypact.VerificationResults()

    assert vr.VerificationPassed() is not None
