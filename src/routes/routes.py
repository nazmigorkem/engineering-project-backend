import json

from fastapi import APIRouter

router = APIRouter()
router.prefix = "/routes"


class Routes:
    @staticmethod
    @router.get('/get')
    def get():
        with open('./data/routes.json') as f:
            data = json.load(f)
        return data
