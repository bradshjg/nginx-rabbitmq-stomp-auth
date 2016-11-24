# nginx-rabbitmq-stomp-auth

## Getting Started

`vagrant up`

`vagrant ssh`

`cd /vagrant`

`./app.py`

Visit 192.168.33.10:8000 in a browser, use username: bob, password: changeme to login.

## ...Well That Was Dumb

Maybe, but hear me out.

This is a prototype for securing access to RabbitMQ's Web-Stomp plugin. It uses NGINX as a reverse proxy for the 
WebSocket connection and leverages the auth\_request directive which allows for client authorization based on the
result of a subrequest. Furthermore, since RabbitMQ's Web-Stomp plugin allows for basic authentication, STOMP
credentials can be passed directly from the auth subrequest to RabbitMQ, removing client access to the RabbitMQ
credentials. This is accomplished by collecting header info from the auth subrequest and passing it to the RabbitMQ
upstream.
