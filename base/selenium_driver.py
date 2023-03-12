import calendar
import logging
import os
import time
import traceback
from traceback import print_stack

from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import utilities.custom_logger as cl


class SeleniumDriver():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except:
            self.log.error("### Exception Occurred when taking screenshot")
            print_stack()

    def getTitle(self):
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType +
                          " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
        except:
            self.log.info("Element not found with locator: " + locator +
                          " and locatorType: " + locatorType)
            self.log.error(f"Exception Caught: {traceback.format_exc()}")
            self.log.error("".join(traceback.format_stack()))
        return element

    def getElementList(self, locator, locatorType="id"):
        locatorType = locatorType.lower()
        byType = self.getByType(locatorType)
        elements = self.driver.find_elements(byType, locator)
        if len(elements) == 0:
            self.log.info("Element list NOT FOUND with locator: " + locator +
                          " and locatorType: " + locatorType)
        return elements

    def clickElementFromList(self, listLocator, locatorType="id", position=0):
        locatorType = locatorType.lower()
        byType = self.getByType(locatorType)
        elements = self.driver.find_elements(byType, listLocator)
        if len(elements) == 0:
            self.log.info("Element list NOT FOUND with locator: " + listLocator +
                          " and locatorType: " + locatorType)
        return elements

    def elementClick(self, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
        except:
            self.log.info("Cannot click on the element with locator: " + locator +
                          " locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator="", locatorType="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.send_keys(data)
        except:
            self.log.info("Cannot send data on the element with locator: " + locator +
                          " locatorType: " + locatorType)
            self.log.error(f"Exception Caught: {traceback.format_exc()}")
            self.log.error("".join(traceback.format_stack()))

    def sendKeysWhenReady(self, data, locator="", locatorType="id"):
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout=10,
                                 poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((byType, locator)))
            element.click()
            element.send_keys(data)

            if element.get_attribute("value") != data:
                self.log.debug("Text is not sent by xpath in field so i will try to send string char by char!")
                element.clear()
                for i in range(len(data)):
                    element.send_keys(data[i] + "")
        except:
            self.log.info("Element not appeared on the web page")
            self.log.error(f"Exception Caught: {traceback.format_exc()}")
            self.log.error("".join(traceback.format_stack()))

    def clearField(self, locator="", locatorType="id"):
        element = self.getElement(locator, locatorType)
        element.clear()

    def getText(self, locator="", locatorType="id", element=None, info=""):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementPresent(self, locator="", locatorType="id", element=None):
        try:
            if locator:
                element_list = self.getElementList(locator, locatorType)
            if len(element_list) == 0:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + locatorType)
                return False
        except:
            print("Element not found")
            return False

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        isDisplayed = False
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
            else:
                self.log.info("Element not displayed")
            return isDisplayed
        except:
            print("Element not found")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) == 0:
                self.log.info("Element not present with locator: " + locator +
                              " locatorType: " + str(byType))
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType="xpath",
                       timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element appeared on the web page")
        except:
            self.log.info("Element not appeared on the web page")
            print_stack()
        return element

    def webScroll(self, direction="up"):
        if direction == "up":
            self.driver.execute_script("window.scrollBy(0, -800);")

        if direction == "down":
            self.driver.execute_script("window.scrollBy(0, 800);")

    def SwitchFrameByIndex(self, locator, locatorType="xpath"):
        result = False
        try:
            iframe_list = self.getElementList("//iframe", locatorType="xpath")
            self.log.debug("Length of iframe list: ")
            self.log.debug(str(len(iframe_list)))
            for i in range(len(iframe_list)):
                self.switchToFrame(index=iframe_list[i])
                result = self.isElementPresent(locator, locatorType)
                if result:
                    self.log.debug("iframe index is:")
                    self.log.debug(str(i))
                    break
                self.switchToDefaultContent()
            return result
        except:
            print("iFrame index not found")
            return result

    def switchToFrame(self, id="", name="", index=None):
        if id:
            self.driver.switch_to.frame(id)
        if name:
            self.driver.switch_to.frame(name)
        if index:
            self.driver.switch_to.frame(index)

    def switchToDefaultContent(self):
        self.driver.switch_to.default_content()

    def getElementAttributeValue(self, attribute, element=None, locator="", locatorType="id"):
        if locator:
            element = self.getElement(locator=locator, locatorType=locatorType)
        value = element.get_attribute(attribute)
        return value

    def isEnabled(self, locator, locatorType="id", info=""):
        element = self.getElement(locator, locatorType=locatorType)
        enabled = False
        try:
            attributeValue = self.getElementAttributeValue(element=element, attribute="disabled")
            if attributeValue is not None:
                enabled = element.is_enabled()
            else:
                value = self.getElementAttributeValue(element=element, attribute="class")
                enabled = not ("disabled" in value)
            if enabled:
                self.log.debug("Element :: '" + info + "' is enabled")
            else:
                self.log.debug("Element :: '" + info + "' is not enabled")
        except:
            self.log.error("Element :: '" + info + "' state could not be found")

        return enabled

    def selectDateInCalendar(self, dateElem="", locatorType="id", date=""):
        calendarMo = "//div[@class = 'MuiPickersCalendarHeader-switchHeader']/div"
        calendarNextMo = "//div[@class = 'MuiPickersCalendarHeader-switchHeader']/button[@tabindex = '0']"
        calendarDay = "//button[contains(@class, 'MuiPickersDay-day')]/span/p[text()='"
        # calendarDay = "//*[button[contains(class, 'MuiPickersDay-day')]/span/p[text()='"
        calendarOK = "//button/span[text() = 'OK']"

        self.elementClick(dateElem, locatorType)

        dateSplit = date.split("-")
        mo = calendar.month_name[int(dateSplit[1])]
        txt = self.getElement(calendarMo, "xpath").text

        while (mo not in txt):
            self.elementClick(calendarNextMo, "xpath")
            txt = self.getElement(calendarMo, "xpath").text
        paath = calendarDay + str(int(dateSplit[2])) + "']/.."
        self.elementClick(paath, "xpath")
        self.elementClick(calendarOK, "xpath")

    def chooseFromSelect(self, selectElem="", locatorType="id", option=""):
        self.elementClick(selectElem, locatorType)
        self.elementClick("//li[@role='option'][text()='" + option + "']", "xpath")
