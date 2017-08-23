# What is this?
Extract user reviews/ user profiles from tripadvisor and apply machine learning techniques to perform Descriptive, Predictive & Prescriptive  Analytics.

# Instruction
Simply run "python main.py" or "python -W ignore main.py" to suppress warning message in terminal. A command line interface will be displayed, user has  toinsert choice to perform action. Actions are basically grouped as:
1. Extraction (Web scraping using BeautifulSoup/ Selenium ChromeDriver)
2. Transformation (Data preprocessing)
3. Data Analytics (Sentimental analysis, topics modelling, decision tree)

Below is screenshot of CLI screen:

<p align="center"> 
  <img src="https://github.com/woo-chia-wei/insight-analysis-tripadvisor/blob/master/images/readme/tripadvisor_ca_cli.png" 
       width="50%" height="50%">
</p>

# Architecture Design
Basically this framework contains 5 different layers:
* Interface
* Workers
* Repository
* Database
* Presentation

<p align="center"> 
  <img src="https://github.com/woo-chia-wei/insight-analysis-tripadvisor/blob/master/images/readme/framework_architecture.png" 
       width="70%" height="70%">
</p>
