# CRITIQUE.md

## Overview
This is a simple structured pipeline project that aims to extract, transform and load a specific dataset from Eurostat website (nasa_10_nf_tr) as a development test.

---

## Architectural Choice
- I've made some research about the extraction methods available in the API documentation from the users-guides https://ec.europa.eu/eurostat/web/user-guides/data-browser/api-data-access/api-introduction and it had the option to use JSON-stat data which with some research found a python lib that deals with that with ease, so that one of the thoughts i had going in that direction. Also usually JSON is commonly parsed in a lot of languages.

Firstly I created a single file ETL script, but then I thought to sharpen it a bit and just make each step a new file so readability and future refactoring would be easier.

---

## AI Tools
- Utilised AI tools to improve project environment creation such as fast installing of all the libraries used in this project.
- Improved data understanding about indexation of multidimensional data

---

## Architecture Modifications
- Utilise Crons to run the pipelines from time to time if necessary. As datasets are often very big.
- The same structure could be applied but with configurations for different URL's and different tables.

---