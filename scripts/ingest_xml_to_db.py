from src import get_settings
from src.extract.apple_health import parse_xml
from src.extract.apple_health import extract_steps
from src.extract.apple_health import extract_sleep
from src.extract.apple_health import extract_hr
from src.db import get_engine, read_table, write_table
# from src.llm import get_llm_response

def main():
    print("I am in main")
    root = parse_xml("data/raw/export.xml")
    steps_df, steps_daily = extract_steps(root)
    sleep_df, sleep_daily = extract_sleep(root)
    hr_df, hr_daily = extract_hr(root)

    # print(steps_df.shape, steps_daily.shape)

    # TODO: convert to DataFrames and save
    write_table(steps_df, "steps", "health", get_engine())
    write_table(steps_daily, "steps_daily", "health", get_engine())
    write_table(sleep_df, "sleep", "health", get_engine())
    write_table(sleep_daily, "sleep_daily", "health", get_engine())
    write_table(hr_df, "heart", "health", get_engine())
    write_table(hr_daily, "heart_daily", "health", get_engine())

if __name__ == "__main__":
    main()
