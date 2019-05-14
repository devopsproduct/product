"""
Product Steps

Steps file for Product.feature
"""
from os import getenv
import logging
import json
import requests
import time
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))


@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/products/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/products'
    for row in context.table:
        data = {
            "name": row['name'],
            "category": row['category'],
            "price": row['price'],
            "available": row['available'] in ['True', 'true', '1']
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)

@when('I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    #context.driver.save_screenshot('home_page.png')

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)

@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = 'product_' + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = 'product_' + element_name.lower()
    element = Select(context.driver.find_element_by_id(element_id))
    expect(element.first_selected_option.text).to_equal(text)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute('value')).to_be(u'')

##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@when('I wait "{duration}" seconds')
def step_impl(context, duration):
    secs = int(duration)
    time.sleep(secs)

@then('I should see "{name}" in the results')
def step_impl(context, name):
    # found = WebDriverWait(context.driver, WAIT_SECONDS, 15).until(
    #     expected_conditions.text_to_be_present_in_element(
    #         (By.ID, 'search_results'),
    #         name
    #     )
    # )
    # expect(found).to_be(True)
    element = context.driver.find_element_by_id('search_results')
    expect(element.text).to_contain(name)

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)

@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)
    element = context.driver.find_element_by_id('flash_message')
    expect(element.text).to_contain(message)

##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by 'product_' so the Name field has an id='product_name'
# We can then lowercase the name and prefix with product_ to get the id
##################################################################

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute('value')).to_equal(text_string)
    # found = WebDriverWait(context.driver, WAIT_SECONDS).until(
    #     expected_conditions.text_to_be_present_in_element_value(
    #         (By.ID, element_id),
    #         text_string
    #     )
    # )
    # expect(found).to_be(True)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    # element = WebDriverWait(context.driver, WAIT_SECONDS).until(
    #     expected_conditions.presence_of_element_located((By.ID, element_id))
    # )
    element.clear()
    element.send_keys(text_string)

# @when('I change "{key}" to "{value}"')
# def step_impl(context, key, value):
#     context.data[key] = value

# @then('I should see "{message}" in "{field}"')
# def step_impl(context, message, field):
#     """ Check a field for text """
#     element = context.driver.find_element_by_id(field)
#     assert message in element.text

##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    # element = WebDriverWait(context.driver, WAIT_SECONDS).until(
    #     expected_conditions.presence_of_element_located((By.ID, element_id))
    # )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

# https://www.guru99.com/handling-dynamic-selenium-webdriver.html
@when('I copy column "{col}" and row "{row}"')
def step_impl(context, col, row):
    column = col
    row = str(int(row) + 1)
    table_path = '//*[@id="search_results"]/tr['+row+']/td['+col+']'
    element = context.driver.find_element(By.XPATH, table_path)
    context.clipboard = element.text
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = 'product_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    # element = WebDriverWait(context.driver, WAIT_SECONDS).until(
    #     expected_conditions.presence_of_element_located((By.ID, element_id))
    # )
    element.clear()
    element.send_keys(context.clipboard)
