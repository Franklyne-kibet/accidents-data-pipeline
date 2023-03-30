{{ config(materialized="view") }}

with accident_data as 
(
    select * from {{ source('staging','accidents_data') }}
)

select
    -- identifiers
    {{ dbt_utils.surrogate_key(['ID', 'Start_Time']) }} as accident_id,
    cast(ID as string) as Id,
    cast(severity as integer) as severity,
    {{ get_accident_severity( 'severity' ) }} as severity_description,

    -- timestamps
    cast(Start_Time as timestamp) as start_time,
    cast(end_time as timestamp) as end_time,
    cast(weather_timestamp as timestamp) as weather_timestamp,

    -- longitude and latitude
    cast(start_lat as integer) as start_lat,
    cast(start_lng as integer) as start_lng,
    cast(end_lat as integer) as end_lat,
    cast(end_lng as integer) as end_lng,

    -- distance
    cast(distance_miles as numeric) as distance_miles,

    -- accident description
    cast(description as string) as description,

    -- accident address
    cast(number as integer) as number,
    cast(street as string) as street,
    cast(side as string) as side,
    cast(city as string) as city,
    cast(county as string) as county,
    cast(state as string) as state,
    cast(zipcode as string) as zipcode,
    cast(country as string) as country,
    cast(timezone as string) as timezone,
    cast(airport_code as string) as airport_code,
    
    -- weather condition
    cast(temperature_F as numeric) as temperature,
    cast(wind_chill_F as numeric) as wind_chill,
    cast(humidity_perc as numeric) as humidity,
    cast(pressure_inches as numeric) as pressure,
    cast(visibility_miles as numeric) as visibility,
    cast(wind_direction as string) as wind_direction,
    cast(wind_speed_mph as numeric) as wind_speed,
    cast(precipitation_inches as numeric) as precipitation,
    cast(weather_condition as string) as weather_condition,

    -- point of interest
    cast(amenity as boolean) as amenity,
    cast(bump as boolean) as bump,
    cast(crossing as boolean) as crossing,
    cast(give_way as boolean) as give_way,
    cast(junction as boolean) as junction,
    cast(no_exit as boolean) as no_exit,
    cast(railway as boolean) as railway,
    cast(roundabout as boolean) as roundabout,
    cast(station as boolean) as station,
    cast(stop as boolean) as stop,
    cast(traffic_calming as boolean) as traffic_calming,
    cast(traffic_signal as boolean) as traffic_signal,
    cast(turning_loop as boolean) as turning_loop,

    -- period of day
    cast(sunrise_sunset as string) as sunrise_sunset,
    cast(civil_twilight as string) as civil_twilight,
    cast(nautical_twilight as string) as nautical_twilight, 
    cast(astronomical_twilight as string) as astronomical_twilight 

from accident_data

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

   --limit 100 

{% endif %}