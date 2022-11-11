import json
from fastapi import APIRouter

router = APIRouter()
router.prefix = "/ports"


class Ports:

    @router.get('/get')
    def get():
        data = None
        with open('./data/ports.json') as f:
            data = json.load(f)
        return data
