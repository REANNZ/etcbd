#!/bin/bash

# Ancillary functions: define separate exec functions for Kubernetes and Docker
# Both provide uniform interface:
# exec_func exec-flags container command
# NOTE: exec-flags must be specified even when empty - add extra ""

function kubectl_exec() {
  FLAGS=$1
  shift
  CONTAINER=$1
  shift
  kubectl exec $FLAGS $PODNAME -c $CONTAINER -- "$@"
}
# TODO: kubectl exec ... why do -i exec's hang?
# Wait for fix to kubernetes/kubernetes#13322 to be included in a release


function docker_exec() {
  FLAGS=$1
  shift
  CONTAINER=$1
  shift
  docker exec $FLAGS -- $CONTAINER "$@"
}

# This script supports both Docker-compose and Kubernetes

PODNAME=""

if [ "$1" == "--pod" ] ; then
    shift
    PODNAME="$1"
    shift
    echo "Using Kubernetes pod $PODNAME"
    function exec_func() { kubectl_exec "$@" ; }
else
    echo "No pod name specified, using docker exec"
    function exec_func() { docker_exec "$@" ; }
fi


if [ $# -eq 0 ] ; then
    echo "Usage: $0 [--pod podname] environment_file(s).."
    exit 1
fi
# Load the local deployment environment variables
# (and filtre the syntax to quote the values first)
eval $( cat "$@" | sed 's/=\(.*\)/="\1"/' )



# Create databases in the Postgres Image
# Run a command in the Postgres database to create the role and database
# Equivalant to:
#   create role djnrodev with login encrypted password 'djnrodev';
#   create database djnrodev with owner djnrodev;

exec_func "" postgres gosu postgres psql --command="create role $DB_USER with login encrypted password '$DB_PASSWORD' ;"
exec_func "" postgres gosu postgres psql --command="create database $DB_NAME with owner $DB_USER;"

# Initialize database on the Django side - and create super user
exec_func -i djnro ./envwrap.sh ./manage.py syncdb <<-EOF
	yes
	$ADMIN_USERNAME
	$ADMIN_EMAIL
	$ADMIN_PASSWORD
	$ADMIN_PASSWORD
EOF

exec_func "" djnro ./envwrap.sh ./manage.py migrate

# load django fixtures - initial data
exec_func "" djnro ./envwrap.sh ./manage.py loaddata initial_data/fixtures_manual.xml

# run fetch-kml one-off:
exec_func "" djnro ./envwrap.sh ./manage.py fetch_kml

# create initial realm
exec_func -i djnro ./envwrap.sh ./manage.py shell <<-EOF
	from edumanage.models import Realm
	Realm(country="$REALM_COUNTRY_CODE").save()
	exit()
EOF

# Configure the name of the Django site
exec_func -i djnro ./envwrap.sh ./manage.py shell <<-EOF
	from django.contrib.sites.models import Site
	site = Site.objects.get(name="example.com")
	site.name="$SITE_PUBLIC_HOSTNAME"
	site.domain="$SITE_PUBLIC_HOSTNAME"
	site.save()
	exit()
EOF

# import initial data
if [ -n "$REALM_EXISTING_DATA_URL" ] ; then
    # NOTE: this exact spelling
    exec_func "" djnro curl -o djnro/institution.xml "$REALM_EXISTING_DATA_URL"
    exec_func "" djnro ./envwrap.sh ./manage.py parse_institution_xml --verbosity=0 djnro/institution.xml
fi

