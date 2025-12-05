# README

## About Section

This project combined two datasets into the ETL pipeline. The project aims to combine a boxers data with information about fight results. 


## Index Section

<a href="#Installations">Installation</a>  

<a href="#Project-Management">Project Management</a>  

<a href="#Kanban">Kanban</a>

<a href="#Project-timeline">Project timeline</a>

<a href="#The-Rules-of-Boxing">The Rules of Boxing</a>  

<a href="#Understanding-the-Data">Understanding the Data</a>

<a href="#Data-Extraction">Data Extraction</a>

<a href="#Data-Transformation">Data Transformation</a>

<a href="#Data-Load">Data Load</a>

<a href="#Testing">Testing</a>

<a href="#Future-Developments">Future Developments</a>

<a href="#Challenges">Challenges</a>

<a href="#Takeaways">Takeaways</a>

<a href="#Git-Branches">Git Branches</a>

<a href="#Further-Discussion">Further Discussion</a>

## Installations

Prerequisite:  

- Python version 3+ available at the <a href="https://www.python.org/downloads/">python website.</A>
- Pip installation
- Git(to clone the repository)


Making a virtual environment(on windows):  

```terminal
python -m .venv venv
```

Going into the virtual environment
```terminal
source .venv/bin/activate
``` 

```
pip install streamlit ipykernel pandas pyarrow plotly pytest pytest-cov 
```

```terminal
pip install -r requirements.txt
```

```terminal
pip -e .
```


Run the ETL pipeline:

```terminal
run_app dev
```


## Project Management

To effectively manage the project, I used a project timeline to ensure full clarity on the features to be developed at the end of each sprint (which typically lasted one day). This allowed me to refer to the priority list and clearly understand which features needed to be implemented next.

MoSCoW prioritisation had become very effective within the core functionality of the application. This allowed me to categorise the features based on their importance level. This helped with continuous deployment as the priorities were placed on the must haves first which were essential to the delivery and initial deployment. Once these features were completed then the order of features were labelled as should, could, would.

<table>
  <tr>
    <th>Priority level</th>
    <th>Feature</th>
    <th>Reason for priority level</th>
    <th>Complete?</th>
  </tr>
  <tr>
    <td>Must</td>
    <td>Data must be extracted autonomously</td>
    <td>Core dependency - without extraction we would have no data to work with</td>
    <td><input type="checkbox" checked><td>
  </tr>
  <tr>
    <td>Must</td>
    <td>Data must be transformed and standardised to fit the data analysis requirements.</td>
    <td>Core dependency again as we would be working with data that would have inconsistencies making analysing the data difficult.</td>
    <td><input type="checkbox" checked><td>
  </tr>
  <tr>
    <td>Should</td>
    <td>Merge both datasets together after it has been cleaned showcasing fighter records with the appropriate attributes.</td>
    <td>Should as this will be able to reveal insights within the data.</td>
    <td><input type="checkbox" checked><td>
  </tr>
    <tr>
    <td>Should</td>
    <td>Generate synthetic dates which has a rule that a fighter cannot fight another individual on the same day.</td>
    <td>This is important as this can help to get the most up to date fighters record when analysing. Furthermore, more emphasis can be placed onto best of the year, most knockouts of the year, losses in the year etc</td>
    <td><input type="checkbox" checked><td>
    </tr>
   <tr>
    <td>Should</td>
    <td>Must be able to showcase the top 5 best performing individuals at every weight class</td>
    <td>Should because this is essential information when asking questions about the sport</td>
    <td><input type="checkbox"><td>
  </tr>
  <tr>
    <td>Could</td>
    <td>Who maintains the most knockout accuracy from every division?</td>
    <td>Could because this would be important to find out for which fighters are the most exciting</td>
    <td><input type="checkbox"><td>
    </tr>
        <tr>
    <td>Could</td>
    <td>Can utilise the requests library to scrape photos of fighters available on wikipedia to showcase the fighters attributes, records and their number of knockouts with other data.</td>
    <td>Could as this is not essential to the project but would make a nice addition as it would be nice to visualise the fighter with statistics.</td>
    <td><input type="checkbox" checked><td>
  </tr>

  <tr>
    <td>Would</td>
    <td>Create a probability for match-ups on who would most likely win given the fighters record.</td>
    <td>Would as this would require machine learning and the use of Scikit-learn. Given the time frame this may not be viable therefore has not been put as a priority. But will be considered a future work.</td>
    <td><input type="checkbox"><td>
  </tr>
