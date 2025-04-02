#!/bin/bash
set -ex

docker network create local || true
docker-compose -f $PWD/docker-compose.yml down
docker-compose -f $PWD/docker-compose.yml up -d

echo "Waiting for Snowflake to be ready..."
until curl -s -d '{}' snowflake.localhost.localstack.cloud:4566/session | grep -q '{"success": true}'; do
  sleep 1
done

echo "Running flyway..."
docker run \
	--rm \
	--net=local \
	--env JAVA_ARGS="--add-opens java.base/java.nio=ALL-UNNAMED" \
	-v ./migrations:/flyway/sql \
	flyway/flyway:11.3.3-alpine \
	-user=test \
	-password=test \
	-url="jdbc:snowflake://http://snowflake.localhost.localstack.cloud:4566/?db=test&schema=PUBLIC&JDBC_QUERY_RESULT_FORMAT=JSON" \
	-schemas=FLYWAY_MYSCHEMA,MYSCHEMA \
	migrate;