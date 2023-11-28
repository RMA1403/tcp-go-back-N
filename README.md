# Tugas Besar 1 - IF3130 Jaringan Komputer

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [How to Run](#how-to-run)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Authors](#authors)

## General Information


## Technologies Used
- python

## Features
- sending file


## How to Run
1. open 1 terminal for server on root directory
2. run this command
    ```bash
    python -m src.classes.Server [server port] data/[file name with extension that want to be sent] 
    ```
    for example
    ```bash
    python -m src.classes.Server 5000 data/data_long.txt
    ```
3. open one or more terminal for client on root directory
4. run this command
    ```bash
    python -m src.classes.Client [client port] [server port] data/output/[file name with extension for output file]
    ```
    for example
    ```bash
    python -m src.classes.Client 5001 5000 data/output/output1.txt
    ```
5. Follow the instructions on the server
6. For each following question on server terminal type "y" or "n" and enter

## Project Status
Project is: _complete_


## Room for Improvement

Room for improvement:
- Speed up algorithm

## Authors
Tidak ada pembagian kerja secara khusus, semua anggota kelompok mengerjakan semua bagian dari program ini. (mengerjakan bersama-sama)
1. Nigel Sahl (13521043)         
2. Hosea Nathanael Abetnego (13521057) 
3. Rava Maulana Azzikri (13521149)
