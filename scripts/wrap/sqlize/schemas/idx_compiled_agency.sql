CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_station_name
    ON compiled_agency('station_name');

CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_ship_date
    ON compiled_agency('ship_date');


CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_file_date
    ON compiled_agency('file_date');

CREATE INDEX IF NOT EXISTS
    idx_compiledstateagency_on_unique_order
    ON compiled_agency('station_name', 'tx', 'item_name', 'quantity', 'ship_date', 'file_date');


