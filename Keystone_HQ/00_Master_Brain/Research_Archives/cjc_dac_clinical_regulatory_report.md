# Clinical Science and Regulatory Status Report: CJC-1295 with DAC
**Date**: 2026-06-18  
**Subject**: CJC-1295 with Drug Affinity Complex (DAC) vs. CJC-1295 No-DAC (Modified GRF 1-29)  
**Target Folder**: `Research_Archives/cjc_dac_clinical_regulatory_report.md`  

---

## 1. Structural Chemistry & Molecular Modifications

CJC-1295 is a synthetic analog of human Growth Hormone-Releasing Hormone (GHRH), specifically based on the biologically active N-terminal 29-amino-acid fragment (GHRH 1-29, also known as Sermorelin). Native GHRH 1-29 has a very short plasma half-life (under 10 minutes) due to rapid degradation by the enzyme dipeptidyl peptidase-4 (DPP-4) between positions 2 and 3.

To resolve this limitation, CJC-1295 incorporates two major layers of chemical engineering: **tetra-substitution** for enzymatic resistance and **Drug Affinity Complex (DAC)** conjugation for serum protein binding.

### A. The 4 Amino Acid Substitutions (Mod GRF 1-29)
The core of CJC-1295 consists of **Modified GRF 1-29** (also known as tetrasubstituted GHRH 1-29 or CJC-1295 without DAC). It features four specific amino acid substitutions compared to native GHRH 1-29:

1. **D-Alanine at Position 2** (replacing L-Alanine): This stereochemical change prevents DPP-4 from identifying and cleaving the N-terminal peptide bond, extending half-life in circulation.
2. **Glutamine at Position 8** (replacing Asparagine): Prevents spontaneous deamidation, a major degradation pathway for peptides in aqueous environments.
3. **Alanine at Position 15** (replacing Glycine): Enhances hydrophobic stability and increases receptor affinity/bioactivity.
4. **Leucine at Position 27** (replacing Methionine): Replaces the highly oxidation-prone sulfur atom of methionine with a stable branched alkyl chain, increasing structural longevity.

* **Native GHRH 1-29 sequence (Sermorelin):**  
  `Tyr-Ala-Asp-Ala-Ile-Phe-Thr-Asn-Ser-Tyr-Arg-Lys-Val-Leu-Gly-Gln-Leu-Ser-Ala-Arg-Lys-Leu-Leu-Gln-Asp-Ile-Met-Ser-Arg-NH2`
* **Modified GRF 1-29 sequence (CJC-1295 No-DAC):**  
  `Tyr-D-Ala-Asp-Ala-Ile-Phe-Thr-Gln-Ser-Tyr-Arg-Lys-Val-Leu-Ala-Gln-Leu-Ser-Ala-Arg-Lys-Leu-Leu-Gln-Asp-Ile-Leu-Ser-Arg-NH2`

---

### B. The Drug Affinity Complex (DAC) & Albumin Binding
In the **CJC-1295 with DAC** variant, a 30th amino acid residue—**Lysine (Lys30)**—is added to the C-terminus of the Mod GRF 1-29 sequence. The $\epsilon$-amino group of this C-terminal Lysine is covalently conjugated to a **Maleimidopropionic Acid (MPA)** linker.

* **CJC-1295 with DAC Chemical Sequence:**  
  `Tyr-D-Ala-Asp-Ala-Ile-Phe-Thr-Gln-Ser-Tyr-Arg-Lys-Val-Leu-Ala-Gln-Leu-Ser-Ala-Arg-Lys-Leu-Leu-Gln-Asp-Ile-Leu-Ser-Arg-Lys(MPA)-NH2`
  *(Chemical Name: $N^\epsilon$-3-maleimidopropionyl-lysine30-[D-Ala2, Gln8, Ala15, Leu27]GHRH-(1-29) amide)*

#### Mechanism of Action:
Upon subcutaneous injection, the highly reactive electrophilic maleimide group of the MPA linker undergoes a rapid, selective, and irreversible covalent **Michael addition** reaction with the free thiol (sulfhydryl) group on **Cysteine-34 (Cys34)** of endogenous human serum albumin (HSA) in the bloodstream.

```
[Mod GRF 1-29 Peptide] - Lys(30) - [MPA Linker]
                                         |
                                (Covalent Bond)
                                         |
                            [Cys34 - Human Serum Albumin]
```

Since albumin is the most abundant circulating protein in blood plasma and has a long physiological half-life (~19 days), this covalent bioconjugation shields the peptide from renal filtration and enzymatic breakdown, extending the plasma half-life of CJC-1295 with DAC to **6–8 days** (compared to ~30 minutes for Mod GRF 1-29).

### C. Structural Comparison Table

