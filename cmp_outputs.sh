#!/bin/bash

total=0
correct=0
for test in  ./test/*; do
    for i in {0..1}; do
        if diff "${test}/saida${i}.csv" "${test}/esperado${i}.csv"  > /dev/null 2>&1
        then
            correct=$((correct + 1))
        fi
    done
    total=$((total + 2))
done

echo "Results ${correct}/${total}"
