# Modeling a Virtual Data Infrastructure

## Raw Data
- **What data can be loaded?**
  
## Analytics
- **Which summary Tables can be made?**

## Topic
Factors that determine the US university ranking

## ETL

### 1. Extract
To determine the factors that influence US university rankings, U.S News is referred to. The following factors are considered for university ranking:
- Graduation and retention rate
- Social mobility
- Graduation rate performance
- Undergraduate academic reputation
- Faculty resources
- Student excellence
- Financial Resources
- Expert Opinion
- Standardized tests (SAT and ACT)

### 2. Transform
Due to the vast number and diverse types of universities in the US, universities are classified into four categories: National Universities, National Liberal Arts Colleges, Regional Universities, and Regional Colleges. Tables are created within these categories.

#### Table 1) Student Information
- High School class Standing
- Standardized tests
- Student Excellence
- Retention Rate

#### Table 2) Faculty Resources
- Class size
- Faculty salaries (full-time instructional professors, associate professors, and assistant professors)
- Faculty with a terminal degree
- Student-faculty ratio
- Proportion of faculty who are full-time

#### Table 3) Financial Resources
- Average Alumni Giving rate
- Financial support per student

#### Table 4) Graduation
- Graduation Rate
- Graduation Rate Performance
- Social Mobility
- Graduate Indebtedness

### 3. Load
The extracted and transformed data or tables are loaded into the Data Warehouse.
