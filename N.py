import pandas as pd
import nltk
import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from collections import Counter
import os

nltk.download('stopwords')

# Text preprocessing function
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text))
    text = text.lower()
    words = text.split()
    words = [word for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

# Ticket analysis function
def analyze_tickets(df):
    all_words = ' '.join(df['cleaned_text']).split()
    most_common = Counter(all_words).most_common(10)
    suggestions = {
        word: f"Consider creating a knowledge base article for '{word}'." for word, _ in most_common
    }
    return most_common, suggestions

# Report generation function
def generate_report(issues, suggestions, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write("Frequently Reported Issues:\n")
        for word, count in issues:
            f.write(f"- {word}: {count} mentions\n")
        f.write("\nRecommended Process Improvements:\n")
        for issue, suggestion in suggestions.items():
            f.write(f"- {suggestion}\n")

# Graph generation function
def show_graph(issues):
    words, counts = zip(*issues)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.title('Top 10 Frequent Issues in Support Tickets')
    plt.xlabel('Issue Keywords')
    plt.ylabel('Number of Mentions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main script to run the full process
if __name__ == "__main__":
    # Load dataset
    df = pd.read_csv('C:/Users/jayde/Downloads/customer_support_tickets/customer_support_tickets.csv')
    
    # Print column names to verify
    print("Available columns:", df.columns)

    # Preprocess ticket text using the correct column name from your CSV
    df['cleaned_text'] = df['Ticket Description'].apply(preprocess_text)

    # Analyze tickets
    frequent_issues, suggestions = analyze_tickets(df)

    # Generate text report
    generate_report(frequent_issues, suggestions, output_path='C:/Users/jayde/Downloads/summary_report.txt')

    # Display visual chart
    show_graph(frequent_issues)

    print("Analysis complete. Report generated and graph displayed.")
