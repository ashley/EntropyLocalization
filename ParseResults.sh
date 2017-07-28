#!/bin/bash

cd Time

for i in {1..27}
	do
		tail -n +59 Time${i}_Probability.txt > tmp_Time${i}.txt
		rm Time${i}_Probability.txt
		mv tmp_Time${i}.txt Time${i}_Probability.txt
	done
