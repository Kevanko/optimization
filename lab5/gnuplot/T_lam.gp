set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/T_lam.png"

set title "Компоненты вектора T_k (N = 65536, {/Symbol m} = 1 1/ч, m = 1)"
set xlabel "Число работоспособных машин k"
set ylabel "T_k (часы)"
set grid
set key top right

set xrange [65526:65537]

plot "../data/T_lam.dat" using 1:2 title "{/Symbol l} = 10^{-5} 1/ч" with linespoints pt 1 lw 1.5, \
     "../data/T_lam.dat" using 1:3 title "{/Symbol l} = 10^{-6} 1/ч" with linespoints pt 2 lw 1.5, \
     "../data/T_lam.dat" using 1:4 title "{/Symbol l} = 10^{-7} 1/ч" with linespoints pt 3 lw 1.5
