from fastapi import FastAPI
import uvicorn
from activation.activation import activation

app = FastAPI()

app.mount("/activation", app=activation, name="activation")

@app.get("/")
async def home():
    return{
        "msg":"Done Correctly"
    }

if __name__ == "__main__":
    with open("./config.json","r") as conf:
        config = eval(str(conf.read()))
    uvicorn.run(app=app,host=config["host"],port=config["port"])