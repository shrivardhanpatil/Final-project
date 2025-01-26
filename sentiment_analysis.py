import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Azure credentials
API_KEY = "5kywR4Bi70yO264WciA0xanfKr1J7L8EDFnFOuBTB79NWCgEwhsRJQQJ99BAAC1i4TkXJ3w3AAAaACOGJ4yS"
ENDPOINT = "https://sentianalysis.cognitiveservices.azure.com/"

# Authenticate with Azure
def authenticate_client():
    credential = AzureKeyCredential(API_KEY)
    text_analytics_client = TextAnalyticsClient(endpoint=ENDPOINT, credential=credential)
    return text_analytics_client

client = authenticate_client()

def analyze_sentiment(client, feedback_list):
    results = client.analyze_sentiment(documents=feedback_list)
    sentiments = []

    total_positive = 0
    total_neutral = 0
    total_negative = 0

    for idx, result in enumerate(results):
        if not result.is_error:
            sentiments.append({
                "Feedback": feedback_list[idx],
                "Sentiment": result.sentiment,
                "Positive Score": result.confidence_scores.positive,
                "Neutral Score": result.confidence_scores.neutral,
                "Negative Score": result.confidence_scores.negative
            })
            
            # Accumulate the sentiment scores for overall analysis
            total_positive += result.confidence_scores.positive
            total_neutral += result.confidence_scores.neutral
            total_negative += result.confidence_scores.negative
        else:
            sentiments.append({
                "Feedback": feedback_list[idx],
                "Sentiment": "Error",
                "Positive Score": 0,
                "Neutral Score": 0,
                "Negative Score": 0
            })

    # Calculate overall sentiment percentages
    total_feedbacks = len(feedback_list)
    overall_positive = (total_positive / total_feedbacks) * 100
    overall_neutral = (total_neutral / total_feedbacks) * 100
    overall_negative = (total_negative / total_feedbacks) * 100

    return sentiments, overall_positive, overall_neutral, overall_negative

# Function to get feedback either from user input or from a CSV file
def get_feedback_input():
    choice = input("Would you like to analyze feedback from a CSV file or provide input manually? (Enter 'csv' or 'manual'): ").lower()

    if choice == 'csv':
        file_path = input("Enter the CSV file path: ")
        try:
            data = pd.read_csv(file_path)
            feedback_list = data["Feedback"].tolist()
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return None
    elif choice == 'manual':
        feedback_list = []
        print("Enter the feedback (type 'done' when finished):")
        while True:
            feedback = input("Feedback: ")
            if feedback.lower() == 'done':
                break
            feedback_list.append(feedback)
    else:
        print("Invalid choice. Please enter 'csv' or 'manual'.")
        return None
    
    return feedback_list

# Get the feedback from user input or CSV file
feedback_list = get_feedback_input()

if feedback_list is not None:
    # Perform sentiment analysis line by line
    results, overall_positive, overall_neutral, overall_negative = analyze_sentiment(client, feedback_list)

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Display results line by line
    print("\nSentiment Analysis for each line:")
    print(results_df)

    # Display overall sentiment percentage
    print("\nOverall Sentiment (in percentage):")
    print(f"Positive: {overall_positive:.2f}%")
    print(f"Neutral: {overall_neutral:.2f}%")
    print(f"Negative: {overall_negative:.2f}%")

    # Save the results to a CSV file
    results_df.to_csv("sentiment_analysis_results.csv", index=False)
    print("Results saved to sentiment_analysis_results.csv")
