import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class Question:
    def __init__(self, question, type, answer):
        self._question = question
        self._type = type
        self._answer = answer

    @property
    def question(self):
        return self._question

    @property
    def type(self):
        return self._type

    @property
    def answer(self):
        return self._answer

    def mark_answer(self, driver):
        pass


class Quiz(Question):
    def mark_answer(self, driver):
        while True:
            buttons = driver.find_elements(By.TAG_NAME, 'button')
            if len(buttons) > 0:
                break
        buttons[self._answer].click()


class MultiSelectQuiz(Question):
    def mark_answer(self, driver):
        while True:
            buttons = driver.find_elements(By.TAG_NAME, 'button')
            if len(buttons) > 0:
                break
        submit_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class*="SubmitButton"]')))
        for answer in self._answer:
            buttons[2 * answer].click()
        submit_button.click()


class OpenEnded(Question):
    def mark_answer(self, driver):
        input_field = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
        input_field.send_keys(self._answer, Keys.RETURN)


class Slider(Question):
    def mark_answer(self, driver):
        scroll_container = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="ScrollContainer"]')))
        reference = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p[class*="ValueText"]>span')))
        submit_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="button"]')))
        scroll_container.click()

        ref_val = float(reference.text.replace(" ", ""))

        while True:
            try:
                marker = driver.find_element(By.XPATH, f"//div[starts-with(translate(text(),'\u00a0',''),'{self._answer}')]/parent::div")
                break
            except EC.NoSuchElementException:
                if ref_val < float(self._answer):
                    ActionChains(driver).send_keys(Keys.ARROW_RIGHT * 2).perform()
                else:
                    ActionChains(driver).send_keys(Keys.ARROW_LEFT * 2).perform()
                time.sleep(0.5)

        marker.click()
        time.sleep(1)
        submit_button.click()
