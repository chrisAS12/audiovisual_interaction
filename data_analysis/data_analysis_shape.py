import pandas as pd
import matplotlib.pyplot as plt
import os
import scienceplots

plt.style.use(["science", "grid"])
plt.rcParams["text.usetex"] = False

combined_folders = ["individual_combined", "lab_tests_combined", "online_tests_combined"]

for folder in combined_folders:
    path = os.path.join("data", folder, "shape.csv")
    if not os.path.exists(path):
        print(f"Faila nav: {path}")
        continue

    df = pd.read_csv(path)

    choice_counts_by_freq = df.groupby(['frequency', 'clicked_item']).size().unstack(fill_value=0)
    bouba_percentage_by_freq = df.groupby('frequency')['clicked_item'].apply(lambda x: (x == 'bouba').mean() * 100)
    kiki_percentage_by_freq = df.groupby('frequency')['clicked_item'].apply(lambda x: (x == 'kiki').mean() * 100)
    rt_by_freq_and_choice = df.groupby(['frequency', 'clicked_item'])['rt'].mean().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 5))
    stacked_df = pd.DataFrame({
        'Bouba': bouba_percentage_by_freq,
        'Kiki': kiki_percentage_by_freq
    })
    stacked_df.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title(f"Izvēļu procenti pēc frekvences — {folder.replace('_combined', '')}")
    ax.set_xlabel("Frekvence (Hz)")
    ax.set_ylabel("Procenti (%)")
    ax.legend(title="Izvēle")
    plt.tight_layout()
    plt.show()


    if folder == "individual_combined":
        overall_direction = df.groupby('frequency')['clicked_item'].apply(
            lambda x: 'bouba' if (x == 'bouba').mean() >= 0.5 else 'kiki'
        )

        results = []
        for pid, group in df.groupby('participant_id'):
            individual_direction = group.groupby('frequency')['clicked_item'].apply(
                lambda x: 'bouba' if (x == 'bouba').mean() >= 0.5 else 'kiki'
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
        ax.set_title("Dalībnieku atbilstība kopējai tendencei (%) — shape tests")
        ax.set_xlabel("Sakrīt ar kopējo virzienu (%)")
        ax.set_ylabel("Dalībnieku skaits")
        plt.tight_layout()
        plt.show()
