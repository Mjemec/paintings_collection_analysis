#!/bin/sh

mkdirs() {

	for file in *.json
	do
		# echo "file: $file"
		time_period=$(cat "$file" | jq -r '.time_period' | cat)
		# echo "$time_period"
		mkdir -p "./$time_period"
	done

}

move() {

	echo "hello"
	for file in *.json
	do
		
		img=$(echo "$file" | sed 's/\.json$/.jpg/')
		# echo "img: $img"
		
		time_period=$(cat "$file" | jq -r '.time_period' | cat)
		# echo "time_period: $time_period"

		mv "$img" "${time_period}/"

	done

}

# mkdirs
move
