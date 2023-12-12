import requests
from fastapi import FastAPI
from main_config import get_price, money


app = FastAPI()


@app.get("/")
def hello():
    return "Hello World!"


@app.get("/price")
def show_price() -> float:
    return get_price()


@app.get("/money")
def show_money() -> float:
    return money()


@app.get("/ip")
def get_public_ipv4():
    try:
        response = requests.get('https://httpbin.org/ip')
        ip_data = response.json()
        public_ipv4 = ip_data['origin']
        return public_ipv4
    except Exception as e:
        return f"Помилка: {e}"


@app.get("/info")
def info():
    return {
        "name": "Basiliy Pupckin",
        "user_name": "Nagibator_3000",
        "phon_number": "+38 123 45 67",
        "money": "999999.99"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


