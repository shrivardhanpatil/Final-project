import pandas as pd
from wordcloud import WordCloud

# Load the sentiment analysis results
results_df = pd.read_csv("sentiment_analysis_results.csv")

# Standardize the Sentiment column to have capitalized first letters
results_df['Sentiment'] = results_df['Sentiment'].str.capitalize()

# Display the first few rows of the data
print("First few rows of the data:")
print(results_df.head())

# Filter rows with negative sentiment
negative_feedback = results_df[results_df['Sentiment'] == 'Negative']

# Display negative feedback
print("\nNegative Feedback:")
print(negative_feedback[['Feedback', 'Positive Score', 'Neutral Score', 'Negative Score']])

# List of keywords to search for in the feedback
keywords = ['waiting', 'doctor', 'staff', 'medicine', 'cleanliness', 'care', 'treatment', 'availability', 'service']

# Function to check for keywords in feedback
def check_keywords(feedback, keywords):
    found_keywords = [keyword for keyword in keywords if keyword in feedback.lower()]
    return found_keywords

# Apply the function to find keywords in negative feedback
negative_feedback['Issues'] = negative_feedback['Feedback'].apply(lambda x: check_keywords(x, keywords))

# Display negative feedback with identified issues
print("\nNegative Feedback with Identified Issues:")
print(negative_feedback[['Feedback', 'Issues']])

# Count the occurrences of each keyword in the negative feedback
all_issues = negative_feedback['Issues'].explode().dropna().value_counts()

# Display the most common issues
print("\nMost Common Issues:")
print(all_issues)

# No word cloud generation or plotting
if negative_feedback.empty:
    print("No negative feedback available for analysis.")

