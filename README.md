#### Create Environment

-   RUN: `py -3 -m venv venv`

#### Run Environment

-   RUN: `.\venv\Scripts\activate`
-   RUN: `python.exe -m pip install --upgrade pip`
-   RUN: `pip install -r ./requirements.txt`
-   RUN: `flask --app .\src\main.py run`

#### Deactivate Environment

RUN: `deactivate`
