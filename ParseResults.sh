#!/bin/bash

cd Lang

for i in {1..65}
	do
		tail -n +59 Lang${i}_Probability.txt > tmp_Lang${i}.txt
		rm Lang${i}_Probability.txt
		mv tmp_Lang${i}.txt Lang${i}_Probability.txt
	done
