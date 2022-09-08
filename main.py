try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    from bson.objectid import ObjectId
    from datetime import datetime
    import motor.motor_asyncio

except Exception as e:
    print(f"Error some Modules are Missing !!! : {e}")

app = FastAPI()


MONGO_URI = "mongodb+srv://<CLUSTER-NAME>:<PASSWORD>@cluster0.u8ump.mongodb.net/test"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

database = client.FASTAPI
FASTAPI_collection = database.get_collection("FasterAPI")

def schema_helper(task) -> dict:
    """
        HELPER TO MAKE MONGO QUERY INTO DICT FORM
    """

    return {
        "id": str(task["_id"]),
        "Title": str(task["title"]),
        "Thumbnail": str(task["thumbnail"]),
        "Price": str(task["price"]),
    }


class Items(BaseModel):
    brand_name: str
    title: str
    thumbnail: str
    price: str

@app.get("/")
async def get_all_data():
    datas = []
    async for data in FASTAPI_collection.find():
        datas.append(schema_helper(data))
    return datas

# Retrieve a data with a matching ID present in the database
@app.get("/{data_id}")
async def get_data(data_id: str):
    data_data = await FASTAPI_collection.find_one({"_id": ObjectId(data_id)})
    return schema_helper(data_data)

# Add a new data into to the database
@app.post('/new/', status_code=201)
async def post_data(item: dict) -> dict:
    data_data = await FASTAPI_collection.insert_one(item)
    new_data = await FASTAPI_collection.find_one({"_id": data_data.inserted_id})
    return schema_helper(new_data)


# Delete a data from the database
@app.delete('/delete_data/{data_id}')
async def delete_data(data_id: str):
    '''
    Return: 
            true, once the data got deleted.
    '''
    data = await FASTAPI_collection.find_one({"_id": ObjectId(data_id)})
    if data:
        await FASTAPI_collection.delete_one({"_id": ObjectId(data_id)})
        return "Deleted"
    return "Not Deleted"

# Update data with a matching ID
@app.put('/update_data/{data_id}')
async def update_data(id: str, data: dict):
    '''
    Return: 
            true, once the data element got updated.
            false, if an empty request body is sent.
    '''
    if len(data) < 1:
        return False
    data = await FASTAPI_collection.find_one({"_id": ObjectId(id)})

    # add update and update time field to get tracked
    data.update({"update":True, "updated_time":datetime.now()})
    if data:
        updated_data = await FASTAPI_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_data:
            return True
        return False
