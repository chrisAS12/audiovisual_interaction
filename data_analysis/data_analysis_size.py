import pandas as pd
import os
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["science", "grid"])
plt.rcParams["text.usetex"] = False

combined_folders = ["individual_combined", "lab_tests_combined", "online_tests_combined"]

def classify_choice(row):
    left = row['left_item']
    right = row['right_item']
    clicked = row['clicked_item']

    if pd.isna(left) or pd.isna(right) or pd.isna(clicked):
        return 'unknown'
    if left == right:
        return 'equal'
    try:
        larger = max(left, right)
        smaller = min(left, right)
    except:
        return 'unknown'
    if clicked == larger:
        return 'larger'
    elif clicked == smaller:
        return 'smaller'
    else:
        return 'unknown'

for folder in combined_folders:
    path = os.path.join("data", folder, "size.csv")
    if not os.path.exists(path):
        print(f"Faila nav: {path}")
        continue

    df = pd.read_csv(path)
    df['choice_type'] = df.apply(classify_choice, axis=1)
    summary = df.groupby(['frequency', 'choice_type']).size().unstack(fill_value=0)
    summary_percent = summary.div(summary.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    summary_percent.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title(f"Izvēļu sadalījums (%) pēc frekvences — {folder.replace('_combined', '')}")
    ax.set_xlabel("Frekvence (Hz)")
    ax.set_ylabel("Procenti (%)")
    ax.legend(title="Izvēle")
    plt.tight_layout()
    plt.show()

    if folder == "individual_combined":
        overall_direction = df.groupby('frequency')['choice_type'].apply(
            lambda x: 'larger' if (x == 'larger').mean() >= 0.5 else 'smaller'
        )

        results = []
        for pid, group in df.groupby('participant_id'):
            individual_direction = group.groupby('frequency')['choice_type'].apply(
                lambda x: 'larger' if (x == 'larger').mean() >= 0.5 else 'smaller'
            )
            match_freqs = (individual_direction == overall_direction[individual_direction.index])
            percent_match = match_freqs.mean() * 100
            results.append((pid, percent_match))
            
        for pid, percent in results:
            status = "SAKRĪT" if percent == 100 else f"{percent:.0f}% sakrīt"
            print(f"{pid:20s}: {status}")

        match_df = pd.DataFrame(results, columns=["participant_id", "percent_match"])
        fig, ax = plt.subplots(figsize=(10, 6))
        match_df['percent_match'].plot(kind='hist', bins=10, edgecolor='black', ax=ax)
        ax.set_title("Dalībnieku atbilstība kopējai tendencei (%)")
        ax.set_xlabel("Sakrīt ar kopējo virzienu (%)")
        ax.set_ylabel("Dalībnieku skaits")
        plt.tight_layout()
        plt.show()
