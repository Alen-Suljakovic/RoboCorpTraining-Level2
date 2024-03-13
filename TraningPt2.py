from robocorp.tasks import task
from robocorp import browser
import csv
import time
import os
import shutil

from RPA.HTTP import HTTP
from RPA.Archive import Archive
from RPA.PDF import PDF

i = 1



@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""
    browser.configure(
        slowmo=100,
    )
    open_the_intranet_website()
    get_file()
    fill_form_with_csv_data()
    archive_receipts()
    


def open_the_intranet_website():
    """Navigates to the given URL"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    page = browser.page()

def get_file():
    """Gets the cvs file"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def fill_and_submit_form(iteration):
    page = browser.page()
    page.click("text=OK")
    page.select_option("#head", iteration[1])
    page.click("#id-body-"+str(iteration[2]))
    page.fill("input[placeholder='Enter the part number for the legs']", str(iteration[3]))
    page.fill("#address", str(iteration[4]))
    robot_screenshot_and_pdf()
    page.click("#order-another")


def fill_form_with_csv_data():
    """LOADING THE CVS FILE AND FEEDING DATA INTO THE WEBPAGE"""
    with open("orders.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',') #postoji read table from csv :(
        next(csv_reader) #skipping the headers

        for row in csv_reader:
            fill_and_submit_form(row)

def robot_screenshot_and_pdf():
    page = browser.page()
    page.click("#preview")
    page.locator("#robot-preview-image").screenshot(path="output/RobotPicture.png")
    page.click("#order")
    while not page.query_selector("#order-another"):
        page.click("#order")
    

    pdf_value = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(pdf_value, "output/RobotReceipt.pdf")
    image_and_pdf_merge()

def image_and_pdf_merge():
    global i
    pdf = PDF()
    pdf.add_watermark_image_to_pdf("output/RobotPicture.png", "output/RobotReceipt.pdf", "output/RobotReceipt.pdf") 
    newFile = os.path.join("output/Receipts", "RobotReceipt"+str(i)+".pdf")
    os.rename("output/RobotReceipt.pdf", newFile)
    i+=1

def archive_receipts():
    shutil.make_archive("Receipts", 'zip', "output")
