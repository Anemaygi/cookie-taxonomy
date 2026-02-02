## 📢 Analysis Overview & Methodology


In the paper, they define vulnerability #1 as "Positive consents registered before user actions" as "Consent strings indicating a non-empty list of consented TCF purposes and vendors are detected before users make choices on cookie banners". 

To detect this violation, CSChecker identifies websites that adopt TCF v2.1 in the automated crawling, record the cookie writes and extracts network activities with consent strings from performance logs. They report a violation if the website used a positive consent string before user interaction with the banner.  

The paper detects binarily if a website has this violation, however some websites may offer a bigger exposure to privacy threats based on the structure of the cookies they are writing before user consent. 

To characterize this heterogeneity and rank the websites based on how severe is the violation, I introduce a cookie taxonomy and define a "severity" as a metric for the risk of privacy threats enabled by cookies written before user consent.

Then, I developed a script to calculate the severity measure of each website of the dataset based on the logs of events before user consent from CSChecker, separated by websites that violates Violation #1 (also defined as "V1" accross the project) and websites that do not (defined as "Non-V1"). All the websites present on the logs are used in the analysis. They are both able to send cookies before user interaction, but Non-V1 does that in non-compliance with TCF v2.1.

This script generates files in "output/", which contains
```
[rank_id], [domain], [severity], [number of cookies]
```
for all the websites, separated by V1 and Non-V1.

Finally, this data is plotted in a density plot in order to determine distribution shape. Statistical tests (such as T-Test) are also applied to verify significant statistical difference between severity scores from V1 and Non-V1


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

Besides the [Cookie Taxonomy and Severity metric definition](https://gitlab.cs.mcgill.ca/billy/comp555-p1-t10/-/blob/main/analysis-3/CookieTaxonomy.md?ref_type=heads#%EF%B8%8F-severity-measure), it is found that websites that commit \textit{Violation \#1} have a more concentrated distribution in terms of their Website Severity metric. Interestingly, through statistical tests, websites that to not commit this violation seem to have a less dense distribution, yet a higher value for the Severity metric. 

![Density plot](analysis-3/img/density_plot.png)



<br/>