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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)


