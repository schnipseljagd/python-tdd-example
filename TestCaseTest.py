class TestFailure:
    def __init__(self, name, error):
        self.name = name
        self.error = error

class TestResult:
    def __init__(self):
        self.runCount = 0
        self.failures = []
    def testStarted(self):
        self.runCount = self.runCount + 1
    def testFailed(self, failure):
        self.failures.append(failure)
    def summary(self):
        return "%d run, %d failed" % (self.runCount, len(self.failures))

class TestCase:
    def __init__(self, name):
        self.name = name
    def run(self, result):
        result.testStarted()
        self.setUp()
        try:
            exec "self." + self.name + "()"
        except Exception as error:
            result.testFailed(TestFailure(self.name, error))
        self.tearDown()
    def setUp(self):
        pass
    def tearDown(self):
        pass

class WasRun(TestCase):
    def setUp(self):
        self.log = ""
        self._appendToLog(self.setUp.__name__)
    def tearDown(self):
        self._appendToLog(self.tearDown.__name__)
    def testMethod(self):
        self._appendToLog(self.testMethod.__name__)
    def testBrokenMethod(self):
        raise Exception
    def _appendToLog(self, message):
        self.log = self.log + message + " "

class TestSuite:
    def __init__(self):
        self.tests = []
    def add(self, test):
        self.tests.append(test)
    def run(self):
        result = TestResult()
        for test in self.tests:
            test.run(result)
        return result

class TestCaseTest(TestCase):
    EXPECTED_LOG = "setUp testMethod tearDown "
    def setUp(self):
        self.result = TestResult()
    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert test.log == self.EXPECTED_LOG
    def testResult(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert self.result.summary() == "1 run, 0 failed"
    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert self.result.summary() == "1 run, 1 failed"
    def testFailedResultFormatting(self):
        self.result.testStarted()
        self.result.testFailed(TestFailure("brokenThing", Exception))
        assert self.result.summary() == "1 run, 1 failed"
    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        self.result = suite.run()
        assert self.result.summary() == "2 run, 1 failed"

suite = TestSuite()
suite.add(TestCaseTest('testTemplateMethod'))
suite.add(TestCaseTest('testResult'))
suite.add(TestCaseTest('testFailedResult'))
suite.add(TestCaseTest('testFailedResultFormatting'))
suite.add(TestCaseTest('testSuite'))
result = suite.run()

for failure in result.failures:
    print failure.name + ": "
    print failure.error
print "---"
print result.summary()
