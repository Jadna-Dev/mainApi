from fastapi import FastAPI
import uvicorn
from activation.activation import activation
from checkSales.checkSales import cs
from QrMenu.qrMenu import qrMenu
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.mount("/activation", app=activation, name="activation")
app.mount("/cs", app=cs, name="checkSales")
app.mount("/qr", app=qrMenu, name="QrMenu")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# here


@app.get("/")
async def home():
    return {
        "msg": "Done Correctly"
    }

if __name__ == "__main__":
    with open("./config.json", "r") as conf:
        config = eval(str(conf.read()))
    uvicorn.run("main:app", host=config["host"],
                port=config["port"], reload=True)
