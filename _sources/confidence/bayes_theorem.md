The [reverse probability page](first_bayes) has a game, that we analyzed by
simulation, and then by reflection.

The game is:

* I have two boxes; *BOX4* with 4 red balls and 1 green ball, and *BOX2* with
  two red balls and three green balls.
* I offer you one of these two boxes, with a 30% chance that I give you BOX4,
  and 70% chance I give you BOX2.
* You draw a ball at random from the box, and you get a red ball.
* What is the probability that I gave you BOX4?

We found by simulation, and later by reflection, that the probability is about
0.462.

The logic we discovered was:

* We want the proportion of "red" trials that came from BOX4.
* Calculate the proportion of trials that are *both* BOX4 and red, and divide
  by the overall proportion of red trials.

We found the proportion of red trials that are *both* BOX4 *and* red is (the
proportion of BOX4 trials) multiplied by (the proportion of BOX4 trials that
are red.

The logic above is a fundamental rule in probability called [Bayes
theorem](https://en.wikipedia.org/wiki/Bayes'_theorem).

In this page, we relate the logic above to the usual way of describing Bayes
theorem.

First we need some notation.

The probability that I give you BOX4 on any one trial is 0.3.

I write this as:

$$
P(BOX4) = 0.3
$$

Read this as "the probability of BOX4 is 0.3".

Similarly:

$$
P(BOX2) = 0.7
$$

The probability of getting a red ball, *given that* I am drawing from BOX4,
is 4/5 = 0.8.  We write "given" here with the bar: $\mid$.

$$
P(red \mid BOX4) = 0.8
$$

Read this as "the probability of drawing a red ball given I have BOX4 is 0.8".

Similarly:

$$
P(red \mid BOX2) = 0.4
$$

We follow the logic above, with this notation.  Here is the logic again:

1. We want the proportion of "red" trials that came from BOX4.
2. Calculate the proportion of trials that are *both* BOX4 and red, and divide
   by the overall proportion of red trials.

We can express the first statement by saying that we are trying to find
$P(BOX4 \mid red)$.

We have already found that that we get the probability of BOX4 *and* red by
multiplying the probability of BOX4 (0.3) by the probability of getting a red
ball, given BOX4 (0.8).  In our notation, this multiplication is $P(BOX4)
P(red \mid BOX4)$.

Remember too, from the [reverse probability page](first_bayes) that we found
$P(red)$ by adding the probabilities of the two different ways we can get
a red ball: $P(red) = P(red | BOX4) + P(red | BOX2)$.

Putting the first and second statements together into one, we get:

$$
P(BOX4 \mid red) = \frac{P(BOX4) P(red \mid BOX4)}{P(red)}
$$

This is Bayes theorem, although it is usually written with the multiplication
in the other order:

$$
P(BOX4 \mid red) = \frac{P(red \mid BOX4) P(BOX4)}{P(red)}
$$

See [Bayes theorem on Wikipedia](https://en.wikipedia.org/wiki/Bayes'_theorem)
for more detail.
