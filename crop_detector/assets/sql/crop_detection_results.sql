-- create table in default schema

CREATE TABLE crop_detection_results
(
    `crop` String,
    `alternate_names` Array(String),
    `color` Array(String),
    `confidence` Float32,
    `startDateTime` DateTime,
    `endDateTime` DateTime,
    `duration` Float32
)
ENGINE = MergeTree
ORDER BY startDateTime;