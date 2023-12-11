from binance.client import Client
import json
from time import sleep
from telegram_config import send
from datetime import datetime
from icecream import ic



#Max 1
api_key = "1ZG2Ja9lkLFwjsKo7bZraBx35su2Tllbi6C1dO6qviJJ3QaXiS4B9dseOwfVGhYx"
secret_key = "Wu0anz5DuT9gKBIOH0d5KOI7IHO12wQ2Ew38cRrYSxfGXrnOqhxVcebCAlTPhnnm"


#Father
# api_key = "ryPMTkgK4IOuW4nFmaGgMl6dm8uHXejfK3Jyx3UsLp0xqNjjWak6v4gNUUeeU3Bs"
# secret_key = "Hngv8uEUexTBXw6IqxsslnlNUB9OrzRroq91nqjImv912U3yqrv9gwV9V9l18Wi0"


client = Client(api_key, secret_key)

interest = 1.003




def load(*keys) -> list | dict | int | str:
	with open("data.json", "r") as f:
		data = json.load(f)

	answer = []
	for key in keys:
		answer.append(data.get(key))

	if len(answer) == 1:
		return answer[0]

	return answer


def save(**kwargs):
	with open("data.json", "r") as f:
		data = json.load(f)

	for key, value in kwargs.items():
		data[key] = value

	with open("data.json", "w") as f:
		json.dump(data, f)


def create_user(user_id, values):
	users = load("users")
	users.update({str(user_id): values})
	save(users=users)


def user_update(user_id, **data):
	users = load("users")
	users.get(str(user_id)).update(data)
	save(users=users)


def find_users(users: dict, find_key: str, find_value: int | str) -> list[str]:
	answer = []
	for key, values in users.items():
		if values.get(find_key) == find_value:
			answer.append(key)

	return answer


def money(symbol="TUSD"):
	try:
		return float(client.get_asset_balance(asset=symbol).get("free"))
	except:
		sleep(1)
		return money(symbol)


def all_money():
	allMoney = money()

	for price, qty in load("buys").items():
		allMoney += float(price) * qty

	return allMoney


def cut(number, precision=5):
	return int(number * 10 ** precision) / 10 ** precision


def check_date(today):
	updata_date = load("updata_date")

	if updata_date == today:
		return False
	if updata_date != today:
		save(updata_date=today)
		return True


def addMonth(date: str) -> str:
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	
	date_list = date.split(" ")
	month = date_list[1]
	month_numer = months.index(month)
	date_list[1] = months[month_numer + 1]

	return " ".join(date_list)


def now():
	return datetime.now().strftime("%d.%m.%y | %H:%M:%S")


def info(text):
	text = f"[INFO] [{now()}] {text}"

	print(text)


def log(text):
	text = f"[LOG] [{now()}] {text}"

	with open("log.txt", "a") as f:
		f.write(text + "\n")

	print(text)


def pause(time: int) -> None:
	print(f"[PAUSE] [{now()}] {time}m")
	sleep(time * 60)


def get_price(symbol="BTCTUSD"):
	try:
		return float(client.get_symbol_ticker(symbol=symbol)["price"])
	except:
		info("Error")
		return get_price()


def buy():
	bet =  all_money() / load("moneySplit")

	if money() < bet:
		info("недостатньо грошей")
		return None, None

	price = get_price()

	btc = cut(bet / price)

	try:
		order = client.create_order(
			symbol='BTCTUSD',
			side='BUY',
			type='MARKET',
			quantity=btc
		)

		ic(order)
	except Exception as e:
		print(e)
		send("Senpai, я намагалася купити BTC, але в мене не вийшло це зробити через якусь помилку")
		return None, None

	price = sum(list(map(lambda fill: float(fill.get("price")), order.get("fills")))) / len(order.get("fills"))

	log(f"[BUY] {price=} TUSD | {btc=} BTC")
	send(f"Я купила вам {btc} BTC за ціною {price} TUSD, Senpai")

	buys = load("buys")

	buys[str(price)] = btc

	save(buys=buys)

	return price, btc


def sell(btc: int, key: str):
	try:
		order = client.create_order(
			symbol='BTCTUSD',
			side='SELL',
			type='MARKET',
			quantity=cut(btc),
		)

		ic(order)
	except Exception as e:
		print(e)
		send(f"Senpai, НЕГАЙНО!!! Потрібно, як умова швидше продати {cut(btc)} BTC")
		return

	tusd = 0
	for fill in order.get("fills"):
		tusd += float(fill.get("qty")) * float(fill.get("price"))

	was_tusd = cut(btc) * float(key)

	profit = tusd - was_tusd
	ic(tusd, was_tusd)

	log(f"[SELL] {profit=} TUSD = {profit * 100 / was_tusd}% | buy {tusd} TUSD | price={get_price()}BTC/TUSD")
	send(f"Senpai, я купила Вам {round(tusd, 2)} TUSD і заробила Вам {round(tusd - was_tusd, 3)} TUSD це приблизно {profit * 100 / was_tusd}%")

	users = load("users")
	creators_list = find_users(users, "segmentation", "creator")

	free_money = all_money()
	for user in users.values():
		fraction = profit * (user.get("money") / all_money())
		ic(user.get("name"), user.get("money"))

		match user.get("segmentation"):
			case "creator":
				user["money"] += fraction
				ic()
			case "best_friend":
				user["money"] += fraction * 0.5
				ic()

		free_money -= user.get("money")

		ic(user.get("money"))

	ic(free_money)

	free_money /= len(creators_list)
	for creator in creators_list:
		users[creator]["money"] += free_money

	buys = load("buys")
	buys.pop(key)
	save(buys=buys, users=users)


















