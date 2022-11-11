#### Create Environment

-   RUN: `py -3 -m venv venv`

#### Run Environment

-   RUN: `.\venv\Scripts\activate`
-   RUN: `python.exe -m pip install --upgrade pip`
-   RUN: `pip install -r ./requirements.txt`
-   RUN: `cd ./src`
-   RUN: `uvicorn main:app --reload --port=5000`

#### Deactivate Environment

RUN: `deactivate`

### Run Environment For Mac

-   RUN: `. venv/bin/activate`
-   RUN: `cd ./src`
-   RUN: `uvicorn main:app --reload --port=5000`
