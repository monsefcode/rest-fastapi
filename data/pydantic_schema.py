from pydantic import BaseModel

class Items(BaseModel):
    brand_name: str
    title: str
    thumbnail: str
    price: str


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