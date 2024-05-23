#!/bin/bash
## Writeable envs
PKG_NAME="spark-deepin-wine-runner"
LINGLONG_WORK_DIR="/data/linglong-build"

## Auto generated
LINGLONG_PKG_NAME="${PKG_NAME}.linyas"
USER=$(whoami)

ARCH=$(uname -m)

if [ ${ARCH} == "x86_64" ]; then
    arch="amd64"
#elif [ ${ARCH} == "aarch64" ]; then
    #arch="aarch64"
else
    echo "Unsupported architecture: ${ARCH}"
    exit 1
fi

if [ ${USER} == "root" ]; then
    echo "Running as root user is not supported!"
    exit 1
else
    echo "Check passed!"
fi

if [ ${PKG_NAME} = "" ] || [ ${LINGLONG_WORK_DIR} = "" ]; then
    echo "The string of PKG_NAME and LINGLONG_WORK_DIR could not be blank!"
    exit 1
else
    echo "Check passed!"
fi

  set -x

# Create linglong-pkg dir
    mkdir -p \
${LINGLONG_WORK_DIR}/linglong-build\
 ${LINGLONG_WORK_DIR}/linglong-deb

## clean old cache
    rm -rf ${LINGLONG_WORK_DIR}/linglong-deb/${PKG_NAME}*
    rm -rf ${LINGLONG_WORK_DIR}/linglong-build/${PKG_NAME}*

## Download deb files
  #cd ${LINGLONG_WORK_DIR}/linglong-deb
  #apt download ${PKG_NAME}

## Create convert workdir
    mkdir -p \
${LINGLONG_WORK_DIR}/linglong-build/${PKG_NAME}

CONVERT_DIR=${LINGLONG_WORK_DIR}/linglong-build/${PKG_NAME}

## Convery
  ll-pica init -w ${CONVERT_DIR} --pi ${LINGLONG_PKG_NAME} --pn ${PKG_NAME} -t repo
  #ll-pica convert -c ${LINGLONG_WORK_DIR}/linglong-deb/${PKG_NAME}*\
# -w ${CONVERT_DIR}
  ll-pica convert -w ${CONVERT_DIR}

## Build
  cd ${CONVERT_DIR}/package/${LINGLONG_PKG_NAME}/${arch}/
  ll-builder build
  ll-builder export

## Move files
  mv ${CONVERT_DIR}/package/${LINGLONG_PKG_NAME}/${arch}/*.layer ${CONVERT_DIR}/
  cd ${CONVERT_DIR}/package/${LINGLONG_PKG_NAME}/${arch}/

## Run Test
  ll-builder run
