---sleep---
with daily_sleep_split_by_time_and_type as (
  select
    date,
    case
      when extract (
        hour
        from
          start_timestamp
      ) > 20 then 'night'
      when extract (
        hour
        from
          start_timestamp
      ) < 11 then 'morning'
      else 'nap'
    end time_sleep,
    sum(hours) as hours,
    sum(
      case
        when value like '%REM%' then hours
        else 0
      end
    ) as REM_sleep,
    sum(
      case
        when value like '%Core%' then hours
        else 0
      end
    ) as Core_sleep,
    sum(
      case
        when value like '%Deep%' then hours
        else 0
      end
    ) as Deep_sleep,
    sum(
      case
        when value like '%Unspecified%' then hours
        else 0
      end
    ) as Unspecified_sleep,
    sum(
      case
        when value like '%Awake%' then hours
        else 0
      end
    ) as Awake
  from
    health.sleep
  group by
    date,case
      when extract (
        hour
        from
          start_timestamp
      ) > 20 then 'night'
      when extract (
        hour
        from
          start_timestamp
      ) < 11 then 'morning'
      else 'nap'
    end
) 

--select * from daily_sleep_split_by_time_and_type where date in ('2025-08-29','2025-08-30','2025-08-31') order by 1 desc;
--select * from health.sleep where date in ('2025-08-29','2025-08-30','2025-08-31') order by 5,1
,
daily_sleep_type as (
  select
    s1.date,
    nullif(
      sum(
        case
          when s1.time_sleep = 'night' then s1.hours
          else 0
        end + case
          when s2.time_sleep = 'morning' then s2.hours
          else 0
        end
      ),
      0
    ) as night_sleep_hrs,
    nullif(
      sum(
        case
          when s1.time_sleep = 'nap' then s1.hours
          else 0
        end
      ),
      0
    ) as nap_hrs,
    nullif(
      sum(
        case
          when s1.time_sleep = 'night' then s1.REM_sleep
          else 0
        end + case
          when s2.time_sleep = 'morning' then s2.REM_sleep
          else 0
        end
      ),
      0
    ) as REM_sleep,
    nullif(
      sum(
        case
          when s1.time_sleep = 'night' then s1.Core_sleep
          else 0
        end + case
          when s2.time_sleep = 'morning' then s2.Core_sleep
          else 0
        end
      ),
      0
    ) as Core_sleep,
    nullif(
      sum(
        case
          when s1.time_sleep = 'night' then s1.Deep_sleep
          else 0
        end + case
          when s2.time_sleep = 'morning' then s2.Deep_sleep
          else 0
        end
      ),
      0
    ) as Deep_sleep,
    nullif(
      sum(
        case
          when s1.time_sleep = 'night' then s1.Awake
          else 0
        end + case
          when s2.time_sleep = 'morning' then s2.Awake
          else 0
        end
      ),
      0
    ) as Awake,
    nullif(
      sum(
        case
          when s1.time_sleep = 'night' then s1.Unspecified_sleep
          else 0
        end + case
          when s2.time_sleep = 'morning' then s2.Unspecified_sleep
          else 0
        end
      ),
      0
    ) as Unspecified_sleep
  from
    daily_sleep_split_by_time_and_type s1
    left join daily_sleep_split_by_time_and_type s2 on s1.date + 1 = s2.date
  group by
    s1.date
  order by
    1
) 

