# Study Appraisal Methodology (living document)

Version: 2026-10-11.1 · Read by [SKILL.md](../SKILL.md) at Step 1 of every appraisal. Kept separate so a
refresh can change the checklist without touching the skill. Schedule in `evergreen.json`, findings in
[RESEARCH.md](../RESEARCH.md), every change in [CHANGELOG.md](../CHANGELOG.md); retrieval routes in
[fetch-routes.md](fetch-routes.md).

## 1. Provenance & citation integrity
- Locate the primary source. Verify the citation actually matches: authors, journal, year,
  DOI must resolve to the claimed paper. A mismatched or invented citation is the hallmark
  of AI content farms: it discredits the article even when the linked paper is real.
- Map the messenger chain: paper → press release → aggregator/blog/social. Compare claims
  at each hop; look for press-release fingerprints (identical phrasing, quotes only from PR).
- Check integrity status: Retraction Watch Database, PubPeer comments on the paper. Also check
  the paper's load-bearing citations (the meta-analysis or headline study it leans on): the
  Crossref record (`api.crossref.org/works/<DOI>`) carries retraction and correction notices.
  Since Jan 2025 the Retraction Watch database is inside the Crossref API (filter
  `update-type:retraction`; also a daily CSV at gitlab.com/crossref/retraction-watch-data). Crossref
  calls retractions comprehensive but corrections and expressions of concern incomplete, so check
  PubPeer and the journal page for an EoC. For a venue you don't know, run the Retraction Watch
  Hijacked Journal Checker.
- Sample recycling: scan the author's other papers from the surrounding 12 months. Same
  demographic, similar n, overlapping submission dates = likely the same dataset sliced twice;
  the abstract's "N participants" then reads more general than the sample is.
- Publication-status drift. A preprint does not stay one. When the article under review is more
  than a few months old, re-check the paper's status NOW: published, retracted, superseded by a
  later version? In economics and the quantitative social sciences a working paper often
  circulates two years or more before a journal accepts it, and neither Crossref nor RePEc
  shows the accepted version. The author's own homepage or CV is usually the only place that
  says "accepted at <journal>", so check it. Grade the article against what was knowable when
  it was written, and report the paper's current status separately.
- Mirror check on the article's own recency claim. Compare the article's date to the paper's. An
  outlet calling a 15-month-old paper "new" has manufactured the freshness, and a gap that long
  is usually long enough for the same team to have published again from the same sample. Search
  for later papers on the same trial or cohort before writing; a companion paper the article
  ignores belongs in the review.

## 2. Venue
- Peer-reviewed journal vs preprint vs conference abstract. Preprint ≠ wrong, but unvetted.
- Journal legitimacy: indexed (MEDLINE/Scopus)? Reputable publisher? Predatory signs:
  fake metrics, pay-to-publish spam, absurdly broad scope, days-long "peer review".
- Paper-mill era (2025-26): fraud is industrial. Screening tools now in use include
  Papermill Alarm (Clear Skies), STM Integrity Hub, Pangram (AI-generated text),
  Grounded AI (citation-context); a 2025 ML screen flagged 250k+ suspect cancer papers.
  Suspect: template phrasing, tortured phrases, unverifiable data/authors, citation rings.

## 3. Design vs claim
- Hierarchy: systematic review/meta-analysis > RCT > prospective cohort > case-control /
  cross-sectional > case series > mechanistic/anecdote. Does the design carry the claim?
- Cross-sectional and case-control designs support association only: police causal verbs
  ("causes", "leads to", "debunks", "proves").
- RCTs: CONSORT 2025 statement (30 items; new: prespecification changes, harms, data
  sharing, intervention delivery, patient involvement). Prospective registration? Primary
  outcome switching?
- Non-randomized: confounding control, selection (treatment-seeking vs population-based),
  reverse causation. Tools: Cochrane RoB 2 (RCTs), ROBINS-I v2 (2025), GRADE for
  body-of-evidence certainty (GRADE Book supersedes the Handbook by end of 2026;
  GRADErater automation in testing).