</table>

#### Kanban

A Github Kanban-board was utilised for understanding the current project backlog and to visualise an overview of the current progress. This helped to understand the definition of "DONE" and during the sprints helped keep morale boosted to view achievements. As can be seen by <a href="#appendix1">appendix1</a>.

<img src="appendices/kanban.png" alt="" title="appendix1" id="appendix1">

Moreover, kanban was integrated with github issues which played a fundamental role with tracking states of issues and where in the process of completion it currently lies.

#### Project timeline

<img src="appendices/timeline.png">

### The Rules of Boxing

Boxing is a physical sport where both athletes are assessed by a series of judges on a round to round basis. Each athlete is scored on their performance. Things that may affect the score can be:

- Aggression
- Landing of punches(how clean the punches land)
- Defense
- Ring Generalship: which includes controlling of the pace, positioning and style of the fight. 

Points can also be deducted in the case of a knockdown or if foul play becomes evident.

The fight can either end by: 

- Technical Knockout: Where the referee/medic intervenes stating the fight cannot go on for the fighters safety.  

- Knockout: Ten seconds is given to the boxer to get on their feet after any part of their body other than their feet touches the canvas. If they do not get up after 10 seconds this results in a knockout victory favouring the person who landed the knockout punch.

- Point decision: Depending on the bout, rounds can last between 4 to 12 rounds depending on the experience level, if it is a championship bout. If the fight goes the distance(the whole way), judges score the contest and decide the winner based on performance of both fighters.

How it can be contested:


<table>
  <tr>
    <th>Decision</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>Unanimous Decision</td>
    <td>This means that all the judges agree that fighter A's performance was better than fighter B's performance.</td>
  </tr>
  <tr>
    <td>Split Decision</td>
    <td>This is where two judges believe fighter A scored a better performance whereas one judge believes fighter B performed better.</td>
  </tr>
  <tr>
    <td>Majority decision</td>
    <td>This is where two judges believe fighter A had performed better however one judge believes it was a draw.</td>
  </tr>
  <tr>
      <td>Split Draw</td>
    <td>One judge scores fighter A, another judge scores boxer B and the third scores the performance a draw.</td>
  </tr>
  <tr>
      <td>Majority Draw</td>
    <td>Two judges rule the fight as a draw and the third scores one boxer as a winner. The match is scored as a draw.</td>
  </tr>
</table>


### Understanding the Data

A fighter is usually recognised from their "portfolio". Meaning the names of the other athletes they have faced and the difficulty of their competition. Which is why their "record" is crucial to them. "Won_a" and "Won_B" is the amount of fights the fighter has won before facing their current competition. Equally the same logic applies to lost_a, lost_b, draw_a and draw_b.

The prefix of _a and _b was used to differentiate the fighter from one another. For example "Canelo" vs "Crawford", Canelo may be fighter A and his attributes are highlighted as [column_attribute]_A and Crawford's attributes may be highlighted as [column_attribute]_B.

Class is an attribute linked to "weight". To fight an opponent one must fit the weight requirement which can be between a certain scale for example middleweight fighters must weigh between 154lbs-160lbs. The classification attribute was therefore created to highlight the weight class the fighters were fighting at.

# Data Extraction



# Data Transformation

