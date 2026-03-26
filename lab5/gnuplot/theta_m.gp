set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/theta_m.png"

set title "Компоненты вектора {/Symbol q}_k (N = 65536, {/Symbol l} = 10^{-5} 1/ч, {/Symbol m} = 1 1/ч)"
set xlabel "Число работоспособных машин k"
set ylabel "{/Symbol q}_k (часы)"
set logscale y
set grid
set key top right

set xrange [65526:65537]
set format y "10^{%L}"

plot "../data/theta_m.dat" using 1:2 title "m = 1" with linespoints pt 1 lw 1.5, \
     "../data/theta_m.dat" using 1:3 title "m = 2" with linespoints pt 2 lw 1.5, \
     "../data/theta_m.dat" using 1:4 title "m = 3" with linespoints pt 3 lw 1.5
