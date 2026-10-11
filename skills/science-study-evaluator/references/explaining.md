# Explaining the appraisal

Read by [SKILL.md](../SKILL.md) at Step 3 while writing the review. People ask "is this legit?" because they want to understand the reasoning, not to receive a grade. A term named and left undefined costs the reader more than three extra paragraphs do (L-004). "Tight" means no filler; it never means skipping an explanation.

## Gloss on first use

Define each appraisal term the first time it appears in a review, in a clause, then use it freely. The ones that come up most:

- Design and bias: confidence interval, statistical power, preregistration, equivalence testing, non-inferiority margin, spin delta, winner's curse, differential attrition, practice effect, regression to the mean, target engagement, hold-out outcome, residual confounding, familial confounding, sibling comparison, negative-control exposure, exposure misclassification, post-treatment control, range restriction.
- Effect sizes and tests: Cohen's d and dz, standard error, per-SD and log-point coefficients, risk ratio and hazard ratio, absolute risk, Bonferroni correction, type I error, d′ (d-prime) and response criterion.
- Measurement: factor loading, composite index, crystallized vs fluid intelligence, proxy measure, single-item outcome.
- Evidence synthesis: umbrella review, AMSTAR-2, corrected covered area (CCA), GRADE certainty.

Add whatever else the particular review turns on.

## Analogies

Use one when it is exact, not decorative, and pick it from the reader's own field when you know it (the user's `reader.md` may say; see SKILL.md). These computing analogies have held up with technical readers:

| Idea | Analogy |
|---|---|
| Yes/no recognition test | A binary classifier: hit rate is recall, false-alarm rate is the false positive rate, d′ is separability, the response criterion is the decision threshold. Moving the threshold slides along the ROC curve without moving the curve, so a better hit rate with no change in d′ is a threshold shift, not better memory. |
| Factor score | A dot product of the item vector with the loading vector. Naming a factor after its loudest item is like naming a PCA component after one input feature. |
| Cohort attrition | A filter applied after the exposure: 47% retention means measuring uptime only on the servers still in the fleet. |
| Hold-out outcome in an uncontrolled trial | The no-op in a benchmark suite: if the function you never touched also got 20% faster, you measured the harness warming up, not your optimisation. The same idea covers a negative-control exposure in a cohort study. |
| Sibling comparison | Benchmarking two builds on the same machine, so the hardware drops out of the diff. |
| Umbrella review | A dashboard of dashboards; the corrected covered area is the duplicate-row rate across their joins. |
| Exposure misclassification | Label noise, which shrinks the measured separation between classes (bias toward the null). |
| Controlling for a coarse confounder | Deduplicating on a lossy hash: some duplicates get through, and they show up as the exposure's effect. |

For a reader with no technical background, everyday analogies work the same way (a bathroom scale that reads two pounds heavy for everyone still ranks people correctly; a survey of gym members about exercise habits). The test is the same: does the analogy have the same structure as the statistical problem?

## Translating the effect

Turn the headline coefficient into something a reader can feel: a percentile of the exposure plus a concrete unit (percent, years, currency, absolute risk per 1,000 people). Label it as your arithmetic on their numbers, not a number from the paper. When no magnitude is reachable (paywall, the outlet reported only "significant"), say so and don't invent one.
