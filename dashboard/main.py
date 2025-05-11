from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'status':'ok'}

# TODO: додати ендпоінти для latency, P&L, Sharpe, health checks
