Modeled a Virtual Data Infrastructure 
•	Raw_data: What data can be loaded?
•	Analytics: Which summary Table can be made

Topic
Factors that determine the US university ranking

ETL

1.Extract
In order to know which factors determine the US university ranking, I refer to U.S News.
The followings are the list of factors that could be considered for university ranking:
•	Graduation and retention rate
•	Social mobility
•	Graduation rate performance
•	Undergraduate academic reputation
•	Faculty resources
•	Student excellence
•	Financial Resources
•	Expert Opinion
•	Standardized tests (SAT and ACT)


2.Transform

Since there are vast number and diverse types of universities in the US, I classified them into 4 categories: National Universities, National Liberal Arts Colleges, Regional Universities, and Regional college. Then, I created tables within the four categories.

Table1) Student Information
High School class Standing
Standardized tests
Student Excellence
Retention Rate
 
Table2) Faculty Resources
Class size
Faculty salaries (full-time instructional professors, associate professor and assistant professors)
Faculty with terminal degree
Student-faculty ratio
Proportion of faculty who are full- time
 
Table3) Financial resources
Average Alumni Giving rate
Financial support per student
 
Table4) Graduation
Graduation Rate
Graduation Rate Performance
Social Mobility
Graduate Indebtedness
  
3. Load
We load these data or table to Data Warehouse.

