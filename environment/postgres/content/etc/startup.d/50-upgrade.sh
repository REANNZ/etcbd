#!/bin/bash

set -eu

# Migrate data from old PostgreSQL in /var/lib/postgresql/data/$DATA_VERSION
# to new PostgreSQL in /var/lib/postgresql/data/$PG_MAJOR

# Assume any old data is already moved to a versioned directory.
if [ -e /var/lib/postgresql/data/PG_VERSION ] ; then
    echo "Unversioned data found in /var/lib/postgresql/data/PG_VERSION, aborting."
    exit 1
fi

# If the DB version file does not exist at this point,
# initialise a new deployment.
if [ ! -e /var/lib/postgresql/data/current ] ; then
  echo "New install: initialising $PG_MAJOR database"
  docker-ensure-initdb.sh
  echo "New install: recording $PG_MAJOR as current version"
  echo $PG_MAJOR > /var/lib/postgresql/data/current
fi

DATA_VERSION=$( cat /var/lib/postgresql/data/current )

# Migrate data from old database to new
if [ "${DATA_VERSION}" != "${PG_MAJOR}" ] ; then
  # Confirm we will be able to proceed with the upgrade
  if [ ! -d "/usr/lib/postgresql/$DATA_VERSION" ] ; then
    echo "Binaries for PostgreSQL $DATA_VERSION not found, upgrade not possible"
    exit 1
  fi

  # Make sure new database is initialised
  echo "Upgrade: initialising empty $PG_MAJOR database"
  docker-ensure-initdb.sh

  # We will need a postgres-writeable current directory
  WRKDIR=$( gosu postgres mktemp -d )
  echo "Upgrading data from $DATA_VERSION to $PG_MAJOR"
  ( cd $WRKDIR ; gosu postgres pg_upgrade --old-bindir="/usr/lib/postgresql/$DATA_VERSION/bin" --old-datadir=/var/lib/postgresql/data/$DATA_VERSION --new-datadir=/var/lib/postgresql/data/$PG_MAJOR )
  rm -rf $WRKDIR
  echo "Successfully upgraded, recording $PG_MAJOR as current version"
  echo $PG_MAJOR > /var/lib/postgresql/data/current
else
  echo "Database already at version $PG_MAJOR"
fi

