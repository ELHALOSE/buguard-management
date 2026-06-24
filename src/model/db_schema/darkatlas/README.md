## Run Alembic Migrations

### Configuration

```bash
cp alembic.ini.example alembic.ini
```

### (Optional) Create a new migration

```bash
alembic revision --autogenerate -m "Add ..."
```
- Update the alembic.ini with your database credentials (sqlalchemy.url)

### Upgrade the database

```bash
alembic upgrade head
```
