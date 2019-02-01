#!/usr/bin/env bash
ps -ef | grep run_cn.py | grep -v grep | cut -c 9-15 | xargs kill -s 9
