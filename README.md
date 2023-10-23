# Grafana DashBoard v2

## Set DataBase

1. Initialize
    ```bash=
    $ alembic init migrate
    ```
2. Editing the alembic.ini File
    ```python=58
    sqlalchemy.url = sqlite:///test.db
    ```
3. Editing the migrate/env.py File
    > Insert
    ```python=7
    from models import Base
    ```

    > Edit
    ```python=22
    target_metadata = Base.metadata
    ```
4. Migrate
    ```bash=
    $ alembic revision --autogenerate -m "\<description\>"
    ```
5. Upgrade
    ```bash=
    $ alembic upgrade head
    ```

### Others

alembic current：查看數據庫現在版本。  
alembic history：查看數據庫所有版本。  
alembic upgrade head：將數據庫升級到最新版本。  
alembic downgrade base：將數據庫降級到最初版本。  
alembic upgrade <version>：將數據庫升級到指定版本。  
alembic downgrade <version>：將數據庫降級到指定版本。  
alembic upgrade +2：相對升級，將數據庫升級到當前版本後的兩個版本。  
alembic downgrade +2：相對降級，將數據庫降級到當前版本前的兩個版本。  

## Install Grafana

https://grafana.com/docs/grafana/latest/setup-grafana/installation/
