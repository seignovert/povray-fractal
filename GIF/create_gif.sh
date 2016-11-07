for f in $(ls *.png)
do
    convert -fill "#FFFFFF" -opaque none $f ${f%.png}.jpg
    rm $f
done

convert -delay 10 -loop 0 *.jpg animated.gif
