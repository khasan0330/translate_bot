# How to use this image

## start a bot instance

```
docker run  --name some-name -e BOT_TOKEN=your_telegram_token -e DB_ADDRESS=postgres_ip -e DB_PORT=postgres_port -e DB_NAME=postgres_db_name -e DB_USER=postgres_db_user -e DB_PASSWORD=postgres_db_password  -d khdev/translate
```




## requirements postgresql
```
docker run  --name some-name -p 5432:5432 -e POSTGRES_PASSWORD=your_password -d postgres 
```
* -p 5432:5432 is the parameter that establishes a connection between the Host Port and Docker Container Port. In this case, both ports are given as 5432, which indicates requests sent to the Host Ports will automatically redirect to the Docker Container Port. In addition, 5432 is also the same port where PostgreSQL will be accepting requests from the client.
* -e POSTGRES_USER is the parameter that sets a unique username to the Postgres database.
* -e POSTGRES_PASSWORD is the parameter that allows you to set the password of the Postgres database.
* -d is the parameter that runs the Docker Container in the detached mode, i.e., in the background. If you accidentally close or terminate the Command Prompt, the Docker Container will still run in the background.
* Postgres is the name of the Docker image that was previously downloaded to run the Docker Container.