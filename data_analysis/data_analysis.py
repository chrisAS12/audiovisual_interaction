import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
import numpy as np

plt.style.use(["science", "grid"])
plt.rcParams["text.usetex"] = False

df_participants = pd.read_csv("data/individual_combined/participants.csv")

df_participants['age'] = pd.to_numeric(df_participants['age'], errors='coerce')

fig, ax = plt.subplots(figsize=(8, 6))
df_participants['age'].value_counts().sort_index().plot(kind='bar', ax=ax)
ax.set_title("Dalībnieku sadalījums pēc vecuma")
ax.set_xlabel("Vecums")
ax.set_ylabel("Dalībnieku skaits")
plt.tight_layout()
plt.show()

gender_counts = df_participants['gender'].value_counts(dropna=True)
gender_percent = gender_counts / gender_counts.sum() * 100

print("Dalībnieku sadalījums pa dzimumiem.")
for gender, count in gender_counts.items():
    percent = gender_percent[gender]
    print(f"{gender}: {count} ({percent:.1f}%)")

fig, ax = plt.subplots(figsize=(6, 5))
gender_counts.plot(kind='bar', ax=ax)
ax.set_title("Dalībnieku sadalījums pa dzimumiem.")
ax.set_xlabel("Dzimums")
ax.set_ylabel("Dalībnieku skaits")
plt.tight_layout()
plt.show()

median_age = df_participants['age'].median()
print(f"Mediānas vecums: {median_age}")

average_age = df_participants['age'].mean()
print(f"Vidējais vecums: {average_age:.2f}")

df_participants['age_group'] = pd.cut(df_participants['age'], bins=[0, 20, 30, 100], labels=['<21', '21–30', '30+'])

df_participants['age_group'].value_counts().sort_index().plot(
    kind='bar',
    title='Dalībnieku sadalījums pēc vecuma grupām'
)
plt.xlabel("Vecuma grupa")
plt.ylabel("Dalībnieku skaits")
plt.tight_layout()
plt.show()

df_combined = pd.read_csv("data/individual_combined/combined_output.csv")

left_right_counts = df_combined['clicked_position'].value_counts()
total = left_right_counts.sum()

for side, count in left_right_counts.items():
    percent = count / total * 100
    print(f"{side.capitalize()} izvēlējās {count} reizes ({percent:.1f}%)")

df_combined = df_combined.dropna(subset=['clicked_item', 'left_item', 'right_item'])

df_combined['choice_side'] = df_combined.apply(
    lambda row: 'left' if row['clicked_item'] == row['left_item'] else
                'right' if row['clicked_item'] == row['right_item'] else
                'unknown',
    axis=1
)

side_counts = df_combined.groupby(['participant_id', 'choice_side']).size().unstack(fill_value=0)

side_counts['total'] = side_counts.sum(axis=1)
side_counts['left_percent'] = side_counts['left'] / side_counts['total'] * 100
side_counts['right_percent'] = side_counts['right'] / side_counts['total'] * 100

print("left/right bias individuali dalibniekiem")
print(side_counts[['left', 'right', 'left_percent', 'right_percent']])

df_combined = df_combined.dropna(subset=['frequency', 'rt'])

rt_stats = df_combined.groupby(['test', 'frequency'])['rt'].agg(['mean', 'median']).reset_index()

freq_order = [100, 500, 1000, 5000, 9000]
freq_to_pos = {freq: i for i, freq in enumerate(freq_order)}

