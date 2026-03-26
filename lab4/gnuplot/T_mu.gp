# Graph 3.1: T(n) for various mu values
# N=1000, lambda=1e-3, m=1, mu in {1, 2, 4, 6}

set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/T_mu.png"

set title "Среднее время восстановления (N = 1000, {/Symbol l} = 10^{-3} 1/ч, m = 1)"
set xlabel "Число машин n в основной подсистеме"
set ylabel "Среднее время восстановления (часы)"
set logscale y
set grid
set key top right

set xrange [899:1001]
set format y "%g"

plot "../data/T_mu.dat" using 1:2 title "{/Symbol m} = 1 1/ч" with linespoints pt 1 lw 1.5, \
     "../data/T_mu.dat" using 1:3 title "{/Symbol m} = 2 1/ч" with linespoints pt 2 lw 1.5, \
     "../data/T_mu.dat" using 1:4 title "{/Symbol m} = 4 1/ч" with linespoints pt 3 lw 1.5, \
     "../data/T_mu.dat" using 1:5 title "{/Symbol m} = 6 1/ч" with linespoints pt 4 lw 1.5
