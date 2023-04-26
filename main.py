from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
async def home():
    return{
        "msg":"Done Correctly"
    }

if __name__ == "__main__":
    uvicorn.run(app=app,host="172.23.93.157",port=8000)