for test in rt_stats['test'].unique():
    df_test = rt_stats[rt_stats['test'] == test].sort_values('frequency')
    df_test['pos'] = df_test['frequency'].map(freq_to_pos)
    print(f"\nTesta veids: {test}")
    print(df_test[['frequency', 'mean', 'median']])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df_test['pos'], df_test['mean'], marker='o', label='Vidējais')
    ax.scatter(df_test['pos'], df_test['median'], marker='s', label='Mediāna')
    ax.set_xticks(list(freq_to_pos.values()))
    ax.set_xticklabels([str(f) for f in freq_order])
    if test == "size":
        ax.set_title(f"Reakcijas laiks (ms) pēc frekvences (Hz) lielumam abu grupu dalībniekiem")
    elif test == "colour":
        ax.set_title(f"Reakcijas laiks(ms) pēc frekvences (Hz) krāsai abu grupu dalībniekiem")
    elif test == "shape":
        ax.set_title(f"Reakcijas laiks (ms) pēc frekvences (Hz) formai abu grupu dalībniekiem")
    
    ax.set_xlabel("Frekvence (Hz)")
    ax.set_ylabel("Reakcijas laiks (ms)")
    ax.legend()
    plt.tight_layout()
    plt.show()

 # visiem testiem kopā
fig, ax = plt.subplots(figsize=(10, 5))
for test in rt_stats['test'].unique():
    df_test = rt_stats[rt_stats['test'] == test].sort_values('frequency')
    ax.scatter(df_test['frequency'], df_test['mean'], label=f"{test} (Vidējais)", marker='o')

ax.set_xlim(-1000, rt_stats['frequency'].max() + 1000)
ax.set_xticks([100, 500, 1000, 5000, 9000])
ax.set_title("Kopējais reakcijas laiks pēc frekvences (Hz) visu tipu testiem")
ax.set_xlabel("Frekvence (Hz)")
ax.set_ylabel("Reakcijas laiks (ms)")
ax.legend()
plt.tight_layout()
plt.show()


#visu testu reakcijas laiks
overall_rt_stats = df_combined.groupby('frequency')['rt'].agg(['mean', 'median']).reset_index()

print("Kopējie reakcijas laiki pēc frekvencēm (visiem testu tipiem kopā):")
print(overall_rt_stats)

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(overall_rt_stats['frequency'], overall_rt_stats['mean'], marker='o', label='Vidējais')
ax.scatter(overall_rt_stats['frequency'], overall_rt_stats['median'], marker='s', label='Mediāna')
ax.set_xlim(-1000, overall_rt_stats['frequency'].max() + 1000)
ax.set_xticks([100, 500, 1000, 5000, 9000])
ax.set_title("Reakcijas laiks pēc frekvences (Hz) visiem testu tipiem kopā")
ax.set_xlabel("Frekvence (Hz)")
ax.set_ylabel("Reakcijas laiks (ms)")
ax.legend()
plt.tight_layout()
plt.show()


rt_stats_all = df_combined.groupby(['test', 'frequency'])['rt'].agg(['mean', 'median']).reset_index()
rt_stats_combined = df_combined.groupby(['frequency'])['rt'].agg(['mean', 'median']).reset_index()
rt_stats_combined['test'] = 'combined'
rt_stats_final = pd.concat([rt_stats_all, rt_stats_combined], ignore_index=True)
rt_stats_final = rt_stats_final.sort_values(['test', 'frequency'])


rt_stats_final['mean_diff'] = rt_stats_final.groupby('test')['mean'].diff()
rt_stats_final['median_diff'] = rt_stats_final.groupby('test')['median'].diff()
result_table = rt_stats_final.pivot_table(index=['test', 'frequency'],
                                          values=['mean', 'mean_diff', 'median', 'median_diff'])
with pd.option_context('display.float_format', '{:,.2f}'.format):
    print(result_table)


df = overall_rt_stats
avg_rt = df.groupby('frequency')['mean'].mean().reset_index()
x = avg_rt['frequency'].values
y = avg_rt['mean'].values
coefficients = np.polyfit(x, y, 2) # izmantojot numpy polinomu fit funkciju, varam iegūt polinoma vidējos koeficientus
a, b, c = coefficients
print(f"y = {a:.4e} * x^2 + {b:.4e} * x + {c:.4f}")