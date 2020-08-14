# A sampling problem

We will soon find that we will need to think about randomness and probability
in order to give sensible answer to many questions.

We start with a legal question, about race discrimination in jury selection.

## Attribution

This page is partly from `Jury_Selection` of the UC Berkeley course \- see the
license file on the main website.

## The problem - was jury selection biased?

In 1963, a court in Talladega County, Alabama convicted a young black man called
Robert Swain of raping a white woman and sentenced him to death [^dp-note].
He appealed his sentence, citing among other factors the all-white jury. At
the time, only men aged 21 or older were allowed to serve on juries in
Talladega County. In the county, 26% of the eligible jurors were black, but
there were only 8 black men among the 100 selected for the jury panel in
Swain's trial.  No black man was selected for the trial jury.

[^dp-note]:
    In the end [Alabama could not execute
    Swain](https://law.justia.com/cases/alabama/supreme-court/1973/274-so-2d-305-1.html)
    because of a [later Supreme Court
    ruling](https://en.wikipedia.org/wiki/Furman_v._Georgia) on another case.

In 1965, the Supreme Court of the United States [denied Swain's
appeal](https://en.wikipedia.org/wiki/Swain_v._Alabama). In its ruling, the
Court wrote "... the overall percentage disparity has been small and reflects
no studied attempt to include or exclude a specified number of Negroes."

The percentage disparity in this case was 8% (the percentage of black jurors
on the jury panel) compared to 26% (the percentage of black people eligible
for jury service).  Is that disparity small?

How would we decide?

We will spend the next while building up the tools we need to answer this
question.
