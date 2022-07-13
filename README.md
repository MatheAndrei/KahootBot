# KahootBot

## Requirements
- python 3.10 or greater
- any supported browser: Google Chrome, Firefox, Brave, Microsoft Edge

## Dependencies
- urllib
- json
- selenium v4.3.0

## How to use
0. Download the corresponding webdriver of the used browser (must have the same version as 
the browser). The webdrivers can be found at https://www.selenium.dev/downloads/ in the 
section entitled "Platforms Supported by Selenium". In case of using Brave, you must download 
the ChromeDriver.
1. Fill the properties' value in the _config.txt_ file. The browser name, browser path and 
webdriver path must be provided (specify their absolute path). The browser path can be left 
blank if the browser used is not Brave.
2. Run the _main.py_ script. You'll be asked to enter quiz id (can be taken from the URL), 
game pin and the nickname that will be used in the game.
3. Sit back and enjoy watching the bot competing with the other player!

## Important notes
- the webdriver must have the same version as the browser
- Brave is based on chromium, so the bot must use the ChromeDriver in this case
- specify absolute path in the _config.txt_ file; for Linux users, __~__ cannot be used in path
- the bot only works with public kahoots (otherwise the kahoot data cannot be retrieved)
- the bot will wait for the next quiz if the current quiz's type cannot be handled

## Known issues
- does not work with private kahoots
- does not work with shuffling
- does not work with puzzle quiz
