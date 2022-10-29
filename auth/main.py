from fastapi import FastAPI


app = FastAPI()


@app.get(path="/")
def get1():
    return {"Hello": "World"}