from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging

def setup_remote_webdriver(session_name, grid_url="http://serverpi:4444"):
    """Creates a remote Chrome WebDriver session for Selenium Grid.

    Args:
        session_name (str): Name for the test session (for tracking in Grid reports).
        grid_url (str, optional): URL of the Selenium Grid hub. Defaults to "http://serverpi:4444".

    Returns:
        WebDriver: A remote WebDriver instance connected to the Selenium Grid.
    """
    try:
        options = ChromeOptions()
        options.set_capability('se:name', session_name) 

        driver = webdriver.Remote(options=options, command_executor=grid_url)
        logging.info(f"WebDriver session '{session_name}' started successfully on Chrome.")
        return driver

    except Exception as e:
        logging.error(f"Failed to start WebDriver session: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    driver = setup_remote_webdriver("TestSession")
    driver.get("http://www.google.com")
    driver.quit()