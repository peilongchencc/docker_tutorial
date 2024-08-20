from fastapi import FastAPI, HTTPException
from dataform import Item
from loguru import logger

# 设置日志配置
logger.remove()  # 移除默认的日志处理器
logger.add("docker_example.log", 
           rotation="1 GB",          # 日志文件超过 1 GB 后自动轮换
           backtrace=True,           # 完整的回溯信息，即使被包装
           diagnose=True,            # 诊断日志的详细输出，帮助调试
           format="{time} {level} {message}")  # 自定义日志格式

app = FastAPI()

# 根路径 GET 请求
@app.get("/")
def read_root():
    logger.info("GET / request received.")
    return {"message": "Hello, Docker with Loguru!"}

# GET 请求，用于获取物品信息
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    if item_id <= 0:
        logger.warning(f"Invalid item_id: {item_id}")
        raise HTTPException(status_code=400, detail="Invalid item_id")
    logger.info(f"GET /items/{item_id} request received with query: {q}")
    return {"item_id": item_id, "q": q}

# POST 请求，用于创建物品
@app.post("/items/")
def create_item(item: Item):
    logger.info(f"POST /items request received with item: {item}")
    return {"item": item}