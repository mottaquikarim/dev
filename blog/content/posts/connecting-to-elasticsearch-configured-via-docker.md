---
title: "Connecting to Elasticsearch Configured via Docker"
date: 2020-03-16T06:37:08Z
tags: ["docker", "elasticsearch"]
---

{{<toc>}}

## Elastic Search and Docker

Setting up an elasticsearch + kibana runtime is very easy to do with docker-compose:

```yaml
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.3.2
    environment:
      - cluster.name=docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    ports:
      - "9200:9200"
  kibana:
    image: docker.elastic.co/kibana/kibana:6.3.2
    ports:
      - "5601:5601"
```

For more information on the defaults (`ulimits` or `environment` variables, please see [this](https://blog.k2datascience.com/running-elasticsearch-kibana-using-docker-5ff10ad017d0) post)

To run, you simply:

```bash
docker-compose up -d
```

And then navigate over to http://localhost:9200 for elasticsearch or http://localhost:5601 for kibana.

## Gotchas

As with all things, there may be some gotchas associated with this setup. Specifically, you may notice that sometimes navigating to the URLs referenced above will result in connection errors.

This can be for quite a few reasons, I'll list some common ones I've encountered below.

### Windows: ElasticSearch doesn't work

A few things to check - run a `docker ps -a` to ensure your container is running and for how long.

if it only lives for a few seconds, it may be due to a default [`max_map_count` issue](https://stackoverflow.com/a/11685165). To fix, if using `docker-machine`:

```bash
docker-machine ssh
sudo sysctl -w vm.max_map_count=262144
exit
```

If _not_ using `docker-machine`, try:

```bash
docker exec -it <container_id> /bin/bash
sysctl -w vm.max_map_count=262144
```

*NOTE*: this will not persist after container is killed. TO make it "permanent" you might want to:

```bash 
vi /etc/sysctl.conf
vm.max_map_count=262144
```

(press `:q` to exit)

```bash
vi /etc/rc.local
echo 262144 > /proc/sys/vm/max_map_count
```
[_source_](https://stackoverflow.com/a/53047291)

### Even after changes above, not working

One bit to note is that the docker container is simply wrapping the elasticsearch service. As such, sometimes it just takes a bit of time to load.

To ensure that elasticsearch is running properly, consider running:

```bash
docker-compose logs elasticsearch
```

This will display the log messages emitted as elasticsearch is booted inside your container.

```bash
example_elasticsearch | [2020-03-16T05:32:12,704][INFO ][o.e.n.Node               ] [IzFG4tZ] initialized
example_elasticsearch | [2020-03-16T05:32:12,704][INFO ][o.e.n.Node               ] [IzFG4tZ] starting ...
example_elasticsearch | [2020-03-16T05:32:12,959][INFO ][o.e.t.TransportService   ] [IzFG4tZ] publish_address {172.18.0.2:9300}, bound_addresses {0.0.0.0:9300}
```

Once you see those three lines, you _should_ be safe to attempt your "healthcheck" such as visiting `http://localhost:9200` in the browser or curling for it.

Alternatively, if something is foobar'd you'll see it here which gives you further clues as to what went wrong.