- Single-arm pre/post (feasibility pilots, open-label extensions, most supplement trials): there
  is no counterfactual, so every within-person change carries practice effects, placebo, regression
  to the mean and natural history inside it. Three checks.
  (a) Find the registered primary outcome and read it literally. Feasibility pilots almost always
  name compliance or retention; the efficacy measures are secondary and openly unpowered. Get the
  published protocol paper, not just the registry record: protocols state the power position in the
  authors' own words ("formal estimates of power are not required"), which is the cleanest quote
  there is against an efficacy headline. ClinicalTrials.gov is robots-blocked to WebFetch, so the
  protocol paper is usually the faster route anyway ([fetch-routes.md](fetch-routes.md)).
  (b) Hold-out / negative-control outcome. Search the battery for a measure that theory says should
  NOT respond to the intervention: a crystallized or premorbid-IQ test in a cognition study, a
  symptom the agent has no mechanism for, an outcome fixed before exposure could act. If it moved,
  it calibrates the artifact floor for every other outcome measured the same way. If it moved the
  MOST, the battery is measuring repetition. Put the hold-out result next to the headline result;
  that comparison does more work than any argument about the p-values.
  (c) Count the outcomes, say which survive a multiplicity correction, then say plainly that
  surviving correction is not the same as surviving the missing control arm. Multiplicity and
  confounding are separate objections; conflating them lets the paper off the harder one.
- Equivalence and non-inferiority claims (any trial or article saying "equivalent", "as good as",
  "no different from"): find the prespecified margin, the largest difference the authors call
  unimportant. Equivalence is shown only when the whole CI (90% for TOST, the two one-sided tests
  convention) sits inside ±margin. "Equivalence defined as P > 0.05" is absence of evidence relabelled
  as evidence of absence, and it gets easier the fewer people finish. If no margin is stated, use the
  difference the power calculation was built on as the authors' implied margin and run the check
  yourself on their reported CIs, in each sensitivity analysis. Say which way the CI escapes the margin:
  a comparator that might be better is a different story from one that might be worse. Reporting
  standard: CONSORT extension for non-inferiority/equivalence trials (Piaggio, JAMA 2012); a CONSORT
  2025-aligned version is registered with EQUATOR as under development (May 2025).
- Comparator and phase design in sponsored trials. Ask who was enrolled relative to the product: a
  trial of habitual users randomised to "continue" vs "quit" answers a different question from one in
  naive users or one against the product's real competitor (SWITCH 2026: 76% habitual diet-drink users,
  no sugar-sweetened arm). Check whether the headline timepoint was in the original protocol; a
  voluntary extension added by amendment self-selects its completers. Check the n behind each
  secondary outcome: "no harm" read off a subsample (31 blood draws of 220 completers) is unpowered in
  both directions, and the direction of the few significant secondaries matters for spin.
- Umbrella reviews and meta-meta-analyses (reviews of meta-analyses): an umbrella can never hold
  more information than the primary studies underneath it. Check (a) overlap, as the corrected
  covered area (CCA): high overlap means several meta-analyses re-count the same cohorts, so seven
  reviews may be one evidence base viewed seven ways; (b) the AMSTAR-2 ratings of what was pooled
  (the BMJ 2025 paracetamol umbrella rated 7 of 9 reviews critically low); (c) whether the
  quality-restricted estimates are reported with CIs. "Attenuated and, in several models,
  approached the null" with no numbers in the abstract is a conclusion without its evidence;
  "several" also means not all.
- Confounding-design check for observational exposure-outcome claims. When a common exposure (a
  drug, a food, screen time) is linked to a heritable outcome, familial confounding is the default
  suspect. Look for (a) sibling comparisons, which cancel shared genes and household, and (b)
  negative-control exposures: the same exposure at a time it cannot act (before pregnancy, paternal
  use, after diagnosis). A negative control carrying an association as large as the real exposure
  (Luo 2026: pre-pregnancy paracetamol HR 1.12/1.24 vs the pooled pregnancy RR 1.17/1.29) says the
  signal comes from who gets exposed. This is the observational twin of the single-arm hold-out
  outcome. Also give the pro-causal side its best argument: exposure misclassification biases
  toward the null, and sibling designs amplify it because only discordant pairs carry information.
  Say whether the negative control answers that argument.