<table>
  <tr>
  <tr>
  <caption>Boxing Match Dataset</caption>
  </tr>
    <th>Dataset</th>
    <th>Kept?</th>
    <th>Reason for keeping?</th>
    <th>Transformation process</th>
  </tr>
  <tr>
    <td>Age_A/Age_B</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>May give us good insights into boxers performance by age demographic. From here</td>
    <td>If the value was null I generated a random age between 18 and 45 years. This is because if I was to use the mean demographic this can affect the distribution of the data and would hinder the analytical processing. The reason it would be 18 is because this is the youngest a boxer can become a professional by sanctioning bodies of boxing.</td>
  </tr>
    <tr>
    <td>reach_a/reach_b</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>Reach was also a metric that was used. The hope was to see if a higher reach meant a higher chance of a knockout.</td>
    <td>Again numpy was used based on height to ensure that the height was proportionate to the reach. To ensure this accuracy height must be computed first.</td>
  </tr>
    <tr>
    <td>stance_A/stance_B</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>Would be good to analyse if different stances have a higher percentage of a knockout. May be used as a potential future work.</td>
    <td>Had cleaned the data by removing whitespacing, outliers in the data, placing a probability of the boxer being "orthodox", "southpaw" based on my own experience of watching boxing.</td>
  </tr>
    <tr>
    <td>weight_A/weight_B</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>This was crucial for classifying the boxer by weight category.</td>
    <td>The transformation had used a range between 40 and 130 if the height wasn't accounted for. But if the height was accounted for it would use a Numpy distribution depending on the boxers height. The taller the boxer is the more likely they are to have a higher weight.</td>
  </tr>
    <tr>
    <td>height_a/height_b</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>Further data can be analysed to see if having height can affect performance(more wins, going on points etc)</td>
    <td>This was an estimate based on the classification of their weight. Depending on their weight I would utilised the Numpy library to create a distribution where it assigns a numeric value based on the boxers height. If weight is not filled in it would get the average height.</td>
  </tr>
  <tr>
    <td>won_A/won_B</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>This was used to find the amount of wins a fighter may have on their record. This can help to produce the best of all time as a table.</td>
    <td>The mean of the wins was computed of the current number of wins was complete. I also used a validation metric which would find a in between value for the number of fights a fighter would have over the span of their career. Typically a fighter would have 50 fights over their career but this was raised higher in the case of anomalies. Furthermore, turning the positive to integer was done to prevent unclean data.</td>
  </tr>
  <tr>
  <td>lost_A/lost_B</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>This can help to produce loss leaders in the different divisions.</td>
    <td>On average the loss rate compared to win rate within boxing is higher therefore, if na fill a number between 0 and 130(inclusive). This is due to higher level of competition within boxing.</td>
  </tr>
  <tr>
  <td>drawn_A/drawn_B</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>As wins and losses were accounted, draws would allow for a holistic view of boxing as a whole.</td>
    <td>The draw rate was set between 0 and 20 for values and a median was drawn from the given distribution of drawn_a and drawn_b columns</td>
  </tr>
    <tr>
  <td>kos_A/kos_B</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>This would allow us to see the knockout percentage of the individual when boxing and how many fights go to points.</td>
    <td>The data was standardised to ensure that knockouts are never above the number of wins.</td>
  </tr>
  <tr>
  <td>result</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>I chose to keep the results as boxing matches require the end result and many attributes such as wins requires results. For future work incrementing the boxers wins dynamically will be taken into account.</td>
    <td>Results required to see many attributes such as the judges scorecards and to summarise the score cards. Whoever had returned a higher sum was declared the winner. Otherwise the bout would end in a draw.</td>
  </tr>
  <tr>
  <td>decision</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>This was used to show what decision had formed whether it was a disqualification/knockout etc. This was used to see the amount of knockouts, unanimous decisions and other forms of decisions within boxing as a future work</td>
    <td>Decision was messy data in itself. It was stripped. Placed in upper casing for standardisation and replaced with abbreviations.</td>
  </tr>
  <tr>
  <td>judge1_A/.../judge3_B
</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>Would be interesting to see what each judge scored the contest.</td>
    <td>If the value was null for judge1_B, the transformation process would first identify the location of the row and estimate the average score of all the other judges. If not it would then do a fall back by giving the contest 114.</td>
  </tr>
</table>


