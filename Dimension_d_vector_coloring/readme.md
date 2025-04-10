This code was used to test whether the subset of vectors $`\{v \in \mathbb{Z}^d \mid \|v\|^2 \mbox{ divides } N\}`$ has a Kochen-Specker coloring. It operates for dimensions $3 \leq d \leq 6$ and for any positive integer $N$. 

The test is run by calling the command vector_coloring(d,N). For instance, if one wants to locate the uncolorable subset of $\mathcal{S}_4(2)$, we can run vector_coloring(4,2**2) to search vectors whose square-norm goes up to $2^2$.
