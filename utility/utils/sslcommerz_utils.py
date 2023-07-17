from sslcommerz_lib import SSLCOMMERZ
# https://github.com/sslcommerz/SSLCommerz-Python
# https://stackoverflow.com/questions/68275177/how-can-i-integrate-sslcommerze-to-my-django-app
store_id = "devss648fc4dc5dbc0"
store_pass = "devss648fc4dc5dbc0@ssl"
# store_id = "kaaru6464c5db8f379"
# store_pass = "kaaru6464c5db8f379@ssl"
sslcz = SSLCOMMERZ({ 'store_id': store_id, 'store_pass': store_pass, 'issandbox': True })

data = {
    'total_amount': "100.26",
    'currency': "BDT",
    'tran_id': "tran_12345",
    'success_url': "http://127.0.0.1:8000/payment-successful", # if transaction is succesful, user will be redirected here
    'fail_url': "http://127.0.0.1:8000/payment-failed", # if transaction is failed, user will be redirected here
    'cancel_url': "http://127.0.0.1:8000/payment-cancelled", # after user cancels the transaction, will be redirected here
    'emi_option': "0",
    'cus_name': "test",
    'cus_email': "test@test.com",
    'cus_phone': "01700000000",
    'cus_add1': "customer address",
    'cus_city': "Dhaka",
    'cus_country': "Bangladesh",
    'shipping_method': "NO",
    'multi_card_name': "",
    'num_of_item': 1,
    'product_name': "Test",
    'product_category': "Test Category",
    'product_profile': "general",
}

def get_session(data=data):
  response = sslcz.createSession(data)
  return response


def get_payment_status(sessionkey=None, tranid=None):
    if sessionkey:
      response = sslcz.transaction_query_session(sessionkey)
    if tranid:
      response = sslcz.transaction_query_tranid(tranid)
    return response

