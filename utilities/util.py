import logging
import random
import string
import time
import traceback

import utilities.custom_logger as cl


class Util(object):
    log = cl.customLogger(logging.INFO)

    def sleep(self, sec, info=""):
        if info is not None:
            self.log.info("Wait :: '" + str(sec) + "' seconds for " + info)
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    def getAlphaNumeric(self, length, type='letters'):
        alpha_num = ''
        if type == 'lower':
            case = string.ascii_lowercase
        elif type == 'upper':
            case = string.ascii_uppercase
        elif type == 'digits':
            case = string.digits
        elif type == 'mix':
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choice(case) for i in range(length))

    def getUniqueName(self, charCount=10):
        return self.getAlphaNumeric(charCount, 'lower')

    def getUniqueNameList(self, listSize=5, itemLength=None):
        nameList = []
        for i in range(0, listSize):
            nameList.append(self.getUniqueName(itemLength[i]))
        return nameList

    def verifyTextContains(self, actualText, expectedText):
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From Application Web UI --> :: " + expectedText)
        if expectedText.lower() in actualText.lower():
            self.log.info("### VERIFICATION CONTAINS !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT CONTAINS !!!")
            return False

    def verifyTextMatch(self, actualText, expectedText):
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From Application Web UI --> :: " + expectedText)
        if actualText.lower() == expectedText.lower():
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT MATCHED !!!")
            return False

    def verifyListMatch(self, expectedList, actualList):
        return set(expectedList) == set(actualList)

    def verifyListContains(self, expectedList, actualList):
        length = len(expectedList)
        for i in range(0, length):
            if expectedList[i] not in actualList:
                return False
        else:
            return True
