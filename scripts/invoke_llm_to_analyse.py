##write code to drive following insights:

#  table_name  | column_name 
# -------------+-------------
#  heart       | bpm
#  heart       | date
#  heart       | timestamp
#  heart_daily | bpm
#  heart_daily | date
#  sleep       | date
#  sleep       | hours
#  sleep       | timestamp
#  sleep       | value
#  sleep_daily | date
#  sleep_daily | hours
#  steps       | date
#  steps       | steps
#  steps       | timestamp
#  steps_daily | date
#  steps_daily | steps


# 🫀 Heart Rate
# Resting HR (RHR): Minimum HR per night/morning.
# HR Variability (HRV): Difference between min & max, or standard deviation over a day.
# Daytime vs Nighttime HR: Mean HR in active vs sleep periods.
# Elevated HR Episodes: Count of times HR exceeds a threshold (e.g., >120 bpm).
# 😴 Sleep
# Total Sleep Duration: Hours per night.
# Sleep Efficiency: (Time asleep ÷ time in bed).
# Sleep Consistency: Standard deviation of sleep onset/wake times.
# Deep vs Light Sleep Ratio (if Apple Health distinguishes phases).
# 🚶 Steps
# Daily Step Count.
# Active Minutes: Periods of sustained steps > 100/min.
# Step Variability: Standard deviation of steps across days.
# Consistency: How many days per week you meet a target (e.g., >8k steps).
# 🪢 Combined Features
# Activity–Sleep Balance: Steps vs sleep hours correlation.
# Recovery Indicator: (Sleep duration + low resting HR the next day).
# Overtraining Signal: High steps + poor sleep + elevated resting HR.

# Making It LLM-Consumable
# You don’t want the LLM to crunch millions of raw rows. Instead, you want structured summaries. Strategies:
# Option A: Daily Summaries
# Store a table like:
# date | steps | sleep_hours | resting_hr | hrv | active_minutes | sleep_efficiency
# The LLM consumes rows for a requested period (last 7 days, last month).
# Option B: Aggregated Features
# Pre-compute:
# Averages (weekly, monthly).
# Trends (7-day rolling averages).
# Flags (e.g., "3 consecutive nights < 6h sleep").
# Option C: Feature Store / API
# Expose a simple API (or DB table) that only serves feature vectors.
# Example JSON the LLM sees:
# {
#   "last_7_days": {
#     "avg_steps": 8421,
#     "avg_sleep": 6.7,
#     "avg_resting_hr": 63,
#     "trend_sleep": "decreasing",
#     "trend_steps": "stable",
#     "trend_hr": "increasing"
#   }
# }
# Option D: Embedding Context
# You create textual summaries (like "In the past week, your average sleep was 6.7 hours, down from 7.5 the week before").
# Provide those summaries as context to the LLM instead of raw data.
# 3. Practical Pipeline
# ETL layer (your scripts): write steps_daily, sleep_daily, heart_daily.
# Feature engineering script:
# Reads those daily tables.
# Creates features_daily and features_weekly.
# Expose to LLM:
# Either via DB → API → LLM tool.
# Or pre-generate textual summaries the LLM ingests.