<table>
  <tr>
  <tr>
  <caption>Fighter Dataset</caption>
  </tr>
    <th>Dataset</th>
    <th>Kept?</th>
    <th>Reason for keeping?</th>
    <th>Transformation process</th>
  </tr>
  <tr>
    <td>Rating</td>
    <td>No<input type="checkbox"></td>
    <td>Not needed for the purpose of this etl project</td>
    <td>Dropped column</td>
  </tr>
  <tr>
    <td>Boxer</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>Need to know the name of the fighter</td>
    <td>Dropped any na values</td>
  </tr>
    <tr>
    <td>Country</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>Need to know the originality of the fighter for Tableau/streamlit analysis.</td>
    <td>Dropped any na records for fighters without countries.</td>
  </tr>  
    <tr>
    <td>Weight</td>
    <td>Yes<input type="checkbox" checked=True></td>
    <td>Needed information about the fighters natural weight class. This can then be brought over to the weight classes and as a future work I plan on matching the fighters weight from the dataset with the fighter weight on the other dataset.</td>
    <td>Standardised the weight by converting lbs to kg so when merging datasets this will ensure a standardised format of weight. I did this by getting the current lbs data in the fighters dataset and multiplying by 0.0.45359(found by a conversion on google)</td>
  </tr>  
      <tr>
    <td>Ceiling</td>
    <td>No<input type="checkbox"></td>
    <td>Unneeded - out of the scope of the project</td>
    <td>Dropped column</td>
  </tr>
    <tr>
    <td>Action</td>
    <td>No<input type="checkbox"></td>
    <td>Unneeded - out of the scope of the project</td>
    <td>Dropped column</td>
  </tr>  
      <tr>
    <td>Trainer</td>
    <td>No<input type="checkbox"></td>
    <td>Unneeded - out of the scope of the project</td>
    <td>Dropped column</td>
  </tr>  
    <tr>
    <td>Sex</td>
    <td>Yes<input type="checkbox"></td>
    <td>Would be interesting to see the number of males/females boxers for analysis.</td>
    <td>Data was already clean.</td>
  </tr> 
</table>

# Data Load

The data was loaded into a final processed folder in which lied the last data during the transformation process. This was data that was ready to be used by Streamlit and Tableau for analytical purposes.

# Testing

Unit testing had been utilised extensively to test out different features within the application. A table has been provided to show the function name, which file and what its used to do.

