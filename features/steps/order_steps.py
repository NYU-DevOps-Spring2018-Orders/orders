"""
Order Steps

Steps file for orders.feature
"""
from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import server

WAIT_SECONDS = 30
BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@given(u'the following orders')
def step_impl(context):
	headers = {'Content-Type': 'application/json'}
	context.resp = requests.delete(context.base_url + '/orders/reset', headers=headers)
	expect(context.resp.status_code).to_equal(204)
	create_url = context.base_url + '/orders'
	for row in context.table:
		data = {
			"customer_id": row['customer_id'],
			"date":	 row['date'],
			"status": row['status'],
			"items": [{
				"id": row['order_id'],
				"order_id": row['order_id'],
				"product_id": row['product_id'],
				"name":	 row['name'],
				"quantity":	 row['quantity'],
				"price": row['price']
				}]
			}
		payload = json.dumps(data)
		context.resp = requests.post(create_url, data=payload, headers=headers)
		expect(context.resp.status_code).to_equal(201)

@when(u'I visit the "home page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)

@then(u'I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)

@when(u'I visit the "{url}"')
def step_impl(context, url):
    context.resp = requests.get(context.base_url + url)
    assert context.resp.status_code == 200

@then(u'I should see "{message}" in the results')
def step_impl(context, message):
	ensure(message in context.resp.text, True)
