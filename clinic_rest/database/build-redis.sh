docker build -t redis_server .
docker run -p 6380:6379 redis_server