- Qualitative (interviews, focus groups, thematic analysis): report against COREQ (32 items)
  or SRQR. Supports description of experience, never a "toll", "effect", or "impact" claim.
  Check: number of coders (single author = single coder), reflexivity statement, saturation,
  member checking, and whether participants were selected on the exposure (recruiting only
  heavy users and then finding dependence themes is circular). Self-reported perception of a
  cognitive change is not a cognitive measure; say so explicitly in the verdict.
- Quantitative observational (cohort/panel regressions; economics, epidemiology, psych): the
  claim rests entirely on controls, so read the specification table, not the abstract. Check:
  (a) Coefficient movement across specifications. How far does the headline estimate shrink as
  controls are added? A drop from 0.039 to 0.026 when cognition, SES and schooling enter says a
  third of the raw association was measurable confounding, and raises the obvious question about
  the confounding nobody could measure. Report the sequence, never the best-looking column;
  Oster-style bounds quantify this when the authors supply them.
  (b) Units. Economics reports effects per standard deviation of the exposure, usually in log
  points, where a coefficient of 0.026 means roughly 2.6%. Translate before judging size.
  (c) Post-treatment controls: a variable measured after the exposure (schooling, occupation)
  can absorb the very mechanism under study, so the "fully controlled" column may be the wrong
  one to headline.
  (d) The authors' own causal language. A good observational paper contains an explicit
  disclaimer sentence; find it and quote it next to the article's headline.
  (e) Coarse controls leave residual confounding. A confounder entered as years of schooling or
  highest degree is measured with error (school quality, homeschooling and reading at home all
  vanish into one number), and whatever the control misses leaks into the exposure's coefficient.
  So "persists after controlling for education" is a fair claim, while "not reducible to
  education" is a stronger one the design can't make. Watch for that upgrade in abstracts.
- N-of-1 self-tracking (wellness videos and posts: one person's repeated lab tests read against a
  diet or habit log, with population studies borrowed to set targets). Grade the cited studies and
  the personal analysis separately; the first can be solid while the second is weak. Check:
  (a) Matrix and units. Are the personal numbers measured on the same sample type and assay as the
  population cut-off? Finger-prick or dried whole blood is not venous plasma (whole-blood
  tryptophan runs near half the plasma value). If every personal point falls past a population
  extreme, suspect the matrix before the biology.
  (b) Time is the confounder. Over a few years, age and calendar date are one variable, so a
  personal trend called "age-related" also carries kit, lab and handling changes and every habit
  that drifted. Compare the slope to the cited population aging slope; one many times faster is
  not aging. Any input that trended will correlate with a trending outcome, so ask whether the model
  includes test date or detrends.
  (c) Count the inputs screened. A food log plus an app's nutrient totals is dozens to hundreds of
  tests against 20-30 blood draws; at p < 0.05, about 5 hits per 100 inputs come from noise. If the
  count isn't given, say the hit list can't be judged.
  (d) Home-made indices. A ratio whose denominator is the headline variable restates it; a rising
  ratio "supporting" a falling denominator is the same evidence counted twice. Ask whether the index
  was ever validated against a direct measure.
  (e) The seller of the measurement. When the presenter earns from the test kit or the tracking app,
  say so even when it's disclosed; it predicts that the measurement gets read as finding a problem.

## 4. Sample & measurement
- N per group, especially controls. In pooled/multi-cohort studies, check whether the
  flashiest number comes from the smallest or most biased subsample.
- Sampling frame: clinic patients vs general population; demographic bounds on generalizing.
- Proxy alert: is the measured quantity what the headline says? (BOLD synchrony ≠ blood
  flow; food-frequency surveys ≠ diet; self-report ≠ behavior.)
- Composite and latent exposures. When the exposure is a factor score, index, or composite
  rather than one measured thing, get the item list and the loadings before accepting the label.
  The score is a weighted sum of its items, so two people with completely different item
  profiles land on the same number. Ask: could someone score high on this without the behaviour
  named in the headline? If yes, the headline is about a construct nobody measured. Naming a
  factor after one of its high-loading items is the most common quiet error in psychology and
  economics coverage, and it sticks because the factor's own name is an author's choice too.
  Quote the loadings in the verdict; the list is usually more persuasive than the argument.
