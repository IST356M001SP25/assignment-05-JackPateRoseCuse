import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

survey_data = pd.read_csv('cache/survey.csv')

states_data = pd.read_csv('cache/states.csv')

cols = []
for year in survey_data['year'].unique():
    col = pd.read_csv(f'cache/col_{year}.csv')
    cols.append(col)

col_data = pd.concat(cols, ignore_index=True)

survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)
survey_states_combined = survey_data.merge(states_data, left_on="if you're in the US., what state do you work in?", right_on='State', how='inner')
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']

combined = survey_states_combined.merge(col_data, left_on = ['year', '_full_city'], right_on = ['year', 'full_city'], how='inner')
combined["_annual_salary_cleaned"] = combined['What is your annual base salary?'].apply(pl.clean_currency) # Clean the salary column first
combined["_annual_salary_cleaned"] = combined.apply(lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']), axis=1)
