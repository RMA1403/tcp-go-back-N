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
Kami diminta untuk membuat sistem program yang terdiri dari server dan client yang berkomunikasi lewat jaringan. Program dibuat menggunakan bahasa Python 3, dan Kami tidak boleh menggunakan library diluar built-in bawaan Python 3. 

Program dijalankan di lingkungan sistem operasi berbasis Linux maupun Windows. Server dan client dibuat secara terpisah dan dijalankan secara terpisah (dijalankan sebagai proses yang berbeda, namun dijalankan di mesin yang sama). Server dan client akan saling mengirim dan menerima berkas file yang merupakan data binary.

## Technologies Used
- python
- threading
- argparse
- binascii
- socket
- struct

## Features
- sending file from server to client and to multiple clients
- three way handshake
- sliding window
- error detection with checksum 

## How to Run
1. open 1 terminal for server on root directory
2. run this command
    ```bash
    python -m src.classes.Server [broadcast port] data/[file name with extension that want to be sent] 
    ```
    for example
    ```bash
    python -m src.classes.Server 5000 data/data_long.txt
    ```
3. open one or more terminal for client on root directory
4. run this command
    ```bash
    python -m src.classes.Client [client port] [broadcast port] data/output/[file name with extension for output file]
    ```
    for example
    ```bash
    python -m src.classes.Client 5001 5000 data/output/output1.txt
    ```
5. Follow the instructions on the server
6. For each following question on server terminal type "y" or "n" and enter

The questions are:
1. q1: Apakah ingin mengirim ke semua client sekaligus secara parallel? (y/n)
2. q2: Mulai mengirim untuk client ke-x, port p ? (y/n)
3. q3: Lanjutkan pengiriman untuk client berikutnya? (y/n)

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
