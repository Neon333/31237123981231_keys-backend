import uvicorn
from api.api_server import fast_api_app


if __name__ == "__main__":
    uvicorn.run(fast_api_app, host="0.0.0.0", port=9000, reload=False)