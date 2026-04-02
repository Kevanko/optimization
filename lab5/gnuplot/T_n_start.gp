set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/T_n_start.png"

set title "Вектор среднего времени восстановления ВС: зависимость T_{n_start} от n_start (N = 65536, {/Symbol l} = 10^{-5} 1/ч, {/Symbol m} = 1 1/ч, m = 1)"
set xlabel "Минимально допустимое число работоспособных машин n_start"
set ylabel "T_{n_start} (часы)"
set grid
set key top right

set xrange [65526:65537]

plot "../data/T_n_start.dat" using 1:2 title "T_{n_start}" with linespoints pt 5 lw 1.8
