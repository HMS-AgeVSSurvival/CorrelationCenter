#!/bin/bash

find . -name "*.py" ! -path './env_o2/*' -exec black {} \;