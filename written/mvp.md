# MVP
This project has been trial and error for me. I've tried many technologies and tools to help me work on the project. I end up using both MongoDB(json)
and SQLite(RMDB) for data storage and able to get both current and historical data(around 500K of historical data, due to many stations NOAA provided
were missing, now I have around 100K of data to work with).

After some EDAs', I was able to use the data to extract information of each city weather condition and locating them on the map. Here is an example of the
application of the project. 


<img width="1107" alt="mvp" src="https://user-images.githubusercontent.com/43353401/137033724-43ceb48c-5311-42a7-a52f-99b3d0ebeec5.png">

As you can see, I've use streamlit over flask because after testing out flask, I realize im not a web developer. Steamlit help me a lot with
creating the functionalities and designing the application.

To complete this project, I will add visuals after analyzing the historical data using pyspark. This will be part of the streamlit app, maybe on
the bottom of the page. I also want to include pictures of weatehr conditions on the map, and it is something I am still working on.
