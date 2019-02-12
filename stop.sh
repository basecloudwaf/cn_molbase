#!/usr/bin/env bash
ps -ef | grep check.py | grep -v grep | cut -c 9-15 | xargs kill -s 9
