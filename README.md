## 📢 Analysis Overview


<br/>

## 📁 Project Structure

```
analysis-1
├── dataset/                                      # Result of experiments from the paper
│   ├── Non-V1-Websites/                          # Websites with no Violation#1
│   │   └── [rank_id].[main/sub].[count].store    # Record cookies
│   ├── V1-Violating-Websites/                    # Websites with Violation#1
│   │   └── [rank_id].[main/sub].[count].store
│   ├── non-v1.txt                                # Rank id to domain map (no violation#1) 
│   └── v1.txt                                    # Rank id to domain map (violation#1)
├── img/                                          # Images for report 
├── output/                                       # Raw outputs from the analysis
│   ├── non_v1.txt                                
│   └── v1.txt
├── CookieTaxonomy.md                             # Cookie Taxonomy and Severity metric description
├── models.py                                     # Classes for the analysis
├── utils.py                                      # Util functions for the analysis
├── pipeline.py                                   # Analysis pipeline
├── plots.ipynb                                   # Plots and statistics of results
├── requirements.txt                              
└── README.md                
```


<br/>

## 💻 Usage

0. Create a virtual environment _(optional)_ [\[1\]](https://www.w3schools.com/python/python_virtualenv.asp)



1. Install the requirements.txt

```bash
pip install requirements.txt
```

2. Run the pipeline script

```bash 
python3 pipeline.py
```

The outputs will be generated on the `output/` folder.

You can regenerate plots on `plots.ipynb`




<br/>

## 📊 Summary of Results



<br/>