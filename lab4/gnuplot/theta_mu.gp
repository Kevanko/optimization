# Graph 2.1: Theta(n) for various mu values
# N=65536, lambda=1e-5, m=1, mu in {1, 10, 100, 1000}

set terminal pngcairo size 900,600 enhanced font "Arial,11"
set output "../plots/theta_mu.png"

set title "Mean time between failures (N = 65536, {/Symbol l} = 10^{-5} hours^{-1}, m = 1)"
set xlabel "Number n of elementary machines in base subsystem"
set ylabel "Mean time between failures (hours)"
set logscale y
set grid
set key top right

set xrange [65526:65537]
set format y "10^{%L}"

plot "../data/theta_mu.dat" using 1:2 title "{/Symbol m} = 1 1/hours"   with linespoints pt 1 lw 1.5, \
     "../data/theta_mu.dat" using 1:3 title "{/Symbol m} = 10 1/hours"  with linespoints pt 2 lw 1.5, \
     "../data/theta_mu.dat" using 1:4 title "{/Symbol m} = 100 1/hours" with linespoints pt 3 lw 1.5, \
     "../data/theta_mu.dat" using 1:5 title "{/Symbol m} = 1000 1/hours" with linespoints pt 4 lw 1.5