<table>
  <tr>
    <th>Function Name(test)</th>
    <th>File Reference</th>
    <th>What its used to do</th>
  </tr>
  <tr>
    <td>test_transformed_data_types</td>
    <td>unit_tests/test_data</td>
    <td>This was used to test the data types for the given data in the original function boxer_dataset_transformation.</td>
  </tr>
  <tr>
    <td>test_value_ranges</td>
    <td>unit_tests/test_data</td>
    <td>This was used to sanity check the range of data from the given ranges during the transformation phase.</td>
  </tr>
  <tr>
    <td>test_drop_columns</td>
    <td>unit_tests/test_dropped_columns</td>
    <td>This tests the drop of 3 columns(promoter, trainer, action)</td>
  </tr>
  <tr>
    <td>test_drop_unnamed_columns</td>
    <td>unit_tests/test_dropped_columns</td>
    <td>Tests for the removal of the unnamed column</td>
  </tr>
  <tr>
    <td>test_extract_raw_data</td>
    <td>unit_tests/test_extract</td>
    <td>This mocks a test function which extracts the raw data and returns columns of the data in the pandas dataframe.</td>
  </tr>
  <tr>
  <td>test_load_processed_fighter_file</td>
  <td>unit_tests/test_load</td>
  <td>This tests that the data has been loaded into the right folder and checks if there is quantities within the dataframe if not returns empty.</td>
  </tr>
  <tr>
  <td>test_missing_processed_fighter_file</td>
  <td>unit_tests/test_load</td>
  <td>This returns a file not found error if the loaded data doesnt contain the specified path.</td>
  </tr>
  <tr>
  <td>test_validate_column_count_passes</td>
  <td>unit_tests/test_load</td>
  <td>This returns a file not found error if the loaded data doesnt contain the specified path.</td>
  </tr>
  <tr>
  <td>test_validate_row</td>
  <td>unit_tests/test_load</td>
  <td>This checks the number of rows return as we expect and we compare this by getting the first value of the shape and comparing it to the number of rows within the dataset that we expect it to be.</td>
  </tr>
    <tr>
  <td>test_run_app_execution_time</td>
  <td>unit_tests/test_streamlit</td>
  <td>This checks the streamlit runs and if it goes over 10 seconds to check if its running it skips.</td>
  </tr>
  <tr>
  <td>test_valid_age</td>
  <td>unit_tests/test_transform</td>
  <td>This checks the boxers age is a valid number between 18 and 43. If it is not a valid age it autogenerates a number for the individual. Furthermore, data ranges ensure that all the integers returned are positive.</td>
  </tr>
  <tr>
  <td>test_fight_dataset_column_count</td>
  <td>unit_tests/test_transform</td>
  <td>This tests that the numerous columns are present within one of the rows using fake data</td>
  </tr>
  <tr>
  <td>test_clean_stance_standardises_values_and_fills_missing</td>
  <td>unit_tests/test_transform</td>
  <td>This tests whether the transformed stance data is clean in the correct format.</td>
  </tr>
  <tr>
  <td>test_clean_height_handles_missing_and_invalid_values</td>
  <td>unit_tests/test_transform</td>
  <td>This checks the height of the given data point and returns if it falls within a valid range.</td>
  </tr>
  <tr>
  <td>test_clean_weight_replaces_invalid_and_missing</td>
  <td>unit_tests/test_transform</td>
  <td>This tests whether the boxer falls into a valid weight by checking the clean_weight function that was used in the transformation stage. If it returns values that were valid then it will undertake the process of validating the data by replacing the datapoint.</td>
  </tr>
    <tr>
  <td>test_clean_kos_caps_invalid_and_fills_missing</td>
  <td>unit_tests/test_transform</td>
  <td>Finds the edge cases for both the knock outs and fills in the missing values.</td>
   </tr>
       <tr>
  <td>test_infer_results_ko_logic</td>
  <td>unit_tests/test_transform</td>
  <td>This tests if someone has a higher knockout ratio in comparison to the other boxer this infers they will win(in theory).</td>
   </tr>
     <td>test_infer_results_scorecard_logic</td>
  <td>unit_tests/test_transform</td>
  <td>This is a crucial test to check that the logic of the judges score card work. It works by faking data of a judge score cards and ensuring score cards are added up and compared to the other fighters score cards.</td>
   </tr>
   <tr>
   <td>test_fill_decision_preserves_existing_value</td>
   <td>unit_tests/test_transform</td>
   <td>This assures us that if a decision has been filled, it sticks with the decision that has been honoured.</td>
   </tr>
  <tr>
   <td>test_fill_decision_detects_ko</td>
   <td>unit_tests/test_transform</td>
   <td>This ensures that a knockout is detected when the data is correctly filled in as required.</td>
   </tr>
   <tr>
   <td>test_clean_draws_handles_invalid_and_fills_with_median</td>
   <td>unit_tests/test_transform</td>
   <td>this checks if the data that has been inputted is a valid number and is between the specified range.</td>
   </tr>
  <tr>
   <td>test_assign_weight_class_fight_ranges</td>
   <td>unit_tests/test_transform</td>
   <td>Tests if the weight specified in the original file is classified into the right category</td>
  </tr>
  <tr>
   <td>test_weight_class_adjusts_invalid_class_differences</td>
   <td>unit_tests/test_transform</td>
   <td>This tests if there is a significant weight categorisation difference in the data. If its over one weight class it returns as invalid.</td>
  </tr>
  <tr>
   <td>test_get_boxer_name_column_detects_name_variants</td>
   <td>unit_tests/test_transform</td>
   <td>This ensures that the fighter's name is returned which was a specified variable in the get_boxer_name_column function.</td>
  </tr>
  <tr>
   <td>test_fighter_dataset_transformation_basic</td>
   <td>unit_tests/test_transform</td>
   <td>This ensures that the right data of the fighter is returned.</td>
  </tr>
  <tr>
   <td>test_assign_unique_fight_dates_no_collision</td>
   <td>unit_tests/test_transform</td>
   <td>This tests whether two fighters are fighting on different days.</td>
  </tr>
    <tr>
   <td>test_clean_score_cards_handles_invalid_and_fills_means</td>
   <td>unit_tests/test_transform</td>
   <td>Tests the score cards and if the score card is not correctly filled out it produces an average value from the distribution of the data.</td>
  </tr>
  <tr>
   <td>test_merge_matchups_creates_pairs</td>
   <td>unit_tests/test_transform</td>
   <td>This function checks when the merge occurs that the data created shows pairs that can fight against one another. </td>
  </tr>
  <tr>
   <td>test_get_wikipedia_image_success</td>
   <td>unit_tests/test_wiki_api_function</td>
   <td>This function gets the success of the image upload(is the happy path)</td>
  </tr>
  <tr>
   <td>test_get_wikipedia_image_no_thumbnail</td>
   <td>unit_tests/test_wiki_api_function</td>
   <td>Returns no thumbnail for the image if it wasnt available upon request when magic mock generates a fake data request</td>
  </tr>
  <tr>
   <td>test_get_wikipedia_image_failure_status</td>
   <td>unit_tests/test_wiki_api_function</td>
   <td>When magic mock is called it checks if a failure has occured and .</td>
  </tr>
  
  
