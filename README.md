# ☕🚀 SQUIT-backend

> ⚡ Start your Java projects as fast as possible

[![CodelyTV](https://img.shields.io/badge/codely-tv-green.svg?style=flat-square)](https://codely.tv)
[![CI pipeline status](https://github.com/CodelyTV/java-ddd-skeleton/workflows/CI/badge.svg)](https://github.com/CodelyTV/java-ddd-skeleton/actions)

## ℹ️ Introduction

Squit appplication will be an application done by MamboAcademy team in order to split expenses between friends.

## ℹ️ Boot Application


## 🏁 How To Start
#### Ubuntu
1. Install Python 3.8
    `sudo apt update`
    `sudo apt install software-properties-common`
    `sudo add-apt-repository ppa:deadsnakes/ppa`
    `sudo apt install python3.8`
    `python3.8 --version`
2. Set it as your default JVM: `export JAVA_HOME='/Library/Java/JavaVirtualMachines/amazon-corretto-8.jdk/Contents/Home'`
3. Clone this repository: `git clone https://github.com/CodelyTV/java-ddd-skeleton`.
4. Bring up the Docker environment: `make up`.
5. Execute some [Gradle lifecycle tasks](https://docs.gradle.org/current/userguide/java_plugin.html#lifecycle_tasks) in order to check everything is OK:
    1. Create [the project JAR](https://docs.gradle.org/current/userguide/java_plugin.html#sec:jar): `make build`
    2. Run the tests and plugins verification tasks: `make test`
6. Start developing!

## Docker

The Dockerfile is a file that is used as an input for Docker to build a virtual environment 
(the same as our PC) with all the software it needs and also all the "environmental" requirements.

The requirements the application needs arte stored in requirements.txt. This file is to import these requirements 
when our docker runs.

To create the Dockerfile image: `docker build -t squit-backend:1.0 .`


