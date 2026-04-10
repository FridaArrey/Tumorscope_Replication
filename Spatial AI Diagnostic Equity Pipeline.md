## **Spatial AI Diagnostic Equity Pipeline**

### **A Tumorscope Replication & Extension for Underrepresented Pathologies**

This project replicates the award-winning **Tumorscope (2025)** methodology to quantify immune exclusion in lung adenocarcinoma. By extending the analysis to include the **Steyn Lab (EMBO 2022\)** datasets, this pipeline identifies critical "spatial mimics" in global health—specifically where the architecture of Tuberculosis (TB) mirrors that of Squamous Cell Carcinoma (SCC).

---

### **🧬 Core Methodology: The "Equity" Logic**

Most spatial AI models are trained on Western oncology cohorts. This pipeline recalibrates diagnostic specificity by:

* **Targeting Pathological Mimicry:** Evaluating the "Frustration" index of T-cells trapped in the fibrotic cuffs of TB granulomas, which often creates a spatial signature identical to a tumor stroma.  
* **Macro-Architecture Normalization:** Adjusting for magnification variance (5x vs 20x) to ensure Whole Slide Images (WSI) from diverse clinical environments are comparable.  
* **The Mimicry Index:** Calculating the overlap in "Pathological Burden" between infectious diseases and malignancies to prevent diagnostic false positives in TB-endemic regions.

---

### **🛠 Project Structure**

Bash  
.  
├── archive/                   \# Deprecated scripts and exploratory drafts  
├── data/                      \# Raw LC25000 tiles and Steyn Lab WSIs  
├── models/                    \# lung\_triage\_v1.pth (Neural weights)  
├── outputs/                   \# Generated figures and CSV ledgers  
├── src/                       \# Core Analytical Engine  
│   ├── calculate\_polarization\_index.py \# Lemaitre spatial math  
│   ├── analyze\_tb\_jem.py              \# WSI processor for TB cohorts  
│   └── finalize\_cancer\_tb\_metrics.py  \# Final statistical reporting  
└── README.md                  \# Project documentation

---

### **📊 Benchmarked Results**

The pipeline identifies a **133.3% Mimicry Index**, where the mechanical exclusion in TB exceeds that of lung cancer:

| Phenotype | Frustration | Density | Burden Score |
| :---- | :---- | :---- | :---- |
| **Normal Lung** | 43.8% | 31.9 | **13.97** |
| **Adeno (ACA)** | 70.0% | 57.8 | **40.46** |
| **Squamous (SCC)** | 82.0% | 62.9 | **51.58** |
| **TB (Steyn Lab)** | 88.5% | 77.7 | **68.76** |

---

### **🚀 Key Technical Features**

* **Infrastructure Resilience:** High-resolution TIF handling with PIL "Decompression Bomb" bypass for Whole Slide Image processing on standard hardware.  
* **Spatial Scaling:** Normalization logic that allows for comparison between disparate pathological datasets (5x AHRI vs 20x LC25000).  
* **Diagnostic Guardrails:** Quantitative evidence that spatial AI trained only on tumors risks misdiagnosing chronic infectious remodeling.

---

### **💡 How to Run**

1. **Prepare Environment:** Ensure src/ contains the core polarization logic.  
2. **Execute Full Spectrum Analysis:**  
   Bash  
   python3 src/finalize\_cancer\_tb\_metrics.py  
3. **Inspect Results:** Check outputs/ for the detailed polarization CSVs and final summary report.

---

### **🎓 Author**

**Frida Arrey, PhD, MSc**

*Data Analytics & Life Science AI Consultant*

*Specializing in Immunological Research and Public Health Data Integrity.*

---

**Note:** This project is a contribution toward ensuring that the next generation of spatial AI is biologically robust enough to serve patients globally, regardless of regional disease prevalence. 

