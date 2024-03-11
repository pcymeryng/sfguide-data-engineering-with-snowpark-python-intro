EXECUTE IMMEDIATE $$
-- Snowflake Scripting code
DECLARE
  radius_of_circle FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius_of_circle := 3;
  area_of_circle := pi() * radius_of_circle * radius_of_circle;
  RETURN area_of_circle;
END;
$$
;

CREATE OR REPLACE PROCEDURE myprocedure()
  RETURNS VARCHAR
  LANGUAGE SQL
  AS
  $$
    -- Snowflake Scripting code
    DECLARE
      radius_of_circle FLOAT;
      area_of_circle FLOAT;
    BEGIN
      radius_of_circle := 3;
      area_of_circle := pi() * radius_of_circle * radius_of_circle;
      RETURN area_of_circle;
    END;
  $$
  ;


set stmt =
$$
declare
    radius_of_circle float;
    area_of_circle float;
begin
    radius_of_circle := 3;
    area_of_circle := pi() * radius_of_circle * radius_of_circle;
    return area_of_circle;
end;
$$
;

execute immediate $stmt;


DECLARE
  query_id_1 VARCHAR;
  query_id_2 VARCHAR;
BEGIN
  SELECT 1;
  query_id_1 := SQLID;
  SELECT 2;
  query_id_2 := SQLID;
  RETURN [query_id_1, query_id_2];
END;
