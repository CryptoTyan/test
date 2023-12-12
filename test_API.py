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
def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        ip_data = response.json()
        public_ip = ip_data['ip']
        return public_ip
    except Exception as e:
        return f"Помилка: {e}"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


