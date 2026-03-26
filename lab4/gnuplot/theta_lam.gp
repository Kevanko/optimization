# Graph 2.2: Theta(n) for various lambda values
# N=65536, mu=1, m=1, lambda in {1e-5..1e-9}

set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/theta_lam.png"

set title "Среднее время наработки до отказа (N = 65536, {/Symbol m} = 1 1/ч, m = 1)"
set xlabel "Число машин n в основной подсистеме"
set ylabel "Среднее время до отказа (часы)"
set logscale y
set grid
set key top right

set xrange [65526:65537]
set format y "10^{%L}"

plot "../data/theta_lam.dat" using 1:2 title "{/Symbol l} = 10^{-5} 1/ч" with linespoints pt 1 lw 1.5, \
     "../data/theta_lam.dat" using 1:3 title "{/Symbol l} = 10^{-6} 1/ч" with linespoints pt 2 lw 1.5, \
     "../data/theta_lam.dat" using 1:4 title "{/Symbol l} = 10^{-7} 1/ч" with linespoints pt 3 lw 1.5, \
     "../data/theta_lam.dat" using 1:5 title "{/Symbol l} = 10^{-8} 1/ч" with linespoints pt 4 lw 1.5, \
     "../data/theta_lam.dat" using 1:6 title "{/Symbol l} = 10^{-9} 1/ч" with linespoints pt 5 lw 1.5
