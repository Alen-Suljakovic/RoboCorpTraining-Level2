from robocorp.tasks import task
from robocorp import browser
import time

from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF

@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""
    browser.configure(
        slowmo=100,
    )
    
    open_the_intranet_website()
    log_in()
    export_as_pdf()

def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://mockaroo.com")

def log_in():
    """Fills in the login form and clicks the 'Log in' button"""
    page = browser.page()
    page.click("text=Preview")

def export_as_pdf():
    """Export the data to a pdf file"""
    page = browser.page()
    
    results_html = page.locator(".MuiTable-root") #Crazy workaround
    results_html = page.locator(".MuiDialogContent-root",has=results_html).inner_html()

    pdf = PDF()
    pdf.html_to_pdf(results_html, "output/MockarooTesting.pdf")
