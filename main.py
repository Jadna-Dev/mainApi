from fastapi import FastAPI
import uvicorn
app = FastAPI()

@app.get("/")
async def home():
    return{
        "msg":"Done Correctly"
    }

if __name__ == "__main__":
    uvicorn.run(app=app,host="127.0.0.1",port=8000)