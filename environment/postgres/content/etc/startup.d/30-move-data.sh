#!/bin/bash

set -eu

# Move PostgreSQL data from /var/lib/postgresql/data
# to versioned directory /var/lib/postgresql/data/$DATA_VERSION

# Detect there is unmigrated data
if [ -e /var/lib/postgresql/data/PG_VERSION ] ; then

  DATA_VERSION=$( cat /var/lib/postgresql/data/PG_VERSION )
  # Bail out if old data exist in both locations
  if [ -e /var/lib/postgresql/data/$DATA_VERSION/PG_VERSION ] ; then
    echo "Data exists both in /var/lib/postgresql/data and /var/lib/postgresql/data/$DATA_VERSION, aborting."
    exit 1
  fi

  # Confirm we will be able to proceed with the upgrade
  if [ ! -d "/usr/lib/postgresql/$DATA_VERSION" ] ; then
    echo "Binaries for PostgreSQL $DATA_VERSION not found, upgrade not possible"
    exit 1
  fi

  echo "Moving data from /var/lib/postgresql/data into /var/lib/postgresql/data/$DATA_VERSION"
  install --verbose --directory --owner postgres --group postgres --mode 0700 "/var/lib/postgresql/data/$DATA_VERSION"
  # Pattern to avoid moving the numeric version named directories (all PostgreSQL files or dirs start with a letter)
  mv /var/lib/postgresql/data/[a-zA-Z]* /var/lib/postgresql/data/$DATA_VERSION

  echo "Successfully moved data from /var/lib/postgresql/data into /var/lib/postgresql/data/$DATA_VERSION, recording $DATA_VERSION as current version"
  echo $DATA_VERSION > /var/lib/postgresql/data/current
else
  echo "No unversioned data in /var/lib/postgresql/data, nothing to move"
fi