- Ability and knowledge exposures (cognitive-epidemiology and "IQ predicts attitude X" papers).
  A short vocabulary test (GSS Wordsum: 10 items) measures crystallized knowledge, which grows
  with reading, schooling quality and home language, not reasoning capacity alone. When the
  outcome is a cultural or religious position, the reverse path is live: the same subculture
  can shape both reading habits and the belief (Sherkat, JSSR 2022, on fundamentalism and
  Wordsum). Check whether fluid measures (abstract reasoning, numeracy) agree, and with what n;
  in long-running surveys such modules usually ran in fewer waves than the headline measure. Calling Wordsum "verbal
  intelligence" or "cognitive ability" in the headline is a proxy upgrade; grade it as one.
- Single-item outcomes standing in for a scale. When the headline construct normally has a
  validated multi-item scale (Christian nationalism, loneliness, wellbeing) and the paper uses
  one or two survey items because that is what a long-running survey carried, say so. Read
  each item literally and ask what else it measures: an item about a court ruling partly
  measures civics knowledge, which correlates with the exposure by construction.
- Long-horizon attrition. In multi-decade cohorts, state retention from the baseline wave to the
  outcome wave as a number (e.g. 14,870 children at age 10 → 6,952 in the wage regressions,
  47%). Then ask whether dropout correlates with the exposure, and which way the resulting bias
  runs. Losing the exposed people whose lives went worst turns a null into a positive finding
  with nobody doing anything wrong.

## 5. Statistics
- Effect sizes with CIs, not just p-values. Tiny d with huge N = real but possibly trivial.
- Multiple-comparisons handling; subgroup fishing; composite indices that amplify weak
  signals; clusters of p just under .05; internal inconsistencies between reported numbers.
- Replication context: independent reproduction? Single-study novelty in replication-crisis
  fields (social psych, nutrition epi, candidate genes, small-N neuroimaging) gets a lower prior.
  When looking for a replication, check the cohort: the same finding in the same dataset is not
  one. A different national cohort, a different birth year, same sign is.
- Translate the headline effect into something a reader can feel: a percentile of the exposure
  plus a concrete unit (percent, years, currency, absolute risk per 1,000). Label it as your own
  arithmetic on their coefficient, not a number from the paper. "Precisely estimated and small"
  is a common and useful verdict; both halves of it need saying.
- When no magnitude is reachable (paywalled, outlet reported only "significant"), say so in the
  verdict, note that a large N makes significance cheap, and name the one number to look for
  if the PDF turns up (usually the coefficient's movement from the bare model to the full one).
  Don't invent a translation.

## 6. Interests
- COI declarations vs author affiliations: a commercial affiliation with no matching
  disclosure is a red flag in its own right.
- Funding source and its role. Who is promoting the finding, and what do they sell?
- Contested-citation check: when an article leans on a secondary source (e.g., a famous
  review), check how the field actually received that source.

## 7. Spin delta
- Quote the paper's own hedged conclusion next to the article's claim. Grade the
  exaggeration: none / mild / severe / fabricated.
- Grade omission as well as exaggeration. A two-sided result reported one-sided is spin even
  when every quoted sentence is accurate: if the same table carries a larger finding in the
  unsurprising direction and the article skips it, say so.
- Association vs causation inversion. "Not linked" or "no link" for a paper that found an
  association and argued it is not causal is spin in the reassuring direction. It is common in
  debunking coverage because the practical takeaway is correct. Grade it (usually mild) and give the
  accurate headline ("linked, but probably not causally").
- Locate the hop that added the claim. Causal language can enter at the paper ("appeals to"),
  the press release, the author's interview with the outlet, or the outlet's headline. Grade
  each hop separately: an outlet that faithfully quotes an author's overconfident interview is
  not the spinner, and blaming the journalist for it misreads the chain.
- Check the outlet's standing thesis. A blog with a named angle (a contrarian book, a
  newsletter with a thesis) selects which half of a result gets written up. That is not fraud
  and should not be graded as fraud, but it explains the selection and belongs in the review.
  The same goes for the author: a scholar whose books argue a thesis isn't conflicted in the
  financial sense, but it predicts which way the framing leans. Say it; don't grade it as a COI.

