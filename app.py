import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Configure logging (writes logs to console & file)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,  # Change to DEBUG for detailed logs
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler("webdriver.log", mode="a")  # Log file
    ]
)

def setup_remote_webdriver(
    session_name,
    grid_url=None,
    headless=False,
    timeout=30
):
    """Creates a remote Chrome WebDriver session for Selenium Grid.

    Args:
        session_name (str): Name for the test session (for tracking in Grid reports).
        grid_url (str, optional): URL of the Selenium Grid hub. Defaults to environment variable 'SELENIUM_GRID_URL' or 'http://serverpi:4444'.
        headless (bool, optional): Whether to run Chrome in headless mode. Defaults to False.
        timeout (int, optional): Maximum time (seconds) to wait for connection. Defaults to 30.

    Returns:
        WebDriver: A remote WebDriver instance connected to Selenium Grid, or None if failed.
    """

    # Use environment variable if no Grid URL is provided
    if not grid_url:
        grid_url = os.getenv("SELENIUM_GRID_URL", "http://serverpi:4444")

    try:
        options = ChromeOptions()
        options.set_capability('se:name', session_name)

        # Enable headless mode if requested
        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")  # Required for some headless environments
            options.add_argument("--no-sandbox")  # Useful for Dockerized Selenium Grid

        # Set connection timeout
        options.set_capability("timeouts", {"implicit": timeout * 1000})  # Convert to ms

        driver = webdriver.Remote(options=options, command_executor=grid_url)
        logging.info(f"WebDriver session '{session_name}' started successfully on Chrome (Headless={headless}).")
        return driver

    except Exception as e:
        logging.error(f"Failed to start WebDriver session: {e}")
        return None
