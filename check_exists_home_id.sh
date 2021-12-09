#!/bin/sh

# chmod u+x add_home_id.sh
ENV_FILE=".env"
if grep -q "HOME_ID" $ENV_FILE; then
  echo "found!"
fi