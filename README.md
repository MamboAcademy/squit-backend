# ☕🚀 SQUIT-backend

> ⚡ Start your Java projects as fast as possible

[![CodelyTV](https://img.shields.io/badge/codely-tv-green.svg?style=flat-square)](https://codely.tv)
[![CI pipeline status](https://github.com/CodelyTV/java-ddd-skeleton/workflows/CI/badge.svg)](https://github.com/CodelyTV/java-ddd-skeleton/actions)

## ℹ️ Introduction

This is a repository intended to serve as a starting point if you want to bootstrap a Java project with JUnit and Gradle.

Here you have the [course on CodelyTV Pro where we explain step by step all this](https://pro.codely.tv/library/ddd-en-java/about/?utm_source=github&utm_medium=social&utm_campaign=readme) (Spanish)

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

## ☝️ How to update dependencies

* Gradle ([releases](https://gradle.org/releases/)): `./gradlew wrapper --gradle-version=WANTED_VERSION --distribution-type=bin`

## 💡 Related repositories

### ☕ Java

* 📂 [Java Basic Skeleton](https://github.com/CodelyTV/java-basic-skeleton)
* ⚛ [Java OOP Examples](https://github.com/CodelyTV/java-oop-examples)
* 🧱 [Java SOLID Examples](https://github.com/CodelyTV/java-solid-examples)
* 🥦 [Java DDD Example](https://github.com/CodelyTV/java-ddd-example)

### 🐘 PHP

* 📂 [PHP Basic Skeleton](https://github.com/CodelyTV/php-basic-skeleton)
* 🎩 [PHP DDD Skeleton](https://github.com/CodelyTV/php-ddd-skeleton)
* 🥦 [PHP DDD Example](https://github.com/CodelyTV/php-ddd-example)

### 🧬 Scala

* 📂 [Scala Basic Skeleton](https://github.com/CodelyTV/scala-basic-skeleton)
* ⚡ [Scala Basic Skeleton (g8 template)](https://github.com/CodelyTV/scala-basic-skeleton.g8)
* ⚛ [Scala Examples](https://github.com/CodelyTV/scala-examples)
* 🥦 [Scala DDD Example](https://github.com/CodelyTV/scala-ddd-example)

## Docker

The Dockerfile is a file that is used as an input for Docker to build a virtual environment 
(the same as our PC) with all the software it needs and also all the "environmental" requirements.

The requirements the application needs arte stored in requirements.txt. This file is to import these requirements 
when our docker runs.