| Metric/Feature | Mod GRF 1-29 (CJC-1295 No-DAC) | CJC-1295 with DAC |
| :--- | :--- | :--- |
| **Amino Acid Count** | 29 residues | 30 residues (29 + Lys30) |
| **Linker Molecule** | None | Maleimidopropionic Acid (MPA) |
| **Serum Binding** | None (circulates freely) | Covalent binding to Cysteine-34 on Serum Albumin |
| **Half-Life** | ~30 minutes | 6–8 days |
| **Dosing Cadence** | 1–3 daily subcutaneous injections | 1 weekly subcutaneous injection |
| **Cardiovascular/Bleed Risk** | Very Low (rapid clearance) | High (continuous GHRH stimulation) |

---

## 2. The Landmark 2006 Ionescu JCEM Study

### A. Study Metadata & Design
* **Citation:** Ionescu M, Frohman LA. *"Pulsatile Secretion of Growth Hormone (GH) Persists during Continuous Stimulation by CJC-1295, a Long-Acting GH-Releasing Hormone Analog, in Healthy Adults."* **The Journal of Clinical Endocrinology & Metabolism** (JCEM), 2006 Dec;91(12):4792-4797. (PMID: 17018654, DOI: 10.1210/jc.2006-1702).
* **Cohort:** Healthy adult volunteers (specifically young healthy men, aged 20–40, $n = 21$).
* **Methodology:** Frequent blood sampling was conducted at **20-minute intervals over a 12-hour overnight period** to evaluate the pharmacokinetic and pharmacodynamic effects of CJC-1295. Sampling was performed one week after a single subcutaneous administration of the peptide.

### B. Verified Quantitative Metrics

#### 1. Preservation of Pulsatility
The core finding of the study was that continuous exposure to the long-acting GHRH agonist **did not flatten or obliterate the natural pulsatile rhythm of growth hormone (GH) secretion**.
* **Pulse Frequency:** The number of secretory pulses remained unchanged (~5–6 pulses per 12 hours).
* **Pulse Amplitude:** The physiological peak amplitude was maintained or slightly enhanced, rather than being suppressed.

#### 2. Basal (Trough) GH Increase
While the pulsatile peaks remained distinct, the baseline level of circulating growth hormone (the valleys between pulses) was highly elevated.
* **Basal Concentration:** Basal (trough) GH levels increased **approximately 7.5-fold** (7.5x) compared to placebo.

#### 3. Mean GH & IGF-1 Concentration
* **Mean GH:** Overall mean GH concentration was significantly elevated (in a parallel escalating-dose trial by Teichman et al., 2006, single doses of CJC-1295 led to a **2- to 10-fold increase** in mean plasma GH sustained for 6+ days).
* **IGF-1 Increase:** Mean plasma IGF-1 (Insulin-like Growth Factor 1) levels increased **1.5- to 3-fold**, with elevations persisting for **9–11 days** following a single injection.

#### 4. Receptor Desensitization / Downregulation Findings
* In contrast to continuous infusions of native GHRH (which cause rapid GHRH receptor internalization, desensitization, and somatotrope exhaustion), continuous stimulation by CJC-1295 **did not cause pituitary desensitization**. Somatotropes remained responsive to endogenous hypothalamic inputs.

### C. Physiological Mechanism (The Somatostatin "Brake")
The biological reason GH pulsatility persists during continuous GHRH receptor stimulation is the hypothalamic-somatotrope feedback loop, driven by **Somatostatin (SST)**:

```
[Hypothalamus] ---> Releases Somatostatin in pulses (SST High/Low cycles)
      |
      v
[Pituitary Somatotropes] <--- Continuously stimulated by CJC-1295
      |
      +---> SST High phase: Somatostatin blocks GH release (CJC-1295 overridden)
      |
      +---> SST Low phase: Somatostatin brake lifts (CJC-1295 triggers robust GH pulse)
```

1. **Somatostatin Peaks:** Somatostatin is released from the hypothalamus in an ultradian, pulsatile pattern. During somatostatin secretory peaks, it acts as a dominant inhibitor on somatotrope cells, blocking GH secretion even when GHRH receptors are continuously occupied by CJC-1295.
2. **Somatostatin Valleys:** When hypothalamic somatostatin secretion drops, the inhibitory brake is released. The continuous stimulation of GHRH receptors by CJC-1295 immediately triggers a strong, synchronized release of GH.
3. **Prevention of Exhaustion:** Because somatotropes are periodically "shut off" by somatostatin, they avoid chronic over-stimulation and receptor internalization, maintaining their responsiveness over long periods.

---

## 3. FDA PCAC Hearing (December 4, 2024)

