#!/bin/bash

# set defaults
TAG=latest
REPOBASE="reannz"
PULL=""
NOCACHE=""
SKIPBUILD=""
SKIPPUSH=""

# Services we support
SERVICES="admintool elk icinga"
IMAGES_admintool="apache djnro postgres filebeat"
IMAGES_elk="elasticsearch logstash kibana apache"
IMAGES_icinga="icingaweb icinga postgres"
EXTRA_IMAGES="filebeat-radius filebeat-radsecproxy"

# parse arguments


while [ $# -gt 0 ] ; do
    if [ "$1" == "--tag" ] ; then
        TAG="$2"
        shift ; shift
    elif [ "$1" == "--repobase" ] ; then
        REPOBASE="$2"
        shift ; shift
    elif [ "$1" == "--pull" ] ; then
        PULL="$1"
        shift
    elif [ "$1" == "--no-cache" ] ; then
        NOCACHE="$1"
        shift
    elif [ "$1" == "--skip-build" ] ; then
        SKIPBUILD="$1"
        shift
    elif [ "$1" == "--skip-push" ] ; then
        SKIPPUSH="$1"
        shift
    elif [ "$1" == "--services" ] ; then
        SERVICES="$2"
        EXTRA_IMAGES=""
        shift ; shift
    elif [ "$1" == "--extra-only" ] ; then
        SERVICES=""
        shift
    else
        echo "Invalid argument $1"
        echo "Usage: $0 [options...]"
        echo "    --tag tag: set the tag of the container image"
        echo "    --repobase repobase: set the base name of the repositories to push into"
        echo "    --pull: pass --pull to docker compose build to refresh base images"
        echo "    --no-cache: pass --no-cache to docker compose build to do a fresh build"
        echo "    --skip-build: skip docker compose build - only tag and push current build"
        echo "    --skip-push: skip docker push, only build and tag services locally"
        echo "    --services \"list of services\": only build listed services,"
        echo "          skip other services and extra images"
        echo "    --extra-only: skip composed services and only build extra images"
        exit 1
    fi
done

#TAG="$(date +'%F')"

for SERVICE in $SERVICES ; do
    # build the images
    if [ -z "$SKIPBUILD" ] ; then
        COMPOSE_FILE=docker-compose-$SERVICE.yml COMPOSE_PROJECT_NAME=$SERVICE docker compose build $PULL $NOCACHE
    fi
    for IMAGE in $( eval "echo \${IMAGES_${SERVICE}}" ) ; do
        docker tag ${SERVICE}-${IMAGE} ${REPOBASE}/${SERVICE}_${IMAGE}:${TAG}
        if [ -z "$SKIPPUSH" ] ; then
            docker push $REPOBASE/${SERVICE}_${IMAGE}:${TAG}
        fi
    done
done

for IMAGE in $EXTRA_IMAGES ; do
    if [ -z "$SKIPBUILD" ] ; then
        docker build $PULL $NOCACHE -t ${IMAGE} ${IMAGE}/
    fi
    docker tag $IMAGE $REPOBASE/${IMAGE}:${TAG}
    if [ -z "$SKIPPUSH" ] ; then
        docker push $REPOBASE/${IMAGE}:${TAG}
    fi
done

