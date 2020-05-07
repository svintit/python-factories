# Usage

```python
db_session = SessionFactory(bind=db_engine)
db_data = select_one(
    table=TableFactory(Tables.USER),
    filter_={"id": user_id},
    session=db_session,
)

# do stuff
name = ""
email = ""

update_one(
    TableFactory(Tables.USER),
    filter_={"id": user_id},
    values={"name": name, "email": email},
    session=db_session,
)
session_commit(db_session)  # auto-closes session
```
