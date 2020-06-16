CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_station_name
    ON compiled_agency(station_name);

CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_ship_date
    ON compiled_agency(ship_date);


CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_file_date
    ON compiled_agency(file_date);

CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_unique_order
    ON compiled_agency(station_name, state, item_name, quantity, ship_date, file_date);


CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_agencyfile
    ON compiled_agency(state, station_name, file_date);



DROP VIEW IF EXISTS agency_files_summary;
CREATE VIEW agency_files_summary AS
WITH usums AS (
        SELECT state
            , station_name
            , file_date
            , COUNT(1) as order_count
        FROM compiled_agency
        GROUP BY state, station_name, file_date
        ORDER BY state, station_name, file_date
    )
    , ua AS (
    SELECT state
        , station_name
        , COUNT(1) AS file_count
        , SUM(order_count) AS order_count
        , MIN(file_date) AS oldest_date
        , MAX(file_date) AS latest_date
    FROM usums
    GROUP BY state, station_name
    ORDER BY state, station_name
)
SELECT *
FROM ua;
