# Verification results: Guo et al. (2017), "first" claims (H1), Bhurane 93.96% (H2)

**Run:** 3 November 2026, using Firecrawl (web search, page scrape, research paper index covering PubMed, bioRxiv, medRxiv and arXiv) and Consensus.
**Feeds:** `drafts/proposal_revisions_draft.md` (E4d reference; issue map rows H1 and H2).

---

## 1. Guo et al. (2017): verified

Source: the PMLR proceedings page, https://proceedings.mlr.press/v70/guo17a.html

| Field | PMLR record | Draft E4d |
|---|---|---|
| Authors | Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger | Same |
| Proceedings | Proceedings of the 34th International Conference on Machine Learning | Same |
| Editors | Doina Precup, Yee Whye Teh | Same |
| Series and volume | Proceedings of Machine Learning Research, Vol. 70 | Same |
| Pages | **1321–1330** | Same |
| Year | 2017 | Same |

**Status:** the E4d reference is correct as drafted. Optionally add the URL at the end:

```
REF|Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q. (2017). On calibration of modern neural networks. In D. Precup & Y. W. Teh (Eds.), *Proceedings of the 34th International Conference on Machine Learning* (Vol. 70, pp. 1321–1330). PMLR. https://proceedings.mlr.press/v70/guo17a.html
```

The paper also supports the E4 wording: temperature scaling is "a single-parameter variant of Platt Scaling" and "surprisingly effective at calibrating predictions".

---

## 2. Bhurane et al. (2026), 93.96%: confirmed

Source: the IEEE Xplore abstract, https://ieeexplore.ieee.org/document/11517622 (DOI 10.1109/CSPA68262.2026.11517622). The full text was not accessed.

What the abstract says:
- **Data:** the NIH-funded Pulsewatch dataset, "106 subjects recorded in real-life settings for 14 days"; raw single-channel PPG only.
- **Model:** "Tiny-ResNet" with 23,727 trainable parameters.
- **Results on the test set:** overall accuracy **98.00%**. For the PAC/PVC class: **sensitivity 93.96%**, specificity 98.80%, F1 92%. For AF: sensitivity 99.20%, specificity 99.00%.
- **Split:** the abstract does not say whether testing was subject-independent.

**Consequences:**
- Table 2.1 "PAC/PVC sensitivity 83% to 94% (Han et al., 2026; Bhurane et al., 2026)" is correct. The 94% is Bhurane's 93.96%, rounded.
- Table 2.2 "accuracy 98.0%" is correct.
- Keep the existing caveat in the `gaps.html` speaker notes: the split is not reported, so 93.96% is not directly comparable with Han et al.'s 83% on 72 held-out subjects.
- Table 2.2 says "full text not accessed". That is still true; the confirmation comes from the abstract.
- The abstract's "recorded … for 14 days" supports the Pulsewatch multi-day premise behind the optional E2 clause. Timestamp continuity still needs `Check_E2_Pulsewatch_Timestamps.md`.

---

## 3. "First" claims (H1)

The proposal makes two novelty claims (Section 2.7, abstract and Section 5.1):

- **Claim A:** no smartwatch or PPG-derived daily PAC count validated against ECG.
- **Claim B:** "in these databases, no graph neural network applied to PPG or inter-beat-interval series for arrhythmia".

### What was searched

| Source | Queries (summary) |
|---|---|
| arXiv | Firecrawl web search restricted to `site:arxiv.org`: GNN with PPG, inter-beat interval or RR interval and atrial fibrillation; the Firecrawl research index (includes arXiv) with three framings |
| IEEE Xplore | Firecrawl web search restricted to `site:ieeexplore.ieee.org`: GNN, photoplethysmography and arrhythmia; plus the Bhurane record |
| PubMed, bioRxiv, medRxiv | Firecrawl research index: GNN on PPG or IBI for arrhythmia; graph or visibility-graph methods on pulse-interval series; PPG or smartwatch PAC burden against Holter |
| Consensus | GNN with PPG or RR intervals for AF or premature beats; smartwatch PPG PAC burden against Holter |

**Limit:** IEEE Xplore was searched through a web index restricted to its domain, not through IEEE Xplore's own search engine. Before the proposal names IEEE Xplore as a searched database, run the native search yourself (Section 3.4).

### Claim A, daily PAC count: holds

No study was found that reports a smartwatch- or PPG-derived **PAC** count or burden validated against ECG. Every count-level validation found is for **AF burden**:
- Poh et al. (2023), Verily watch against a 14-day Zio patch: R² = 0.986.
- Zhao et al. (2024): R² = 0.996.
- Zuo et al. (2026), 728 patients: r = 0.999. This study is already cited.
- Pan et al. (2025), Amazfit against a 7-day Holter: ICC 0.976.
- Anagnostopoulos et al. (2025): a meta-analysis of six AF-burden studies.

The nearest PAC work:
- **Kwon et al. (2019)** used a "PAC indicator" to estimate the share of PPG samples containing PACs (29.79% of post-cardioversion samples). That is a sample-level flag, not a validated count against ECG.
- **Han et al. (2020, 2026)** and **Bhurane et al. (2026)** classify windows only.

**Useful for the defence:** count-level validation is established for AF burden but not for PAC burden. That makes the gap concrete. Optionally, one AF-burden study could be cited in Section 2.4 as the analogue, but that costs words.

