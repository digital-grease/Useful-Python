#website check uses selenium to login to a website, navigate two pages in, and check that two values are present.

1. First, uses base64 encoded credentials 
  * *using keyring library would be a better option, but wasn't a choice at the time*

2. Initializes webdriver and uses CSS selector values to login and navigate

3. Checks that two values exist on destination page, and returns status of their presence.

4. uses taskkill to kill geckodriver and the window it opened
  * *used taskkill instead of built in driver.close() due to known issue in selenium at the time*
