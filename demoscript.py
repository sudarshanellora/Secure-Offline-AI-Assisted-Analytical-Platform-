import pandas as pd
import ollama
import matplotlib.pyplot as plt
import time
import os


def print_executive_brief(title, text):
    print(f"\n📌 {title}")
    print("-" * 60)
    for line in text.split("\n"):
        line = line.strip()
        if line:
            print("•", line)


print("\n" + "=" * 70)
print("[SYSTEM] Secure Offline Demand Analytics Demo")
print("=" * 70)
time.sleep(0.5)

model = "llama3"


data_file = input("\n📂 Enter demo data file (default: master_data.csv): ").strip()
if data_file == "":
    data_file = "master_data.csv"

if not os.path.exists(data_file):
    print("[FATAL] Data file not found.")
    exit()

df = pd.read_csv(data_file)

print("[DATA] Dataset loaded successfully")
print(f"[DATA] Columns detected: {list(df.columns)}")
print("[SECURITY] Data remains local and offline")

print("\n📊 Choose categorical dimension:")
print("1 → Branch")
print("2 → District")

choice = input("👉 Enter choice (1 or 2): ").strip()
group_col = "district" if choice == "2" else "branch"

print(f"[INPUT] Grouping demand by: {group_col}")


print("\n💬 Enter your business question")
print("Example: Analyse demand patterns and operational risks")

user_prompt = input("👉 Your prompt: ").strip()
if user_prompt == "":
    user_prompt = f"Analyse demand patterns by {group_col} and location"


print("\n📐 Calculating verified metrics...")
time.sleep(0.5)

# Graph 1 data
avg_demand_group = (
    df.groupby(group_col)["demand"]
    .mean()
    .sort_values(ascending=False)
)

# Graph 2 data
trend_df = (
    df.groupby("month")["demand"]
    .mean()
    .sort_index()
)

# Graph 3 data
geo_df = df[["lat", "long", "demand"]].dropna()


summary_1 = "\n".join(
    [f"{k}: {v:.2f}" for k, v in avg_demand_group.items()]
)

prompt_1 = f"""
You are a senior operations analytics consultant.

Business question:
{user_prompt}

Below is average demand grouped by {group_col}:

{summary_1}

Explain:
1. What this distribution shows
2. Which groups stand out
3. Why leadership should care

Keep it concise.
"""

response_1 = ollama.chat(
    model=model,
    messages=[{"role": "user", "content": prompt_1}]
)

print_executive_brief(
    f"Insight 1 – Demand by {group_col.title()}",
    response_1["message"]["content"]
)


plt.figure(figsize=(11, 6))
plt.bar(avg_demand_group.index.astype(str), avg_demand_group.values)

plt.title(f"Average Demand by {group_col.title()}", fontsize=15, weight="bold")
plt.xlabel(group_col.title())
plt.ylabel("Average Demand")
plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

summary_2 = "\n".join(
    [f"{k}: {v:.2f}" for k, v in trend_df.items()]
)

prompt_2 = f"""
You are analysing demand trends over time.

Below is average demand by month:

{summary_2}

Explain:
1. Trend or seasonality
2. Any volatility or risk
3. Planning implications

Keep it concise.
"""

response_2 = ollama.chat(
    model=model,
    messages=[{"role": "user", "content": prompt_2}]
)

print_executive_brief(
    "Insight 2 – Demand Trend Over Time",
    response_2["message"]["content"]
)


plt.figure(figsize=(11, 6))
plt.plot(trend_df.index, trend_df.values, marker="o")

plt.title("Average Demand Trend Over Time", fontsize=15, weight="bold")
plt.xlabel("Month")
plt.ylabel("Average Demand")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()


geo_summary = (
    f"Latitude range: {geo_df['lat'].min():.2f} to {geo_df['lat'].max():.2f}\n"
    f"Longitude range: {geo_df['long'].min():.2f} to {geo_df['long'].max():.2f}\n"
    f"Demand range: {geo_df['demand'].min():.2f} to {geo_df['demand'].max():.2f}"
)

prompt_3 = f"""
You are analysing geographic demand distribution.

{geo_summary}

Explain:
1. What spatial spread of demand suggests
2. Any concentration or dispersion
3. Operational or logistics implications

Keep it concise.
"""

response_3 = ollama.chat(
    model=model,
    messages=[{"role": "user", "content": prompt_3}]
)

print_executive_brief(
    "Insight 3 – Geographic Demand Distribution",
    response_3["message"]["content"]
)


plt.figure(figsize=(10, 6))
plt.scatter(
    geo_df["long"],
    geo_df["lat"],
    s=geo_df["demand"] / geo_df["demand"].max() * 300,
    alpha=0.6
)

plt.title("Geographic Distribution of Demand", fontsize=15, weight="bold")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()

print("\n[SUCCESS] Multi-view demand analysis completed offline.")
print("=" * 70)
