import json
from fastapi import APIRouter

router = APIRouter()
router.prefix = "/routes"


class Routes:

    @router.get('/get')
    def get():
        data = None
        with open('./data/routes.json') as f:
            data = json.load(f)
        return data
