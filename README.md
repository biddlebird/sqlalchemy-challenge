# Climate Analysis and Exploration - SQLalchemy-Challenge

## Overview

For this project, I performed a detailed climate analysis and data exploration for Honolulu, Hawaii, using Python, SQLAlchemy, Pandas, and Matplotlib. The goal was to gather insights into the climate patterns and to design a Flask API that serves this information in a structured manner.

## Dependencies

```
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
```

## Part 1: Analyze and Explore the Climate Data

### Database Setup

- **Database:** `hawaii.sqlite`
- **Tools:** SQLAlchemy, Pandas, Matplotlib

### Steps Performed

1. **Connect to the Database:**
   - Used `SQLAlchemy create_engine()` to connect to the SQLite database.
   - Reflected the database tables into classes using `automap_base()` and saved references to the `Station` and `Measurement` tables.

2. **Precipitation Analysis:**
   - Retrieved the most recent date in the dataset.
   - Queried the last 12 months of precipitation data, specifically the `date` and `prcp` values.
   - Loaded the data into a Pandas DataFrame, sorted by date, and plotted the results.
   - Calculated and printed the summary statistics for the precipitation data.

![Alt.txt](https://github.com/biddlebird/sqlalchemy-challenge/blob/main/Plots/Precipitation%20Over%20the%20Last%2012%20Months.png)

3. **Station Analysis:**
   - Designed a query to calculate the total number of stations in the dataset.
   - Identified the most-active stations (with the most observations) and listed them in descending order.
   - Queried and calculated the lowest, highest, and average temperatures for the most-active station.
   - Retrieved the last 12 months of temperature observations (TOBS) for this station and plotted the results as a histogram.

![Alt.txt](https://github.com/biddlebird/sqlalchemy-challenge/blob/main/Plots/Temperature%20Observation%20for%20Station.png)

## Part 2: Design Your Climate App

### Flask API Setup

Using Flask, I created an API to serve the results of the climate analysis. The following routes are available:

- **`/`**: Home page listing all available routes.
- **`/api/v1.0/precipitation`**: Returns the last 12 months of precipitation data as a JSON dictionary, with dates as keys and precipitation values as values.
- **`/api/v1.0/stations`**: Returns a JSON list of all stations from the dataset.
- **`/api/v1.0/tobs`**: Returns a JSON list of temperature observations for the most-active station over the past year.
- **`/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`**: Returns a JSON list of the minimum, average, and maximum temperatures for a specified start or start-end date range.

### Running the Flask App

To run the Flask app, navigate to the project directory and execute:

```bash
python app.py
```

This will start the Flask server, and the API will be accessible at `http://localhost:5000/`.

![Alt.txt](https://github.com/biddlebird/sqlalchemy-challenge/blob/main/SurfsUp/app.png)

---

This README captures the work you've done and provides instructions for others to understand and use your project.
