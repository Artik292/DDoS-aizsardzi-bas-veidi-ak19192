#!/bin/bash

if [ $# -eq 0 ]; then
  printf "Wrong flag. Type: \n ./ip_ban.sh -h \n For help\n"
  exit 1
fi

ip_ban() {
        export NUMBER_FOR_SHOWING_IP=${1}
        export PROTOCOL=${2}
        python3 ./ip_ban.py
}

while getopts 'hN:' flag; do
        case "${flag}" in
                h) printf "This tool scan mail logs and show IP, if there was more than N connection count.\n -h        Help \n -N [number]     If more than N connection count, IP will be blocked.\n" ;;
                N) ip_ban "${2}" "${3}"
                        exit 1 ;;
                *) printf "Wrong flag. Type: \n ./ip_ban.sh -h \n For help\n"
        esac
done