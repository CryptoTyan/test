from time import sleep
from binance.client import Client


#Max 1
api_key = "1ZG2Ja9lkLFwjsKo7bZraBx35su2Tllbi6C1dO6qviJJ3QaXiS4B9dseOwfVGhYx"
secret_key = "Wu0anz5DuT9gKBIOH0d5KOI7IHO12wQ2Ew38cRrYSxfGXrnOqhxVcebCAlTPhnnm"


#Father
# api_key = "ryPMTkgK4IOuW4nFmaGgMl6dm8uHXejfK3Jyx3UsLp0xqNjjWak6v4gNUUeeU3Bs"
# secret_key = "Hngv8uEUexTBXw6IqxsslnlNUB9OrzRroq91nqjImv912U3yqrv9gwV9V9l18Wi0"


client = Client(api_key, secret_key)

interest = 1.003





def money(symbol="TUSD"):
	try:
		return float(client.get_asset_balance(asset=symbol).get("free"))
	except:
		return "Error"


def get_price(symbol="BTCTUSD"):
	try:
		return float(client.get_symbol_ticker(symbol=symbol)["price"])
	except:
		return get_price()






