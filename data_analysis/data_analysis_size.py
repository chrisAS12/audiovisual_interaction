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
    total_tests = len(df)

    summary = df.groupby(['frequency', 'choice_type']).size().unstack(fill_value=0)
    summary_percent = summary.div(summary.sum(axis=1), axis=0) * 100
    print(summary_percent)

    fig, ax = plt.subplots(figsize=(10, 6))
    summary_percent.plot(kind='bar', stacked=True, ax=ax)
    if folder == "individual_combined":
        ax.set_title(f"Izvēles procenti (%) lielumam pēc frekvences (Hz) abu grupu dalībniekiem")
    elif folder == "lab_tests_combined":
        ax.set_title(f"Izvēles procenti (%) lielumam pēc frekvences (Hz) kontrolētās grupas dalībniekiem")
    elif folder == "online_tests_combined":
        ax.set_title(f"Izvēles procenti lielumam (%) pēc frekvences (Hz) nekontrolētās grupas dalībniekiem")
    ax.set_xlabel("Frekvence (Hz)")
    ax.set_ylabel("Procenti (%)")
    ax.legend(title="Izvēle")
    plt.tight_layout()
    plt.show()

    print(f"\n dzimumi un frekvences - {folder}")
    for gender, group in df.groupby("gender"):
        gender_tests = len(group)
        gender_pct = gender_tests / total_tests * 100
        choices = group['choice_type']
        larger_pct = (choices == "larger").mean() * 100
        smaller_pct = (choices == "smaller").mean() * 100
        moda = choices.mode().iloc[0] if not choices.mode().empty else 'nav'

        print(f"\n dzimums: {gender} ({gender_tests} testi, {gender_pct:.1f}%)")
        print(f"larger: {larger_pct:.1f}%")
        print(f"smaller: {smaller_pct:.1f}%")
        print(f"moda: {moda}")
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
        choices = group['choice_type']
        larger_pct = (choices == "larger").mean() * 100
        smaller_pct = (choices == "smaller").mean() * 100
        moda = choices.mode().iloc[0] if not choices.mode().empty else 'nav'

        print(f"\n hobijs: {hobby} ({hobby_tests} testi, {hobby_pct:.1f}%)")
        print(f"larger: {larger_pct:.1f}%")
        print(f"smaller: {smaller_pct:.1f}%")
        print(f"moda: {moda}")
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
        choices = group['choice_type']
        larger_pct = (choices == "larger").mean() * 100
        smaller_pct = (choices == "smaller").mean() * 100
        moda = choices.mode().iloc[0] if not choices.mode().empty else 'nav'

        print(f"\n vecuma grupa: {group_name} ({group_tests} testi, {group_pct:.1f}%)")
        print(f"larger: {larger_pct:.1f}%")
        print(f"smaller: {smaller_pct:.1f}%")
        print(f"moda: {moda}")
        print(f"testi frekvencēs:")
        freq_counts = group['frequency'].value_counts().sort_index()
        for freq, count in freq_counts.items():
            freq_pct = count / group_tests * 100
            print(f"{freq} Hz: {count} testi ({freq_pct:.1f}%)")

