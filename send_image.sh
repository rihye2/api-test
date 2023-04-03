#!/bin/bash

img_name="1.jpg 2.jpg 3.jpg 4.jpg 5.jpg"

for img in $img_name;
do
	echo $img
	touch $img
done

mv *.jpg ./images/
