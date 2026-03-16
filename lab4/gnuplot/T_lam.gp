# Graph 3.2: T(n) for various lambda values
# N=8192, mu=1, m=1, lambda in {1e-5..1e-9}

set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/T_lam.png"

set title "Mean time to recovery (N = 8192, {/Symbol m} = 1 hours^{-1}, m = 1)"
set xlabel "Number n of elementary machines in base subsystem"
set ylabel "Mean time to recovery (hours)"
set grid
set key top right

set xrange [8091:8193]
set yrange [0.99:1.20]

plot "../data/T_lam.dat" using 1:2 title "{/Symbol l} = 10^{-5} 1/hours" with linespoints pt 1 lw 1.5, \
     "../data/T_lam.dat" using 1:3 title "{/Symbol l} = 10^{-6} 1/hours" with linespoints pt 2 lw 1.5, \
     "../data/T_lam.dat" using 1:4 title "{/Symbol l} = 10^{-7} 1/hours" with linespoints pt 3 lw 1.5, \
     "../data/T_lam.dat" using 1:5 title "{/Symbol l} = 10^{-8} 1/hours" with linespoints pt 4 lw 1.5, \
     "../data/T_lam.dat" using 1:6 title "{/Symbol l} = 10^{-9} 1/hours" with linespoints pt 5 lw 1.5
