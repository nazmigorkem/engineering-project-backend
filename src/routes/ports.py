import json
from fastapi import APIRouter

router = APIRouter()
router.prefix = "/ports"


class Ports:

    @staticmethod
    @router.get('/get')
    def get():
        with open('./data/ports.json') as f:
            data = json.load(f)
        return data