## Test coverage by file
<img src="appendices/test_cov.png">   

## Test coverage by functions
<img src="appendices/test_cov_functions.png">
</table>


## Future Developments

<ol>
<li>Display more accurate data(for example heavyweights in the boxer dataset column is honoured on the crossover to the final cleaned dataset)</li>  
<p>
<li>Minor bug fixing</li>  
<p>
<li>Aiming for more consistency within the dataset.</li>  
<p>
<li>Create a prediction algorithm using Scikit-Learn for match-ups and chance of a knockout either way, points etc.</li>  
<p>
<li>Incorporate power rating, using attributes of defense, footwork etc and placing it within a radar graph.</li>  
<p>
<li>Cloud Migration of the environment??</li>
This would depend on the overall cost of the cloud migration. But would only be done for a limited amount of time before deleting.
</ol>

# Challenges

<h3>Inconsistent data during the transformation process</h3>
Dataset had contained inconsistent records, missing values, duplicate data. Cleaning had taken most of the time set which I was given. The inconsistencies had meant decision making must be made!!  

<h3>Designing a modular and maintainable ETL pipeline</h3>  
A lot of the transformation phase was modularised and many csv's caused confusion even for myself. Documentation played a crucial role.  

<h3>Bottlenecks in the pipeline😡</h3>  
The ETL process due to large volumes of data had caused huge problems in terms of the performance. Sometimes returning results within minutes after run_app dev would be called. This led to a lot of wait time.  

<h3>Communicating the Domain</h3>
Tested even my own knowledge (after years of experience in watching boxing). Being able to communicate this knowledge with a variation of experience with the sport is a skill in itself.

# Takeaways

<h3>Project Management</h3>
The utilisation of a kanban board, using an agile approach, MuSCoW Prioritisation of the project and splitting the task according to priority listings.

<h3>What you set out to do isn't always the end product, but thats the agile way</h3>
As old requirements may change, new ones may be added in. Some featurues may be not worth doing due to resource limitations but this all comes from experience.

<h3>Emphasis on forward thinking for the whole ETL process</h3>
Some decisions made earlier may limit or alternatively may help you in the long run. Being able to drop data can be as helpful as keeping the data if it means reducing bottlenecks and its overall performance. A useful tactic that from hindsight would be needed is thinking "what data would I need to create that insight". From this dropping accordingly.


## Git Branches

- main  

This is the production environment which was used when a feature was finalised and ready to deploy. Upon feature completion a merge/pull request was done to ensure there were minimal merge conflicts. Furthermore, this had helped to promote working in silos before merging into the production environment(which in this case was main).

- etl-test  

Was used to test the code, all the functions as well as to work on the different folders within the tests.

- etl-transform 
 
Was used to transform the csv changes after extraction and to clean the data. This would play a crucical role when comparing the two csv files with other branches.

- viz  

This branch was used to visualise the streamlit app once the load process was complete. This was also used to demonstrate the etl pipleine integration when running ```run_app dev``` it would run the streamlit app in parallel displaying the data as required.

### Further Discussion

<table>
  <tr>
    <th>Subject</th>
    <th>Description</th>
    <th>Link</th>
  </tr>
  <tr>
    <td>AWS Service Integration plan</td>
    <td>As AWS is a scalable resource the markdown provided would allow me to plan how I would shift over this ETL project to the cloud. The markdown provides the reasons why this may be of benefit as well as the potential way this would be completed.</td>
    <td><a href="docs/AWS.md">AWS Documentation</a></td>
  </tr>
  <tr>
    <td>Boxing dataset location</td>
    <td>Reference: Kaggle Dataset. This dataset was open source and was extracted as a csv file.</td>
    <td><a href="https://www.kaggle.com/datasets/iyadelwy/boxing-matches-dataset-predict-winner/data">Boxer Dataset</a></td>
  </tr>
  <tr>
    <td>Fixture dataset</td>
    <td>Reference: Kaggle Dataset. This data was extracted as a csv file. Contains 25MB of data.</td>
    <td><a href="https://www.kaggle.com/datasets/mexwell/boxing-matches">Boxing matches</a></td>
  </tr>
</table>
