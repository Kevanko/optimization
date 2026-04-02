set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/theta_mu.png"

set title "Вектор среднего времени безотказной работы ВС: компоненты {/Symbol q}_k (N = 65536, {/Symbol l} = 10^{-5} 1/ч, m = 1)"
set xlabel "Число работоспособных машин k"
set ylabel "{/Symbol q}_k (часы)"
set logscale y
set grid
set key top right

set xrange [65526:65537]
set format y "10^{%L}"

plot "../data/theta_mu.dat" using 1:2 title "{/Symbol m} = 1 1/ч" with linespoints pt 1 lw 1.5, \
     "../data/theta_mu.dat" using 1:3 title "{/Symbol m} = 10 1/ч" with linespoints pt 2 lw 1.5, \
     "../data/theta_mu.dat" using 1:4 title "{/Symbol m} = 100 1/ч" with linespoints pt 3 lw 1.5, \
     "../data/theta_mu.dat" using 1:5 title "{/Symbol m} = 1000 1/ч" with linespoints pt 4 lw 1.5
