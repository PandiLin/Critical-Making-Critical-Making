import os
import time
from datetime import datetime
from tqdm import tqdm
import subprocess
import sys
from ai_maker import start_manufacture
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_pdf_with_text(file_path, text, font_name="Helvetica", font_size=10, offset=0):
    width, height = A4  # A4 size
    c = canvas.Canvas(file_path, pagesize=A4)
    text_object = c.beginText()
    text_object.setFont(font_name, font_size)
    text_object.setTextOrigin(offset, height - inch)  # Start an inch from the top
    
    # Calculate the available width for text
    available_width = width - 2*offset  # Assuming the same offset for the right margin
    
    # Wrap text to fit within the available width
    from reportlab.lib.utils import simpleSplit
    wrapped_text = []
    for line in text.split('\n'):
        # Split the line into words and recombine them until they exceed the available width
        wrapped_line = simpleSplit(line, font_name, font_size, available_width)
        wrapped_text.extend(wrapped_line)
    
    # Add text to the PDF, creating new pages as necessary
    for line in wrapped_text:
        # Check if we need to start a new page
        if text_object.getY() < inch:  # Less than an inch from the bottom
            c.drawText(text_object)
            c.showPage()  # Start a new page
            text_object = c.beginText()
            text_object.setFont(font_name, font_size)
            text_object.setTextOrigin(offset, height - inch)
        text_object.textLine(line)
    
    # Draw the text on the last page
    c.drawText(text_object)
    c.save()

def print_pdf(file_path, printer_name=None):
    command = ['lpr', file_path]
    if printer_name:
        command += ['-P', printer_name]
    subprocess.run(command)

def print_string_with_lpr(text, printer_name=None, offset=0, font_size=10):
    # Temporary PDF file
    temp_pdf = "temp_print.pdf"
    create_pdf_with_text(temp_pdf, text, font_size=font_size, offset=offset)
    
    # Print the PDF
    print_pdf(temp_pdf, printer_name)
    
    # Optionally, remove the temporary PDF file after printing
    os.remove(temp_pdf)

def rest(minutes):
    for _ in tqdm(range(minutes * 60), desc="Countdown", unit="s", leave=False):
        time.sleep(1)

def start_exec_at(desinated_time):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"Current time: {current_time}")
    if current_time == desinated_time:
        return True
    else:
        return False


def main_loop(rest_time: int):
    last_feedback = ""

    while True:
        print(f"This message is printed every {rest_time} minutes.")
        # Wait for rest_time minutes
        result, last_feedback = start_manufacture(last_feedback)
        print(result)
        print_string_with_lpr(result, font_size=8, offset=20)  # Font size 12, offset 1 inch
        rest(rest_time)

def main(start_execute_time, rest_time):
    try:
        current_time = datetime.now()
        target_time = datetime.strptime(start_execute_time, "%H:%M:%S").replace(year=current_time.year, month=current_time.month, day=current_time.day)
    except ValueError:
        raise ValueError("start_execute_time must be in the format HH:MM:SS")

    while True:
        time_difference = target_time - current_time
        total_seconds = int(time_difference.total_seconds())

        if current_time >= target_time:
            print("Time difference is negative, exiting.")
            break

        # Display countdown
        for _ in tqdm(range(total_seconds), desc="Countdown to start", unit="s", leave=False):
            time.sleep(1)
        break  # Exit the loop when countdown is done

    main_loop(rest_time)


def test_print():
    text_to_print = """Hello, this is a test print.
    This is the second line.
    And this is the third line."""
    offset = 15  # Number of spaces to offset
    print_string_with_lpr(text_to_print,font_size=8, offset=offset)

#TODO: ALARM MODEgi
try:
    start_execute_time = sys.argv[1]
    rest_time = int(sys.argv[2])
    main(start_execute_time, rest_time)
  
except KeyboardInterrupt:
    print("Timer stopped by user.")

# test_print()
