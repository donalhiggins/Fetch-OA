import sys
import pandas as pd
import json

# Read in csv file
df = pd.read_csv(sys.argv[2])

# Clean data and sort by timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by='timestamp')

# Create another dataframe to store the total points of each payer
totalPoints = df.groupby('payer').sum()

# Convert dataframe to hashmap
totalPoints = dict([(key, value) for key, value in zip(totalPoints.index, totalPoints['points'])])

pointsToSpend = int(sys.argv[1])

i = 0
# Spend the points in order
while pointsToSpend > 0 and i < len(df):
    # Get the oldest points
    oldestPoints = df.iloc[i]

    # If pointsToSpend is greater than we can spend all the points at oldestPoints
    # Otherwise just spend pointsToSpend
    if pointsToSpend > oldestPoints['points']:
        # Check to make sure we don't go negative
        if oldestPoints['points'] > totalPoints[oldestPoints['payer']]:
            pointsToSpend -= totalPoints[oldestPoints['payer']]
            totalPoints[oldestPoints['payer']] = 0
        else:
            pointsToSpend -= oldestPoints['points']
            totalPoints[oldestPoints['payer']] -= oldestPoints['points']
    else:
        totalPoints[oldestPoints['payer']] -= pointsToSpend
        pointsToSpend = 0
    i += 1

# Convert int to string for JSON
totalPoints = {k: str(v) for k, v in totalPoints.items()}

# Print out the total points in JSON format
print(json.dumps(totalPoints, indent=4))
