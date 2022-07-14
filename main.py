# ----------------------------------------------------------------------------------
# Author: Mathe Andrei
#
# Overview: KahootBot is a bot that can play by itself almost any kahoot on www.kahoot.com.
#
# Requirements: python 3.10 or greater, any supported browser (Google Chrome,
# Firefox, Brave, Microsoft Edge)
#
# Dependencies: urllib, json, time, selenium (version 4.3.0)
#
# How to use:
# 0. Download the corresponding webdriver of the used browser (must have the same
# version as the browser). The webdrivers can be found at https://www.selenium.dev/downloads/
# in the section entitled "Platforms Supported by Selenium". In case of using Brave,
# you must download the ChromeDriver.
# 1. Fill the properties' value in the "config.txt" file. The browser name, browser
# path and webdriver path must be provided (specify their absolute path). The browser
# path can be left blank if the browser used is not Brave.
# 2. Run the "main.py" script. You'll be asked to enter the quiz id (can be taken from
# the URL), game pin and the nickname that will be used in the game.
# 3. Sit back and enjoy watching the bot competing with the other players!
#
# Important notes:
# - the webdriver must have the same version as the browser
# - Brave is based on chromium, so the bot must use the ChromeDriver in this case
# - specify absolute paths in the "config.txt" file; for Linux users, "~" cannot be used in path
# - the bot only works with public kahoots (otherwise the kahoot data cannot be retrieved)
# - the bot will wait for the next quiz if the current quiz's type cannot be handled
#
# Known issues:
# - does not work with private kahoots
# - does not work with shuffling
# - does not work with puzzle quiz
# ----------------------------------------------------------------------------------

import urllib.request
import json

import selenium.webdriver.chrome.service
import selenium.webdriver.firefox.service
import selenium.webdriver.edge.service
from selenium import webdriver

from question import *


class Config:
    def __init__(self, config_path):
        self.browser_name = ''
        self.browser_path = ''
        self.driver_path = ''

        with open(config_path, 'r') as file:
            for line in file.readlines():
                line = line.split('=')
                if line[0].strip() == 'browser-name':
                    self.browser_name = line[1].strip().lower()
                elif line[0].strip() == 'browser-path':
                    self.browser_path = line[1].strip()
                elif line[0].strip() == 'webdriver-path':
                    self.driver_path = line[1].strip()

    def validate(self):
        if self.browser_name == '' or self.browser_path == '' or self.driver_path == '':
            raise Exception('Please fill the browser-name, browser-path and driver-path proprieties in \'config.txt\' file!')
        if all(browser != self.browser_name for browser in ('chrome', 'firefox', 'brave', 'edge')):
            raise Exception('Unknown browser name! Choose any of \'chrome\', \'firefox\', \'brave\', \'edge\'!')


def get_kahoot_data(quiz_id):
    url = 'https://play.kahoot.it/rest/kahoots/' + quiz_id
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data


def extract_questions(data):
    questions = {}
    index = 0
    for question in data['questions']:
        type = question['type']
        answer = None
        match type:
            case 'quiz':
                for i, choice in enumerate(question['choices']):
                    if choice['correct'] is True:
                        answer = i
                        break
                questions[index] = Quiz(question['question'], type, answer)
            case 'multiple_select_quiz':
                answer = []
                for i, choice in enumerate(question['choices']):
                    if choice['correct'] is True:
                        answer.append(i)
                questions[index] = MultiSelectQuiz(question['question'], type, answer)
            case 'open_ended':
                answer = question['choices'][0]['answer']
                questions[index] = OpenEnded(question['question'], type, answer)
            case 'slider':
                answer = str(question['choiceRange']['correct'])
                if answer.split('.')[1] == '0':
                    answer = answer.split('.')[0]
                questions[index] = Slider(question['question'], type, answer)
            case 'content':
                continue
            case _:
                questions[index] = Question(None, type, None)
        index += 1
    return questions


def read_quiz_id():
    print('Enter the quiz id!')
    while True:
        quiz_id = input('quiz id: ')
        if quiz_id != '':
            break
        print('Try again!')
    return quiz_id


def read_game_pin():
    print('Enter the game pin!')
    while True:
        game_pin = input('game pin: ')
        if game_pin != '':
            break
        print('Try again!')
    return game_pin


def read_nickname():
    print('Enter nickname!')
    while True:
        nickname = input('nickname: ')
        if nickname != '':
            break
        print('Try again!')
    return nickname


def get_service_and_options(configs):
    service = None
    options = None

    match configs.browser_name:
        case 'chrome':
            service = webdriver.chrome.service.Service(configs.driver_path)
            options = webdriver.ChromeOptions()
        case 'firefox':
            service = webdriver.firefox.service.Service(configs.driver_path)
            options = webdriver.FirefoxOptions()
        case 'brave':
            service = webdriver.chrome.service.Service(configs.driver_path)
            options = webdriver.ChromeOptions()
            options.binary_location = configs.browser_path
        case 'edge':
            service = webdriver.edge.service.Service(configs.driver_path)
            options = webdriver.EdgeOptions()
    return service, options


def main():
    config_path = 'config.txt'
    configs = Config(config_path)
    configs.validate()

    quiz_id = read_quiz_id()
    game_pin = read_game_pin()
    nickname = read_nickname()

    data = get_kahoot_data(quiz_id)
    questions = extract_questions(data)

    service, options = get_service_and_options(configs)
    service.start()
    driver = webdriver.Remote(service.service_url, options=options)
    driver.get('https://kahoot.it/')

    # join game
    game_id_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'gameId')))
    game_id_elem.send_keys(game_pin, Keys.RETURN)
    nickname_elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'nickname')))
    nickname_elem.send_keys(nickname, Keys.RETURN)

    # play game
    for key in questions.keys():
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "countdown")]')))
        questions[key].mark_answer(driver)
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ResultPage")]')))

    # cleanup
    driver.quit()
    service.stop()


if __name__ == '__main__':
    main()
