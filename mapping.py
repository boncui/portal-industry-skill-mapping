import pandas as pd
import openai

# Load the dataset (Ensure the correct file path)
file_path = "your_dataset.csv"  # Change this to your actual dataset path
df = pd.read_csv(file_path)

# OpenAI API Key (Set your actual API key here)
openai.api_key = "your_openai_api_key"

# Define the skills (Extract from dataset headers)
skills = df.columns[2:]  # Assuming the first 2 columns are "Industry" & "Required Educational Level"

# Function to get skill importance from ChatGPT
def get_skill_importance(industry, skill):
    prompt = f"On a scale from 0 to 1, how important is '{skill}' for professionals in the '{industry}' industry? Only return a float number."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 for better accuracy
        messages=[{"role": "system", "content": "You are an expert in job industry skill analysis."},
                  {"role": "user", "content": prompt}],
        temperature=0.3  # Low randomness for consistency
    )

    try:
        return float(response["choices"][0]["message"]["content"].strip())  # Extract and convert response to float
    except:
        return 0.5  # Default to 0.5 if parsing fails

# Populate dataset with skill scores
for index, row in df.iterrows():
    industry = row["Industry"]  # Get industry name
    for skill in skills:
        df.at[index, skill] = get_skill_importance(industry, skill)

# Save the filled dataset
output_file = "encoded_industry_skills.csv"
df.to_csv(output_file, index=False)
print(f"✅ Skill importance scores saved to: {output_file}")