On December 4, 2024, the FDA’s Pharmacy Compounding Advisory Committee (PCAC) convened to evaluate several bulk drug substances—including CJC-1295 free base, CJC-1295 acetate, and various DAC formulations (free base, acetate, and trifluoroacetate)—for potential inclusion on the **503A Bulks List** (Category 1).

### A. Rationale for Rejection (Why Voted Down)

The FDA and PCAC presented several critical safety, efficacy, and chemical arguments for recommending **against** the inclusion of CJC-1295 in Category 1 compounding:

1. **Lack of Evidence of Clinical Efficacy:** The FDA noted there are no randomized, double-blind, placebo-controlled trials demonstrating clinical effectiveness for the nominated compounding uses (e.g., muscle hypertrophy, fat loss, anti-aging, or cachexia).
2. **Systemic Safety Risks:** Clinical data showed that CJC-1295 causes systemic vasodilatory reactions, including flushing, hypotension, and transient tachycardia. 
3. **Cardiovascular Safety and Halted Phase 2 Trial (NCT00267527):**  
   The primary safety objection centered on a Phase 2 clinical trial of CJC-1295 with DAC (evaluating its use in HIV-associated visceral obesity). In **July 2006, the trial was abruptly terminated following the death of a study participant** who suffered a fatal myocardial infarction (heart attack) approximately two hours after receiving their 11th weekly dose.
   * Although the principal investigator suggested the cause was likely underlying, asymptomatic coronary artery disease, the sponsor (ConjuChem) halted commercial development.
   * The FDA argued that because clinical development was halted, there is a **complete lack of long-term safety data** in humans, presenting an unacceptable risk for compounded drugs.
4. **Manufacturing Quality and Impurities:** Compounded peptides are highly susceptible to impurities and degradation. The FDA highlighted that without an approved drug master file or USP monograph, compounded CJC-1295 products frequently contain unidentified peptide impurities that could trigger severe immunogenic reactions or antibody formation.

### B. Vote Tally
The PCAC voted **unanimously 12-0 (0 "Yes" to 12 "No")** against the addition of CJC-1295-related substances to the 503A Bulks List.

---

## 4. 2025/2026 Compounding Status Updates

The regulatory status of compounded CJC-1295 changed significantly in **April 2026**, placing it in a complex legal position.

### A. April 2026: Removal from Category 2
* **Action:** The FDA officially removed CJC-1295 (and 11 other peptides, including BPC-157, TB-500, and MOTS-c) from its **Category 2** list.
* **Reason:** Category 2 contains bulk drug substances that the FDA has identified as presenting "significant safety risks" during active evaluation. However, the original nominators formally **withdrew the compounding nominations** for CJC-1295. Under FDA rules, when a nomination is withdrawn, the FDA removes the substance from the interim evaluation categories (both Category 1 and Category 2).

### B. The Compounding "Gray Zone" (Current Legality)
Many online forums and marketing channels mischaracterized the April 2026 update, claiming peptides had been "legalized again." In reality, the removal from Category 2 created a **regulatory gray zone that effectively bars legal compounding**:

Under **Section 503A** of the Food, Drug, and Cosmetic Act, a compounding pharmacy may only use a bulk drug substance if it meets one of three statutory criteria:
1. It is a component of an FDA-approved commercial drug.
2. It is the subject of an active United States Pharmacopeia (USP) or National Formulary (NF) monograph.
3. It appears on the FDA's final list of approved bulk drug substances (the 503A Bulks List).

#### The Legal Reality for CJC-1295:
* CJC-1295 is **not** a component of any FDA-approved drug.
* CJC-1295 has **no** USP or NF monograph.
* CJC-1295 was rejected by the PCAC and is **not** on the 503A Bulks List.
* Because the nomination was withdrawn, it is **no longer in Category 1** (under evaluation), meaning it does not benefit from the FDA's interim enforcement discretion policy.

> [!IMPORTANT]
> **Conclusion on Legality:** While CJC-1295 is no longer designated as an active "Category 2 Significant Safety Risk" (due to nomination withdrawal), **there is no legal pathway under Section 503A for compounding pharmacies to compound or distribute CJC-1295.** Compounded CJC-1295 distributed by compounding pharmacies is considered an unapproved new drug and is subject to FDA enforcement action.

### C. Upcoming PCAC Reviews (July 2026 & February 2027)
* The FDA scheduled a PCAC review on **July 23–24, 2026** (Docket No. FDA-2025-N-6895) to evaluate seven other peptides (BPC-157, KPV, TB-500, MOTS-c, DSIP, Semax, Epitalon) that were removed from Category 2.
* A second meeting is planned before the end of **February 2027** to review the remaining five (including GHK-Cu, Melanotan II, LL-37, DiHexa, and PEG-MGF).
* **CJC-1295 is not on the docket for these upcoming reviews** because its evaluation was completed and officially rejected during the December 2024 meeting.
