
# CardioMotion

### Computational Cardiovascular Imaging and Motion Analysis

CardioMotion is an experimental research software project investigating computational methods for analysing cardiac MRI images, ventricular structures, myocardial motion and regional deformation.

The project aims to develop a research platform integrating cardiac image processing, segmentation, motion estimation, myocardial strain analysis and measurement-quality assessment.

## Research Vision

To investigate whether an integrated computational framework can provide reproducible, quality-aware measurements of cardiac structure and motion across different cardiac MRI acquisitions.

## Research Objectives

1. Develop cardiac MRI image-loading and preprocessing workflows.
2. Analyse left ventricular, right ventricular and myocardial structures.
3. Investigate cardiac motion and displacement estimation.
4. Explore regional myocardial strain estimation in 2D and 3D.
5. Investigate uncertainty and reliability of computational measurements.
6. Evaluate reproducibility across datasets and imaging conditions.

## Initial Research Experiment

**Experiment 001: ACDC Cardiac MRI Analysis**

The initial experiment uses the Automated Cardiac Diagnosis Challenge (ACDC) dataset.

Initial tasks:

- Load cardiac MRI volumes in NIfTI format.
- Inspect image dimensions and voxel spacing.
- Visualise expert-provided segmentation masks.
- Analyse ventricular structures.
- Calculate exploratory ventricular volume measurements.

The ACDC dataset provides expert segmentation references at selected cardiac phases. These references support segmentation and volume analysis but do not independently establish ground-truth myocardial strain.

## Planned Research Modules

| Module | Research direction |
|---|---|
| Image Processing | MRI loading and preprocessing |
| Segmentation | LV, RV and myocardium |
| Motion Analysis | Cardiac displacement estimation |
| Strain Analysis | Regional myocardial deformation |
| Quality Assessment | Tracking reliability and uncertainty |
| Validation | Reproducibility and cross-dataset evaluation |

## Technology Stack

- Python
- Streamlit
- NumPy
- SciPy
- NiBabel
- Matplotlib
- Pandas
- PyTorch / MONAI (planned)

## Project Structure

```text
cardiomotion/
├── app.py
├── README.md
├── requirements.txt
├── src/
├── experiments/
├── tests/
└── docs/
```

## Scientific Scope and Limitations

CardioMotion is currently an experimental research prototype.

The initial implementation focuses on image visualisation, segmentation inspection and exploratory measurements.

Myocardial strain estimation, 2D/3D motion tracking, uncertainty quantification and clinical validation are future research objectives.

Computed measurements must not be interpreted as clinically validated results or used for patient diagnosis or treatment decisions.

## Research Collaboration

CardioMotion is intended to support collaborative research involving:

- Cardiologists
- Cardiac radiologists
- Biomedical engineers
- Medical imaging scientists
- Computational researchers

Contributions, scientific feedback and research collaborations are welcome.

## Current Development Status

**Stage 1 — Initial prototype development**

- [x] Initial Streamlit interface
- [x] Initial dependency configuration
- [ ] ACDC dataset integration
- [ ] Segmentation validation
- [ ] Motion estimation
- [ ] Myocardial strain analysis
- [ ] Uncertainty and reproducibility studies

---

**CardioMotion — Experimental Computational Cardiovascular Research Software**
