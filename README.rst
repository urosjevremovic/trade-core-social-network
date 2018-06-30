social website REST API
-------------

​REST​ API for social network​.

In order to asynchronously pick up additional info about registered users using clearbit API you should have
rabbitmq server running along with celery.

In your local environment:

sudo rabbitmq-server
celery -A social_network_REST_API worker -l info