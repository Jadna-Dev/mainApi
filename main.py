from fastapi import FastAPI
import uvicorn
from activation.activation import activation
from database.main import database
from checkSales.checkSales import cs

app = FastAPI()

app.mount("/activation", app=activation, name="activation")
app.mount("/database", app=database, name="database")
app.mount("/cs", app=cs, name="checkSales")


@app.get("/")
async def home():
    return {
        "msg": "Done Correctly"
    }

if __name__ == "__main__":
    with open("./config.json", "r") as conf:
        config = eval(str(conf.read()))
    uvicorn.run("main:app", host=config["host"], port=config["port"],reload=True)
