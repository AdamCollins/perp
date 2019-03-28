#!/bin/bash

PROJECT_NAME=perp
BUILD="NO"
RUN="NO"
PUSH="NO"
FRONT="NO"

function show_help() {
    printf "Invalid command.\nUsage: ./perp [build(--front)|run|push]\n"
    exit 1
}

function build_frontend() {
    echo Building Frontend
    pushd frontend
    npm install
    ng build
    popd
}

function build_image() {
    if [[ ${FRONT} == "YES" ]]
        then
            build_frontend
    fi
    docker build -t ${PROJECT_NAME} .
}

function run_container() {
    docker run --rm \
    -p 8000:80 \
    -e PERP_DATABASE_USER=root \
    -e PERP_DATABASE_HOST=host.docker.internal \
    -e PERP_DATABASE_NAME=perp \
    --name ${PROJECT_NAME} ${PROJECT_NAME}
}

function push_image() {
    $(aws ecr get-login --no-include-email --region us-east-2)
    docker tag perp:latest 978228982337.dkr.ecr.us-east-2.amazonaws.com/perp:latest
    docker push 978228982337.dkr.ecr.us-east-2.amazonaws.com/perp:latest
}

for i in "$@"
do
case $i in
    "build")
        BUILD="YES"
        ;;
    "run")
        RUN="YES"
        ;;
    "push")
        PUSH="YES"
        ;;
    "--front")
        FRONT="YES"
        ;;
    *)
        show_help
        ;;
esac
done

if [[ ${BUILD} == "YES" ]]
    then
        build_image
fi
if [[ ${RUN} = "YES" ]]
    then
        run_container
fi
if [[ ${PUSH} = "YES" ]]
    then
        push_image
fi
