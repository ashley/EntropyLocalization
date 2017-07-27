#!/bin/bash

cd Time

for i in {1..27}
	do
		tail -n +59 Time${i}.txt > tmp_Time${i}.txt
		rm Time${i}.txt
		mv tmp_Time${i}.txt Time${i}.txt
	done
