from cornac.models import BPR
from cornac.data import Dataset
from fastapi import FastAPI, status

app = FastAPI()

dataset = []
# Dataset should be in the format [(userId, videoId, liked (0 or 1)), ...]


@app.get("/check_existence/{user_id}", tags=["user"])
async def check_existence(user_id: str):
    return user_id == "1000"


@app.put("/register/", status_code=status.HTTP_201_CREATED, tags=["user"])
async def register(interests: set[str]):
    return 0


@app.put(
    "/watch/{user_id}/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["player"],
)
async def watch(user_id: str, item_id: str):
    pass


@app.put(
    "/like/{user_id}/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["player"]
)
async def like(user_id: str, item_id: str):
    pass


@app.put(
    "/unlike/{user_id}/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["player"],
)
async def unlike(user_id: str, item_id: str):
    pass


@app.get("/recommend_more/{user_id}", tags=["video_list"])
async def recommend_more(user_id: str):
    data = Dataset.build(dataset)
    # TODO: put the real dataset in
    bpr = BPR(
        k=10,
        max_iter=100,
        learning_rate=0.001,
        lambda_reg=0.001,
        use_bias=True,
    )
    bpr.fit(data)
    return 0
