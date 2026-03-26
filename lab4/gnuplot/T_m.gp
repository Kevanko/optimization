# Graph 3.3: T(n) for various m values
# N=8192, mu=1, lambda=1e-5, m in {1,2,3,4}

set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/T_m.png"

set title "Среднее время восстановления (N = 8192, {/Symbol l} = 10^{-5} 1/ч, {/Symbol m} = 1 1/ч)"
set xlabel "Число машин n в основной подсистеме"
set ylabel "Среднее время восстановления (часы)"
set grid
set key top right

set xrange [8091:8193]

plot "../data/T_m.dat" using 1:2 title "m = 1" with linespoints pt 1 lw 1.5, \
     "../data/T_m.dat" using 1:3 title "m = 2" with linespoints pt 2 lw 1.5, \
     "../data/T_m.dat" using 1:4 title "m = 3" with linespoints pt 3 lw 1.5, \
     "../data/T_m.dat" using 1:5 title "m = 4" with linespoints pt 4 lw 1.5
