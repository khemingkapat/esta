# Parsing Esports Trajectories & Actions (ESTA)
fork version from [esta](https://github.com/pnxenopoulos/esta) to be tabular format for further data modelling

# Important Notes
In the `./parsed/` folder is the tables of data extracted from 50 CSGO matches, 25 LAN and 25 online matches.

If you want the table for more matches, you could use the function to extract from more matches, 50 matches is just reasonable size for both analyzing purpose and available space for github.

**Please Be Careful**, I spend a lot of time since my the data bloated by system to around 200 GB because of the data. So be careful on how you use the function and how you store it. But that shouldn't be the case because the data bloating my system is trash since I repeatedly create and delete for testing.

For further use, you could use all the `.parquet` files in the `./parsed`. Don't forget to check the integrity and clean it before use it because this is just to extract from `.csv` files to `.parquet` as a tabular data.

