import openai, pandas as pd
from jinja2 import Environment, FileSystemLoader

openai.api_key = "YOUR_API_KEY"
data = pd.read_csv("../data/log_samples.csv")
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('log_analysis_template.j2')
variants = ['instruction', 'soc_analyst', 'few_shot']
results = []

for variant in variants:
    for _, row in data.iterrows():
        prompt = template.render(variant=variant, log_entry=row['Log_Entry'])
        response = openai.ChatCompletion.create(model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}])
        results.append({"Log_ID": row['Log_ID'], "Variant": variant, "LLM_Output": response.choices[0].message.content.strip()})

pd.DataFrame(results).to_csv("../results/analysis_results.csv", index=False)