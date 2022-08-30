#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Script to take screenshots of a list of websites using Firefox.
#
# by Psycho (@UDPsycho)
#   Twitter: https://www.twitter.com/UDPsycho
#

import os
import argparse
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException


parser = argparse.ArgumentParser(
  description="Script to take screenshots of a list of websites using Firefox."
)

parser.version = "Simple Web Screenshots v1.0"

group = parser.add_mutually_exclusive_group()

parser.add_argument("-v", "--version", action="version", )

parser.add_argument("-i", type=str, dest="input_file", metavar="<in_file>", required=True,
                    help="input file with a list of http(s) URLs")

parser.add_argument("-o", type=str, dest="output_dir", metavar="<out_dir>", required=False,
                    default="screenshots", help="output directory to save the images")

group.add_argument("-m", type=str, dest="screenshot_mode", required=False, default="visible",
                    choices=["visible", "whole"], help="screenshot mode to use (default visible)")

group.add_argument("-s", type=str, dest="screenshot_size", metavar="<size>", required=False,
                    help="custom screenshot size (AxB)")

parser.add_argument("-w", type=int, dest="timeout", metavar="<time>", required=False, default=10,
                    help="seconds to wait for server response (default 10)")

args = parser.parse_args()


# Read input file
try:
  with open(args.input_file, "r") as URLS:
    urls = URLS.readlines()
    total_urls = len(urls)
except Exception as e:
  print ("File Exception: " + str(e) + ".")
  exit(1)


# Create output directory if it doesn't exist
try:
  args.output_dir = os.getcwd() + "/" + args.output_dir

  if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)
except Exception as e:
  print ("OS Exception: " + str(e) + ".")
  exit(1)


# Extract values of the required dimensions
if args.screenshot_size:
  try:
    width  = args.screenshot_size.split("x")[0]
    height = args.screenshot_size.split("x")[1]
  except Exception as e:
    print ("Image Size Exception: " + str(e) + ".")
    exit(1)


# Configure driver options
try:
  options = webdriver.FirefoxOptions()
  options.headless = True
  driver = webdriver.Firefox(options=options)
  driver.set_page_load_timeout(args.timeout)
  if args.screenshot_size:
    driver.set_window_size(width, height)
except Exception as e:
  print ("WebDriver Exception: " + str(e) + ".")
  exit(1)


# Required for handle errors
reached_error_page = "Reached error page"
malformed_url_error = "Malformed URL"
dismissed_user_prompt_dialog_error = "Dismissed user prompt dialog"
custom_timeout_error = "Timeout error"
FAILED_URLS_FILE = "failed_urls.txt"
failed_urls = []


# Required for color output
RED    = "\033[1;91m"
GREEN  = "\033[1;92m"
YELLOW = "\033[1;93m"
BLUE   = "\033[94m"
RESET  = "\033[0m"


# Take the screenshots
for i, url in enumerate(urls, 1):

  url = url.rstrip()
  domain_name = url[url.find("://")+3:]

  print ("Screenshot {}/{}\t".format(str(i).zfill(2), str(total_urls).zfill(2)), end="")

  try:

    driver.get(url)

    if args.screenshot_mode == "visible":
      # Take screenshot of visible page
      driver.get_screenshot_as_file(args.output_dir+"/"+domain_name+".png")

    else:
      # Take screenshot of the whole/specified dimensions page
      S = lambda X: driver.execute_script("return document.body.parentNode.scroll"+X)
      driver.set_window_size(S("Width"),S("Height"))
      driver.find_element("tag name", "body").screenshot(args.output_dir+"/"+domain_name+".png")

    print ("{}Taken{}\t\t{}".format(GREEN, RESET, domain_name))

  except TimeoutException as e:

    failed_urls.append(url)
    error_msg = custom_timeout_error + ": " + unquote(e.msg) + ". " + url

    print ("{}Skipped{}\t\t{}".format(YELLOW, RESET, error_msg))

  except Exception as e:

    failed_urls.append(url)
    error_msg = unquote(e.msg)

    if reached_error_page in error_msg:
      error_msg = reached_error_page + ": " + error_msg[error_msg.find("&d=")+3:]
    elif dismissed_user_prompt_dialog_error in error_msg:
      error_msg = error_msg + " " + url
    elif malformed_url_error in error_msg:
      error_msg = malformed_url_error + error_msg[error_msg.find(": ")+17:]

    print ("{}Failed{}\t\t{}".format(RED, RESET, error_msg))

driver.quit()


# Save failed/skipped URLs to a file
if failed_urls:
  with open(FAILED_URLS_FILE, "w") as f:
    f.write("\n".join(failed_urls)+"\n")

  print ("\nFailed/Skipped URLs have been saved as {}{}{}".format(BLUE, FAILED_URLS_FILE, RESET))
