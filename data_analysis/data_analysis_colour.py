import pandas as pd
import matplotlib.pyplot as plt
import os
import scienceplots

plt.style.use(["science", "grid"])
plt.rcParams["text.usetex"] = False

combined_folders = ["individual_combined", "lab_tests_combined", "online_tests_combined"]

def classify_brightness(row):
    left = row['left_item']
    right = row['right_item']
    clicked = row['clicked_item']
    if pd.isna(left) or pd.isna(right) or pd.isna(clicked):
        return 'unknown'
    if left == right:
        return 'ignore'
    brighter = max(left, right)
    if clicked == brighter:
        return 'brighter'
    else:
        return 'darker'

for folder in combined_folders:
    path = os.path.join("data", folder, "colour.csv")
    if not os.path.exists(path):
        print(f"Faila nav: {path}")
        continue

    df = pd.read_csv(path)
    df['choice_type'] = df.apply(classify_brightness, axis=1)
    df = df[df['choice_type'] != 'ignore']

    print(df)

    summary = df.groupby(['frequency', 'choice_type']).size().unstack(fill_value=0)
    print(summary)

    summary_percent = summary.div(summary.sum(axis=1), axis=0) * 100
    print(summary_percent)

    fig, ax = plt.subplots(figsize=(10, 5))
    summary_percent.plot(kind='bar', stacked=True, ax=ax)
    if folder == "individual_combined":
            ax.set_title(f"Izvēles procenti (%) krāsai pēc frekvences (Hz) abu grupu dalībniekiem")
    elif folder == "lab_tests_combined":
            ax.set_title(f"Izvēles procenti (%) krāsai pēc frekvences (Hz) kontrolētās grupas dalībniekiem")
    elif folder == "online_tests_combined":
        ax.set_title(f"Izvēles procenti (%) krāsai pēc frekvences (Hz) nekontrolētās grupas dalībniekiem")
    ax.set_xlabel("Frekvence (Hz)")
    ax.set_ylabel("Procenti (%)")
    ax.legend(title="Izvēle")
    plt.tight_layout()
    plt.show()

    if folder == "individual_combined":
        overall_direction = df.groupby('frequency')['choice_type'].apply(
            lambda x: 'brighter' if (x == 'brighter').mean() >= 0.5 else 'darker'
        )

        print("overall_direction")
        print(overall_direction)

        results = []
        for pid, group in df.groupby('participant_id'):
            individual_direction = group.groupby('frequency')['choice_type'].apply(
                lambda x: 'brighter' if (x == 'brighter').mean() >= 0.5 else 'darker'
            )

            print(f"dalībnieks {pid}")
            print(individual_direction)

            match_freqs = (individual_direction == overall_direction[individual_direction.index])
            percent_match = match_freqs.mean() * 100
            results.append((pid, percent_match))

        print("\n iondividuāli rezultāti")
        for pid, percent in results:
            status = "SAKRĪT" if percent == 100 else f"{percent:.0f}% sakrīt"
            print(f"{pid:20s}: {status}")

        match_df = pd.DataFrame(results, columns=["participant_id", "percent_match"])
        print("\n match_df")
        print(match_df)

        fig, ax = plt.subplots(figsize=(10, 6))
        match_df['percent_match'].plot(kind='hist', bins=10, edgecolor='black', ax=ax)
        ax.set_title("Dalībnieku atbilstība kopējai tendencei (%)")
        ax.set_xlabel("Sakrīt ar kopējo virzienu (%)")
        ax.set_ylabel("Dalībnieku skaits")
        plt.tight_layout()
        plt.show()