## 8. Verdict scale

| Verdict | Meaning |
|---|---|
| Solid | sound design for the claim, decent venue, meaningful effects, faithful reporting |
| Real but overhyped | legitimate study, distorted framing (in coverage, or in the paper's own abstract and the author's interviews; say which hop) |
| Weak | real but underpowered, confounded, or proxy-measured beyond its claims |
| Junk / predatory | venue or methods disqualifying |
| Fabricated / misattributed | citation doesn't check out, or integrity flags on the paper |

## Changelog
Full history with reasons: [CHANGELOG.md](../CHANGELOG.md). The C- ids below were assigned before the
skill was published; the public changelog summarises them under its first entry.
- 2026-10-11 (v8): §3 n-of-1 self-tracking branch (matrix and units vs the population cut-off,
  time as the confounder, count the inputs screened, home-made indices, the seller of the
  measurement). Source: C-20261011-2.
- 2026-10-01 (v7): §3 coarse controls leave residual confounding ("persists after" vs "not
  reducible to"). §4 ability/knowledge exposures (vocabulary is crystallized, reverse path via
  subculture, check fluid measures and their n) and single-item outcomes standing in for a
  scale. §5 what to say when no magnitude is reachable. §7 locate the hop that added the causal
  claim; author's standing thesis. §8 "overhyped" can originate upstream of coverage.
  Source: C-20261001-1.
- 2026-09-30 (v6): §3 equivalence/non-inferiority check (prespecified margin, 90% CI inside ±margin,
  implied margin from the power calculation, "P > 0.05 = equivalent" as an error) and a
  sponsored-trial comparator/phase check (habitual users, amended extensions, subsample n behind
  "no harm"). §1 Retraction Watch data via Crossref, EoC gap, Hijacked Journal Checker. Sources:
  C-20260930-1, C-20260930-2.
- 2026-09-28 (v5): §3 umbrella-review branch (overlap/CCA, AMSTAR-2 of the pooled reviews, restricted
  estimates with CIs) and a confounding-design check (sibling comparisons, negative-control
  exposures, and the misclassification counter-argument). §7 association-vs-causation inversion
  ("not linked") as reassuring-direction spin. Source: C-20260928-1.
- 2026-09-16 (v4): §3 single-arm pre/post branch (registered primary outcome read literally, the
  protocol paper's own power statement, the hold-out / negative-control outcome as the artifact
  floor, and multiplicity vs the missing control arm as separate objections). §1 mirror check on
  the article's recency claim and on companion papers from the same sample. Source: C-20260916-1.
- 2026-09-15 (v3): §1 publication-status drift (a working paper's status changes; the author's
  homepage is often the only source). §3 quantitative-observational branch (coefficient movement
  across specifications, per-SD log-point units, post-treatment controls, the authors' own causal
  disclaimer). §4 composite/latent exposures (get the loadings; a factor is not its loudest item)
  and long-horizon cohort attrition as a stated retention number with a bias direction. §5
  same-dataset vs same-finding for replication, and translate the effect into a felt unit. §7
  omission as spin, and the outlet's standing thesis. Source: C-20260915-1.
- 2026-09-02 (v2): Added qualitative branch to §3 (COREQ/SRQR, single-coder, selection on
  exposure, perception ≠ measure); §1 now checks load-bearing citations for retraction and
  scans for sample recycling across an author's recent papers. Source: C-20260902-2.
- 2026-08-31 (v1): Initial baseline. Sources: CONSORT 2025 statement (BMJ/Lancet/Nat Med,
  Apr 2025); GRADE Book transition + GRADErater; ROBINS-I v2 (2025); Cochrane Methods
  Report 2025; paper-mill detection landscape 2025-26 (Clear Skies, STM Integrity Hub,
  Pangram, Grounded AI).
