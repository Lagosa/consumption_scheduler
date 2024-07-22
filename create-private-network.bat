@echo off
setlocal enabledelayedexpansion

call docker network create --gateway 172.19.0.1 --subnet 172.19.0.0/24 licenta-network