**Garmin-specific find:** Chang et al. (2022, *American Heart Journal*) ran 24-hour simultaneous Garmin smartwatch PPG with Holter ECG in 200 participants for AF detection. It is a Garmin precedent for continuous ambulatory recording. Consider it for Section 3.5 or the device answers.

### Claim B, GNN on PPG or IBI for arrhythmia: holds, keep it scoped

No study was found that applies a GNN to **PPG or inter-beat-interval series for arrhythmia**. Graph methods nearby, which an examiner might raise:

| Work | What it does | Why it does not break Claim B |
|---|---|---|
| ECG-GraphNet (2025, *Heart Rhythm O2*); visibility-graph GCN (arXiv 2404.15367); CNN-GNN-BiLSTM (2025, *Med Eng Phys*, "inter-beat relationships"); several others | GNNs on **ECG** beats or leads, N/S/V classification | ECG, not PPG or IBI. The visibility-graph GCN notes the S (supraventricular) class stays hard inter-patient, which supports the proposal's motivation |
| CiGNN (IEEE) | GNN on wearable PPG for **blood pressure** | PPG, but not arrhythmia. This is why the claim must keep "for arrhythmia" |
| Rivera-Juzga et al. (2025, *Comput Biol Med*; Lip co-author) | GNN predicting **new AF after stroke** from clinical data | Not signals. But it is the closest GNN work in the same clinical space |
| Visibility-graph analysis of RR series (e.g., Entropy 2023) | Graph features of heartbeat series, no GNN | Feature engineering, not a GNN |
| MGNN (2022) | Despite the name, a multiscale grouped **CNN** on RR intervals | Not a graph network |

**Recommendations:**
1. Keep Claim B worded as "for arrhythmia" and "to our knowledge".
2. **Prepare for Rivera-Juzga et al. (2025).** If asked "hasn't a GNN already been used for AF after stroke?", answer: "Yes, on clinical variables to predict AF. This study applies a graph network to beat intervals from a wearable to estimate ectopy, a different input and a different target." Cite it only if the word budget allows.
3. The visibility-graph GCN paper reports S-class difficulty, which supports the existing EPMoghaddam et al. (2024) point that graphs are tested, not assumed.

### 3.4 Run IEEE Xplore's own search (10 minutes) before naming it

Use https://ieeexplore.ieee.org/search/advanced with these queries, all years:
1. `("graph neural network" OR "graph convolutional" OR "graph attention") AND (photoplethysmograph* OR PPG OR "inter-beat interval" OR "pulse interval") AND (arrhythmia OR "atrial fibrillation" OR premature OR ectopic)`
2. `(smartwatch OR wearable OR photoplethysmograph*) AND ("premature atrial" OR "atrial ectopy" OR "supraventricular ectopic") AND (burden OR count OR "per day" OR "24-hour")`

Record the date and the number of hits screened. If nothing breaks either claim, the Section 2.7 sentence can name IEEE Xplore and arXiv (see 3.5).

### 3.5 Optional wording for Section 2.7 (+5 words)

**Current**
> Searches of PubMed, Consensus and Wiley Scholar Gateway in October 2026 found no smartwatch or PPG-derived daily PAC count validated against ECG, and, in these databases, no graph neural network applied to PPG or inter-beat-interval series for arrhythmia (Table 2.1).

**Proposed** (only after step 3.4)
> Searches of PubMed, Consensus, Wiley Scholar Gateway, IEEE Xplore and arXiv in October and November 2026 found no smartwatch or PPG-derived daily PAC count validated against ECG, and, in these databases, no graph neural network applied to PPG or inter-beat-interval series for arrhythmia (Table 2.1).

Word budget: the main draft is at about 6,989, so +5 gives about 6,994, still under 7,000.

---

## Sources

- Guo et al. (2017), PMLR: https://proceedings.mlr.press/v70/guo17a.html
- Bhurane et al. (2026), IEEE Xplore: https://ieeexplore.ieee.org/document/11517622
- Poh et al. (2023), JAHA: https://doi.org/10.1161/jaha.123.030543
- Zhao et al. (2024), PACE: https://doi.org/10.1111/pace.14951
- Zuo et al. (2026), JACC Clin EP: https://doi.org/10.1016/j.jacep.2026.03.036
- Pan et al. (2025), Digital Health: https://doi.org/10.1177/20552076251314105
- Anagnostopoulos et al. (2025), JCDD: https://doi.org/10.3390/jcdd12040122
- Kwon et al. (2019), JMIR mHealth uHealth: https://doi.org/10.2196/12770
- Chang et al. (2022), Am Heart J: https://doi.org/10.1016/j.ahj.2022.02.002
- ECG-GraphNet (2025), Heart Rhythm O2: https://doi.org/10.1016/j.hroo.2025.05.012
- Visibility-graph GCN (2024), arXiv: https://arxiv.org/abs/2404.15367
- CNN-GNN-BiLSTM (2025), Med Eng Phys: https://doi.org/10.1016/j.medengphy.2025.104418
- Rivera-Juzga et al. (2025), Comput Biol Med: https://doi.org/10.1016/j.compbiomed.2025.111095
- CiGNN, IEEE: https://ieeexplore.ieee.org/iel7/6221020/10521573/10472032.pdf
