Kochen-Specker colorings of vectors and projections
=====================================================

This page contains code that was used to carry out computations for the paper 
[Minimal ring extensions of the integers exhibiting Kochen-Specker colorability](https://www.math.uci.edu/~mreyes/ks462.pdf). 

Given positive integers $d$ and $N$, we define a set 
```math
\mathcal{S}_d(N) = \{v \in \mathbb{Z}^d \mid \|v\|^2 \mbox{ divides a power of } d\}.
```
Much of the code here addresses the problem of determining whether $\mathcal{S}_d(N)$ has a Kochen-Specker colroing.
The Mathematica code was originally used to find an uncolorable subset of $\mathcal{S}_3(462)$. The Python code 
was used to explore larger values of $d$ and $N$, especially showing that $\mathcal{S}_6(3)$ is KS uncolorable.

There is also Python code that searches for colorings of projection matrices over the finite field $\mathbb{F}_2$.
