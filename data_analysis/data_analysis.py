import pandas as pd
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "grid"])
plt.rcParams["text.usetex"] = False

df_participants = pd.read_csv("data/individual_combined/participants.csv")

df_participants['age'] = pd.to_numeric(df_participants['age'], errors='coerce')

gender_counts = df_participants['gender'].value_counts(dropna=True)
gender_percent = gender_counts / gender_counts.sum() * 100

print("Dzimumu sadalījums:")
for gender, count in gender_counts.items():
    percent = gender_percent[gender]
    print(f"{gender}: {count} ({percent:.1f}%)")

fig, ax = plt.subplots(figsize=(6, 5))
gender_counts.plot(kind='bar', ax=ax)
ax.set_title("Dzimumu sadalījums")
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
df_combined = df_combined.dropna(subset=['frequency', 'rt'])

rt_stats = df_combined.groupby(['test', 'frequency'])['rt'].agg(['mean', 'median']).reset_index()

for test in rt_stats['test'].unique():
    df_test = rt_stats[rt_stats['test'] == test].sort_values('frequency')
    print(f"\nTesta veids: {test}")
    print(df_test[['frequency', 'mean', 'median']])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_test['frequency'], df_test['mean'], marker='o', label='Vidējais')
    ax.plot(df_test['frequency'], df_test['median'], marker='s', label='Mediāna')
    ax.set_xlim(df_test['frequency'].min(), df_test['frequency'].max())
    ax.set_title(f"Reakcijas laiks pēc frekvences — {test} tests")
    ax.set_xlabel("Frekvence (Hz)")
    ax.set_ylabel("Reakcijas laiks (ms)")
    ax.legend()
    plt.tight_layout()
    plt.show()
