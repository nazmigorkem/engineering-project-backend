#### Create Environment

-   RUN: `py -3 -m venv venv`

#### Run Environment

-   RUN: `.\venv\Scripts\activate`
-   RUN: `python.exe -m pip install --upgrade pip`
-   RUN: `pip install Flask`
-   RUN: `flask --app .\src\main.py`

#### Deactivate Environment

RUN: `deactivate`
