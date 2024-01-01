from fastapi import FastAPI
from fastapi import FastAPI


from pydantic import BaseModel




from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Body(BaseModel):
    name: str

@app.get("/dummy_get")
def hello(name: str):
  return {'Hello ' + name + '!'}


@app.post("/dummy_post")
def send_here(body: Body):
   return "Hello " + body.name + ", Free Palestine! 🇵🇸🇵🇸🇵🇸🇵🇸🇵🇸"