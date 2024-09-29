#!/bin/sh
set -e

host="$MYSQL_HOST"
port="$MYSQL_PORT"

until nc -z -v -w30 $host $port
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

echo "Database is ready!"