--select * from daily_sleep where date >= '2025-08-29';
--select * from health.sleep where date >= '2025-08-29'
,
daily_sleep_timings as (
  select
    s1.date,
    cast(
      max(
        case
          when extract (
            hour
            from
              start_timestamp
          ) < 11 then to_char(start_timestamp, 'HH24.MI')
          else NULL
        end
      ) as float
    ) as wake_time,
    cast(
      coalesce(
        min(
          case
            when extract (
              hour
              from
                start_timestamp
            ) > 20 then to_char(start_timestamp, 'HH24.MI')
            else NULL
          end
        ),
        cast(min(s2.sleep_time) as text)
      ) as float
    ) as sleep_time
  from
    health.sleep s1
    join (
      select
        date,
        cast(
          min (to_char(start_timestamp, 'HH24.MI')) as float
        ) + 24 as sleep_time
      from
        health.sleep
      where
        extract (
          hour
          from
            start_timestamp
        ) < 3
      group by
        date
    ) s2 on s1.date + 1 = s2.date --where
    --s1.date > '2025-01-21'
    --and date = '2025-01-27'
  group by
    s1.date
  order by
    s1.date
),
daily_sleep as (
  select
    sl_tp.date,
    night_sleep_hrs,
    nap_hrs,
    REM_sleep as rem_sleep_hrs,
    Core_sleep as core_sleep_hrs,
    Deep_sleep as deep_sleep_hrs,
    Awake as awake_sleep_hrs,
    Unspecified_sleep as unspecified_sleep_hrs,
    wake_time,
    sleep_time
  from
    daily_sleep_type sl_tp
    join daily_sleep_timings sl_tm on sl_tp.date = sl_tm.date
) 

--select * from daily_sleep
,
weekly_sleep_std_dev as (
  select
    extract (
      year
      from
        date
    ) as year_,
    extract (
      week
      from
        date
    ) as week_,
    stddev(wake_time),
    stddev(sleep_time)
  from
    daily_sleep_timings
  group by
    extract (
      year
      from
        date
    ),
    extract (
      week
      from
        date
    )
)

---steps---
,
daily_steps as (
  select
    date,case
      when sum(steps) > 8000 then 'yes'
    end as goal_reached,
    sum(steps) as step_count,
    SUM(
      CASE
        WHEN (
          steps / NULLIF(
            EXTRACT(
              EPOCH
              FROM
                (end_timestamp - start_timestamp)
            ),
            0
          )
        ) * 60 > 100 THEN EXTRACT(
          EPOCH
          FROM
            (end_timestamp - start_timestamp)
        ) / 60.0
        ELSE NULL
      END
    ) AS total_active_minutes
  from
    health.steps
  group by
    date
) 

--select * from daily_step_count order by date
,
weekly_step_trend as (
  select
    extract (
      year
      from
        date
    ) as year_,
    extract (
      week
      from
        date
    ) as week_,
    stddev(step_count) std_dev,
    count(goal_reached) goal_reached_times,
    max(step_count) max_steps,
    min(step_count) min_steps
  from
    daily_steps
  group by
    extract (
      year
      from
        date
    ),
    extract (
      week
      from
        date
    )
  order by
    1,
    2
) 

--select * from weekly_step_trend;

---heart---

,
heart_observation as (
  select
    h.date,
    bpm,
    cast(to_char(h.timestamp, 'HH24.MI') as float) obv_ts,
    timestamp,
    case
      when s.date is null then 'asleep'
      else 'awake'
    end as obv_type
  from
    health.heart h
    left join daily_sleep_timings s on cast(to_char(timestamp, 'HH24.MI') as float) between s.wake_time
    and s.sleep_time
),
daily_hr as (
  select
    date,
    stddev(bpm) as stddev_bpm,
    PERCENTILE_CONT(0.5) WITHIN GROUP (
      ORDER BY
        bpm
    ) AS median_bpm,
    avg(bpm) as mean_bpm,
    min(bpm) as min_bpm,
    max(bpm) as max_bpm,
    count(
      case
        when bpm > 120 then 1
      end
    ) as elevated_bpm_count
  from
    health.heart
  group by
    date
) 

--select * from daily_hr
--where date > '2025-01-01'


---combined ---
,
daily_combined as (
  select
    hr.date,
    st.step_count,
    st.total_active_minutes,
    night_sleep_hrs,
    nap_hrs,
    rem_sleep_hrs,
    core_sleep_hrs,
    deep_sleep_hrs,
    awake_sleep_hrs,
    unspecified_sleep_hrs,
    wake_time,
    sleep_time,
    stddev_bpm,
    median_bpm,
    mean_bpm,
    min_bpm,
    max_bpm,
    elevated_bpm_count
  from
    daily_hr hr
    left join daily_steps st on hr.date = st.date
    left join daily_sleep sl on hr.date = sl.date
)
select
  *
from
  daily_combined
