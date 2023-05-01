# How to use this image

## start a bot instance

```
docker run  --name some-name -e BOT_TOKEN=your_telegram_token -e DB_ADDRESS=postgres_ip -e DB_PORT=postgres_port -e DB_NAME=postgres_db_name -e DB_USER=postgres_db_user -e DB_PASSWORD=postgres_db_password  -d khdev/translate
```
