set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/theta_n_start.png"

set title "Вектор среднего времени безотказной работы ВС: зависимость {/Symbol q}_{n_start} от n_start (N = 65536, {/Symbol l} = 10^{-5} 1/ч, {/Symbol m} = 1 1/ч, m = 1)"
set xlabel "Минимально допустимое число работоспособных машин n_start"
set ylabel "{/Symbol q}_{n_start} (часы)"
set logscale y
set grid
set key top right

set xrange [65526:65537]
set format y "10^{%L}"

plot "../data/theta_n_start.dat" using 1:2 title "{/Symbol q}_{n_start}" with linespoints pt 5 lw 1.8

