# How to use this image

## start a bot instance

```
docker run  --name some-name -e BOT_TOKEN=your_telegram_token -e DB_ADDRESS=postgres_ip -e DB_PORT=postgres_port -e DB_NAME=postgres_db_name -e DB_USER=postgres_db_user -e DB_PASSWORD=postgres_db_password  -d khdev/translate
```
* **-e BOT_TOKEN** is the parameter that, token your bot (from BotFather).
* **-e DB_ADDRESS** is the parameter that, IP Address your postgres server (is you don't have db server, you can run the command below from requirements).
* **-e DB_PORT** is the parameter that, port your postgres server.
* **-e DB_NAME** is the parameter that, database name your postgres server.
* **-e DB_USER** is the parameter that, username your postgres server.
* **-e DB_PASSWORD** is the parameter that, password your postgres server.
* **-d** is the parameter that runs the Docker Container in the detached mode, i.e., in the background. If you accidentally close or terminate the Command Prompt, the Docker Container will still run in the background.

## requirements postgresql
```
docker run  --name some-name -p 5432:5432 -e POSTGRES_PASSWORD=your_password -d postgres 
```
* **-p 5432:5432** is the parameter that establishes a connection between the Host Port and Docker Container Port. In this case, both ports are given as 5432, which indicates requests sent to the Host Ports will automatically redirect to the Docker Container Port. In addition, 5432 is also the same port where PostgreSQL will be accepting requests from the client.
* **-e POSTGRES_USER** is the parameter that sets a unique username to the Postgres database.
* **-e POSTGRES_PASSWORD** is the parameter that allows you to set the password of the Postgres database.
* **-d** is the parameter that runs the Docker Container in the detached mode, i.e., in the background. If you accidentally close or terminate the Command Prompt, the Docker Container will still run in the background.
* **postgres** is the name of the Docker image that was previously downloaded to run the Docker Container.