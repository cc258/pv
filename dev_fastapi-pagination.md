# fastapi-pagination

# Usage
https://uriyyo-fastapi-pagination.netlify.app/#introduction

# Repo
https://github.com/uriyyo/fastapi-pagination

# Quick start

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

# import all you need from fastapi-pagination
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()  # create FastAPI app
add_pagination(app)  # important! add pagination to your app

```

```python
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate


@app.get("/users")
def get_users(db: Session = Depends(get_db)) -> Page[UserOut]:
    return paginate(db, select(User).order_by(User.created_at))
```
