import pandas as pd
import matplotlib.pyplot as plt
import os
import scienceplots
import numpy as np

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

    for freq, group in df.groupby('frequency'):
        bouba_pct = (group['clicked_item'] == 'bouba').mean() * 100
        kiki_pct = (group['clicked_item'] == 'kiki').mean() * 100
        print(f"Frekvence {freq} Hz — Bouba: {bouba_pct:.1f}%, Kiki: {kiki_pct:.1f}%")

    fig, ax = plt.subplots(figsize=(10, 5))
    stacked_df = pd.DataFrame({
        'Bouba': bouba_percentage_by_freq,
        'Kiki': kiki_percentage_by_freq
    })
    stacked_df.plot(kind='bar', stacked=True, ax=ax)
    if folder == "individual_combined":
            ax.set_title(f"Izvēles procenti (%) formai pēc frekvences (Hz) abu grupu dalībniekiem")
    elif folder == "lab_tests_combined":
            ax.set_title(f"Izvēles procenti (%) formai pēc frekvences (Hz) kontrolētās grupas dalībniekiem")
    elif folder == "online_tests_combined":
        ax.set_title(f"Izvēles procenti (%) formai pēc frekvences (Hz) nekontrolētās grupas dalībniekiem")
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

        counts = match_df['percent_match'].value_counts().sort_index()

        print("\nDalībnieku skaits pēc precīzās sakritības ar kopējo tendenci:")
        for percent, count in counts.items():
            print(f"{percent:>5.1f}% sakrīt: {count} dalībnieki")

        fig, ax = plt.subplots(figsize=(10, 6))
        match_df['percent_match'].plot(kind='hist', bins=10, edgecolor='black', ax=ax)
        ax.set_title("Dalībnieku atbilstība kopējai tendencei (%)")
        ax.set_xlabel("Sakrīt ar kopējo virzienu (%)")
        ax.set_ylabel("Dalībnieku skaits")
        plt.tight_layout()
        plt.show()



for folder in combined_folders:
    path = os.path.join("data", folder, "shape.csv")
    if not os.path.exists(path):
        print(f"Faila nav: {path}")
        continue

    df = pd.read_csv(path)
    total_tests = len(df)

    print(f"\n dzimumi un frekvences - {folder}")
    for gender, group in df.groupby("gender"):
        gender_tests = len(group)
        gender_pct = gender_tests / total_tests * 100

        choices = group['clicked_item']
        bouba_pct = (choices == "bouba").mean() * 100
        kiki_pct = (choices == "kiki").mean() * 100
        moda = choices.mode().iloc[0] if not choices.mode().empty else 'nav'

        print(f"\n dzimums: {gender} ({gender_tests} testi, {gender_pct:.1f}%)")
        print(f"Bouba: {bouba_pct:.1f}%")
        print(f"Kiki: {kiki_pct:.1f}%")
        print(f"Moda: {moda}")
        print(f"testi frekvencēs:")
        freq_counts = group['frequency'].value_counts().sort_index()
        for freq, count in freq_counts.items():
            freq_pct = count / gender_tests * 100
            print(f"{freq} Hz: {count} testi ({freq_pct:.1f}%)")

    print(f"\n hobiji un frekvences - {folder}")
    df['hobbies'] = df['hobbies'].apply(lambda x: eval(x) if isinstance(x, str) else [])
    all_hobbies = sorted(set(hobby for sublist in df['hobbies'] for hobby in sublist))
    for hobby in all_hobbies:
        group = df[df['hobbies'].apply(lambda x: hobby in x)]
        hobby_tests = len(group)
        hobby_pct = hobby_tests / total_tests * 100
        choices = group['clicked_item']
        bouba_pct = (choices == "bouba").mean() * 100
        kiki_pct = (choices == "kiki").mean() * 100
        moda = choices.mode().iloc[0] if not choices.mode().empty else 'nav'

        print(f"\n hobijs: {hobby} ({hobby_tests} testi, {hobby_pct:.1f}%)")
        print(f"Bouba: {bouba_pct:.1f}%")
        print(f"Kiki: {kiki_pct:.1f}%")
        print(f"Moda: {moda}")
        print(f"testi frekvencēs:")
        freq_counts = group['frequency'].value_counts().sort_index()
        for freq, count in freq_counts.items():
            freq_pct = count / hobby_tests * 100
            print(f"{freq} Hz: {count} testi ({freq_pct:.1f}%)")

    print(f"\n vecuma grupas un frekvences - {folder}")
    df['age_group'] = pd.cut(df['age'], bins=[0, 20, 30, 100], labels=['<21', '21-30', '30+'])
    for group_name, group in df.groupby("age_group"):
        group_tests = len(group)
        group_pct = group_tests / total_tests * 100
        choices = group['clicked_item']
        bouba_pct = (choices == "bouba").mean() * 100
        kiki_pct = (choices == "kiki").mean() * 100
        moda = choices.mode().iloc[0] if not choices.mode().empty else 'nav'

        print(f"\n vecuma grupa: {group_name} ({group_tests} testi, {group_pct:.1f}%)")
        print(f"Bouba: {bouba_pct:.1f}%")
        print(f"Kiki: {kiki_pct:.1f}%")
        print(f"Moda: {moda}")
        print(f"testi frekvencēs:")
        freq_counts = group['frequency'].value_counts().sort_index()
        for freq, count in freq_counts.items():
            freq_pct = count / group_tests * 100
            print(f"{freq} Hz: {count} testi ({freq_pct:.1f}%)")
