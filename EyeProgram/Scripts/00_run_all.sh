#!/bin/bash
echo "Run all Scripts"

for f in *py
do
	if [ "$f" != "SetupScript.py" ]
	then
		echo $f
		python3 "$f"
	fi
done

echo "All Done"
