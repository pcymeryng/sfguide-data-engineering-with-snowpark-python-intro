import re
import requests
import pandas as pd
import config as cfg
import langchain_community
from eodhd import APIClient
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

api_key = '65c4e7e8a79ed4.69872698'
api = APIClient(api_key)

resp = api.financial_news(s = "AMZN.US", from_date = '2024-01-01', to_date = '2024-01-30', limit = 100)
df = pd.DataFrame(resp) # converting the json output into datframe
df.tail()

#funtion to clean the textual data
def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    return cleaned_text.strip()

# Apply the replacement function to the entire column
df['content'] = df['content'].apply(clean_text)

llm = ChatOpenAI(model = "gpt-3.5-turbo",
                 openai_api_key = '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', 
                 temperature = 0)

template = """
Identify the sentiment towards the Apple(AAPL) stocks from the news article , where the sentiment score should be from -10 to +10 where -10 being the most negative and +10 being the most positve , and 0 being neutral

Also give the proper explanation for your answers and how would it effect the prices of different stocks

Article : {statement}
"""

#forming prompt using Langchain PromptTemplate functionality
prompt = PromptTemplate(template = template, input_variables = ["statement"])
llm_chain = LLMChain(prompt = prompt, llm = llm)

print(llm_chain.invoke(df['content'][13]))


#A function to count the number of tokens
def count_tokens(text):
    tokens = text.split()  
    return len(tokens)

# Applying the tokenization function to the DataFrame column
df['TokenCount'] = df['content'].apply(count_tokens)

# Define a token count threshold (for example, keep rows with more than 2 tokens)
token_count_threshold = 3500

# Create a new DataFrame by filtering based on the token count
new_df = df[df['TokenCount'] < token_count_threshold]

# Drop the 'TokenCount' column from the new DataFrame if you don't need it
new_df = new_df.drop('TokenCount', axis = 1)

# Resetting the index
new_df = new_df.reset_index(drop = True)

template_2 = """
Identify the sentiment towards the Apple(AAPL) stocks of the news article from -10 to +10 where -10 being the most negative and +10 being the most positve , and 0 being neutral

GIVE ANSWER IN ONLY ONE WORD AND THAT SHOULD BE THE SCORE

Article : {statement}
"""

#forming prompt using Langchain PromptTemplate functionality
prompt_2 = PromptTemplate(template = template_2, input_variables = ["statement"])

llm_chain_2 = LLMChain(prompt = prompt_2, llm = llm)

print(new_df['content'][2])
print('')
print('News sentiment: ', llm_chain_2.invoke(new_df['content'][2]))

x = []
for i in range(0,new_df.shape[0]):
    x.append(llm_chain_2.run(new_df['content'][i]))

# graficar
import matplotlib.pyplot as plt

dt = pd.DataFrame(x) #Converting into Dataframe
column_name = 0 # this is my column name you should change it according to your data
value_counts = dt[column_name].value_counts()

# Plotting the pie chart
plt.pie(value_counts, labels = value_counts.index, autopct = '%1.1f%%', startangle = 140)
plt.title(f'Pie Chart')
plt.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

# Show the pie chart
plt.show()

# remover valores neutrales
value_to_remove = '0'
# Remove all rows where the specified value occurs in the column
dt_new = dt[dt[0] != value_to_remove]

# ver la data nueva
value_counts = dt_new[column_name].value_counts()

# Plotting the pie chart
plt.pie(value_counts, labels = value_counts.index, autopct = '%1.1f%%', startangle = 140)
plt.title(f'Pie Chart')
plt.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

# Show the pie chart
plt.show()

