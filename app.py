import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.state.SECRET_KEY = "secret"
security = OAuth2PasswordBearer(tokenUrl='/token')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {
    'user1': 'password1',
    'user2': 'password2',
}


@app.post('/token')
async def login(username: str, password: str):
    if username not in users or users[username] != password:
        raise HTTPException(
            status_code=401, detail='Incorrect username or password')
    return {'access_token': username, 'token_type': 'bearer'}


@app.get('/')
async def index(*, authorization: str = Depends(security)):
    return {'status_code': 200, 'message': 'Success fetch the API!'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
