--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.18
-- Dumped by pg_dump version 12.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: log_meta_data; Type: SCHEMA; Schema: -; Owner: recharge
--

CREATE SCHEMA log_meta_data;


ALTER SCHEMA log_meta_data OWNER TO recharge;

--
-- Name: worker_slot; Type: SCHEMA; Schema: -; Owner: recharge
--

CREATE SCHEMA worker_slot;


ALTER SCHEMA worker_slot OWNER TO recharge;

--
-- Name: disposition; Type: TYPE; Schema: public; Owner: recharge
--

CREATE TYPE public.disposition AS ENUM (
    'WRITE_APPEND',
    'WRITE_TRUNCATE',
    'MERGE_MODE'
);


ALTER TYPE public.disposition OWNER TO recharge;

--
-- Name: final_machine_state; Type: TYPE; Schema: public; Owner: recharge
--

CREATE TYPE public.final_machine_state AS ENUM (
    'shutdown',
    'awake',
    'delete'
);


ALTER TYPE public.final_machine_state OWNER TO recharge;

--
-- Name: spark_submit_type; Type: TYPE; Schema: public; Owner: recharge
--

CREATE TYPE public.spark_submit_type AS ENUM (
    'spark-submit',
    'python'
);


ALTER TYPE public.spark_submit_type OWNER TO recharge;

--
-- Name: target_format; Type: TYPE; Schema: public; Owner: recharge
--

CREATE TYPE public.target_format AS ENUM (
    'JSON',
    'AVRO',
    'CSV'
);


ALTER TYPE public.target_format OWNER TO recharge;

--
-- Name: process_bq_checker_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_bq_checker_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.bq_checker_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.bq_checker_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, NEW.dag_id, NEW.subdag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.bq_checker_log SELECT NEW.id, null, null, NEW.dag_id, NEW.subdag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_bq_checker_log() OWNER TO recharge;

--
-- Name: process_bq_to_bq_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_bq_to_bq_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.bq_to_bq_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.bq_to_bq_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, NEW.dag_id, NEW.subdag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.bq_to_bq_log SELECT NEW.id, null, null, NEW.dag_id, NEW.subdag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_bq_to_bq_log() OWNER TO recharge;

--
-- Name: process_bq_to_bt_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_bq_to_bt_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.bq_to_bt_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.bq_to_bt_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, NEW.dag_id, NEW.subdag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.bq_to_bt_log SELECT NEW.id, null, null, NEW.dag_id, NEW.subdag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_bq_to_bt_log() OWNER TO recharge;

--
-- Name: process_bq_to_gs_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_bq_to_gs_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.bq_to_gs_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.bq_to_gs_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, NEW.dag_id, NEW.subdag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.bq_to_gs_log SELECT NEW.id, null, null, NEW.dag_id, NEW.subdag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_bq_to_gs_log() OWNER TO recharge;

--
-- Name: process_bq_to_pubsub_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_bq_to_pubsub_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.bq_to_pubsub_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.bq_to_pubsub_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, NEW.dag_id, NEW.subdag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.bq_to_pubsub_log SELECT NEW.id, null, null, NEW.dag_id, NEW.subdag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_bq_to_pubsub_log() OWNER TO recharge;

--
-- Name: process_database_connection_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_database_connection_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.database_connection_log SELECT OLD.db_id, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.database_connection_log SELECT OLD.db_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.database_connection_log SELECT NEW.db_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_database_connection_log() OWNER TO recharge;

--
-- Name: process_dataflow_config_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_dataflow_config_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.dataflow_config_log SELECT OLD.df_id, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.dataflow_config_log SELECT OLD.df_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.dataflow_config_log SELECT NEW.df_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_dataflow_config_log() OWNER TO recharge;

--
-- Name: process_generate_wait_for(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_generate_wait_for() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    DECLARE
        my_dag_id int;
        my_subdag_id int;
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            my_dag_id := OLD.dag_id;
            my_subdag_id := OLD.subdag_id;
        ELSIF (TG_OP = 'UPDATE') or (TG_OP = 'INSERT') THEN
            my_dag_id := NEW.dag_id;
            my_subdag_id := NEW.subdag_id;
        END IF;
        UPDATE public.sub_dag set wait_for =
            (
                select cast(replace(array_to_json(array_agg(row_to_json(z)))::text, '"subdag":"OK"', '"task_id":"OK"') as jsonb)
                from (
                     select md.dag_name as dag_id, 'subdag_' || id || '_' || source_table_name as subdag
                     from slave_to_bq b inner join main_dag md on b.dag_id = md.dag_id
                     where target_table_name in (select replace(a.t, 'voyager_staging.', '')
                          from (
                               select array_to_string(
                                              regexp_matches(query, 'voyager_staging.[A-Za-z0-9\-_]+', 'g'),
                                              '') as t
                               from bq_to_bq
                               where subdag_id = my_subdag_id and bq_to_bq.enabled is true
                               UNION
                               select array_to_string(
                                              regexp_matches(sql_query, 'voyager_staging.[A-Za-z0-9\-_]+', 'g'),
                                              '') as t
                               from bq_to_bt
                               where subdag_id = my_subdag_id and bq_to_bt.enabled is true
                               UNION
                               select array_to_string(
                                              regexp_matches(query, 'voyager_staging.[A-Za-z0-9\-_]+', 'g'),
                                              '') as t
                               from bq_to_gs
                               where subdag_id = my_subdag_id and bq_to_gs.enabled is true
                           ) a) and b.enabled is true
                     UNION
                     select md.dag_name as dag_id, subdag_name as subdag
                     from sub_dag b inner join main_dag md on b.dag_id = md.dag_id
                     where subdag_name in (select replace (a.t, 'voyager_dwh.', '') || '_subdag'
                        from (
                            select array_to_string(regexp_matches(query, 'voyager_dwh.[A-Za-z0-9\-_]+', 'g'), '') as t
                            from bq_to_bq where subdag_id = my_subdag_id and bq_to_bq.enabled is true
                            UNION
                            select array_to_string(regexp_matches(sql_query, 'voyager_dwh.[A-Za-z0-9\-_]+', 'g'), '') as t
                            from bq_to_bt where subdag_id = my_subdag_id and bq_to_bt.enabled is true
                            UNION
                            select array_to_string(regexp_matches(query, 'voyager_dwh.[A-Za-z0-9\-_]+', 'g'), '') as t
                            from bq_to_gs where subdag_id = my_subdag_id and bq_to_gs.enabled is true
                            ) a
                        ) and b.dag_id != my_dag_id
                     UNION
                     select md.dag_name as dag_id, subdag_name as subdag
                     from sub_dag b inner join main_dag md on b.dag_id = md.dag_id
                     where subdag_name in (select replace (a.t, 'zoom.', '') || '_subdag'
                        from (
                            select array_to_string(regexp_matches(query, 'zoom.[A-Za-z0-9\-_]+', 'g'), '') as t
                            from bq_to_bq where subdag_id = my_subdag_id and bq_to_bq.enabled is true
                            UNION
                            select array_to_string(regexp_matches(sql_query, 'zoom.[A-Za-z0-9\-_]+', 'g'), '') as t
                            from bq_to_bt where subdag_id = my_subdag_id and bq_to_bt.enabled is true
                            UNION
                            select array_to_string(regexp_matches(query, 'zoom.[A-Za-z0-9\-_]+', 'g'), '') as t
                            from bq_to_gs where subdag_id = my_subdag_id and bq_to_gs.enabled is true
                            ) a
                        ) and b.dag_id != my_dag_id
                     UNION
                     select ga.dag_name as dag_id, replace(ga.t, '.ga_sessions_', 'OK') as subdag
                     from (
                        select 'dwh_ga_checker'::text as dag_name,  array_to_string(regexp_matches(query, '.ga_sessions_', 'g'), '') as t
                        from bq_to_bq where subdag_id = my_subdag_id and bq_to_bq.enabled is true
                        UNION
                        select 'dwh_ga_checker'::text as dag_name,  array_to_string(regexp_matches(query, '.ga_sessions_', 'g'), '') as t
                        from bq_to_gs where subdag_id = my_subdag_id and bq_to_gs.enabled is true
                        UNION
                        select 'dwh_ga_checker'::text as dag_name,  array_to_string(regexp_matches(sql_query, '.ga_sessions_', 'g'), '') as t
                        from bq_to_bt where subdag_id = my_subdag_id and bq_to_bt.enabled is true limit 1
                        ) ga
                ) z
            )
        WHERE subdag_id = my_subdag_id;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_generate_wait_for() OWNER TO recharge;

--
-- Name: process_gs_to_bq_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_gs_to_bq_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.gs_to_bq_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.gs_to_bq_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, NEW.dag_id, NEW.subdag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.gs_to_bq_log SELECT NEW.id, null, null, NEW.dag_id, NEW.subdag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_gs_to_bq_log() OWNER TO recharge;

--
-- Name: process_main_dag_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_main_dag_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.main_dag_log SELECT OLD.dag_id, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.main_dag_log SELECT NEW.dag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.main_dag_log SELECT NEW.dag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_main_dag_log() OWNER TO recharge;

--
-- Name: process_sbq_checker_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_sbq_checker_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.sbq_checker_log SELECT OLD.sbq_id, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.sbq_checker_log SELECT OLD.sbq_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.sbq_checker_log SELECT NEW.sbq_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_sbq_checker_log() OWNER TO recharge;

--
-- Name: process_slave_to_bq_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_slave_to_bq_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.slave_to_bq_log SELECT OLD.id, OLD.dag_id, OLD.db_id, OLD.df_id, null, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.slave_to_bq_log SELECT OLD.id, OLD.dag_id, OLD.db_id, OLD.df_id, NEW.dag_id, NEW.db_id, NEW.df_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.slave_to_bq_log SELECT NEW.id, null, null, null, NEW.dag_id, NEW.db_id, NEW.df_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_slave_to_bq_log() OWNER TO recharge;

--
-- Name: process_spark_config_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_spark_config_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.spark_config_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, null, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.spark_config_log SELECT OLD.id, OLD.dag_id, OLD.subdag_id, NEW.dag_id, NEW.subdag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.spark_config_log SELECT NEW.id, null, null, NEW.dag_id, NEW.subdag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_spark_config_log() OWNER TO recharge;

--
-- Name: process_sub_dag_log(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.process_sub_dag_log() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO log_meta_data.sub_dag_log SELECT OLD.subdag_id, OLD.dag_id, null, to_jsonb(OLD.*), Null, 'DELETE', user, now();
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO log_meta_data.sub_dag_log SELECT OLD.subdag_id, OLD.dag_id, NEW.dag_id, to_jsonb(OLD.*), to_jsonb(NEW.*), 'UPDATE', user, now();
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO log_meta_data.sub_dag_log SELECT NEW.subdag_id, null, NEW.dag_id, Null, to_jsonb(NEW.*), 'INSERT', user, now();
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.process_sub_dag_log() OWNER TO recharge;

--
-- Name: update_modified_column(); Type: FUNCTION; Schema: public; Owner: recharge
--

CREATE FUNCTION public.update_modified_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_time = now();
    NEW.updated_by = "current_user"();
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_modified_column() OWNER TO recharge;

SET default_tablespace = '';

--
-- Name: bq_checker_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.bq_checker_log (
    bq_checker_id integer NOT NULL,
    old_dag_id integer,
    old_subdag_id integer,
    new_dag_id integer,
    new_subdag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.bq_checker_log OWNER TO recharge;

--
-- Name: bq_to_bq_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.bq_to_bq_log (
    bq_to_bq_id integer NOT NULL,
    old_dag_id integer,
    old_subdag_id integer,
    new_dag_id integer,
    new_subdag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.bq_to_bq_log OWNER TO recharge;

--
-- Name: bq_to_bt_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.bq_to_bt_log (
    bq_to_bt_id integer NOT NULL,
    old_dag_id integer,
    old_subdag_id integer,
    new_dag_id integer,
    new_subdag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.bq_to_bt_log OWNER TO recharge;

--
-- Name: bq_to_gs_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.bq_to_gs_log (
    bq_to_gs_id integer NOT NULL,
    old_dag_id integer,
    old_subdag_id integer,
    new_dag_id integer,
    new_subdag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.bq_to_gs_log OWNER TO recharge;

--
-- Name: bq_to_pubsub_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.bq_to_pubsub_log (
    bq_to_pubsub_id integer NOT NULL,
    old_dag_id integer,
    old_subdag_id integer,
    new_dag_id integer,
    new_subdag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.bq_to_pubsub_log OWNER TO recharge;

--
-- Name: database_connection_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.database_connection_log (
    db_id integer NOT NULL,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.database_connection_log OWNER TO recharge;

--
-- Name: dataflow_config_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.dataflow_config_log (
    df_id integer NOT NULL,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.dataflow_config_log OWNER TO recharge;

--
-- Name: gs_to_bq_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.gs_to_bq_log (
    gs_to_bq_id integer NOT NULL,
    old_dag_id integer,
    old_subdag_id integer,
    new_dag_id integer,
    new_subdag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.gs_to_bq_log OWNER TO recharge;

--
-- Name: main_dag_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.main_dag_log (
    dag_id integer NOT NULL,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.main_dag_log OWNER TO recharge;

--
-- Name: sbq_checker_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.sbq_checker_log (
    sbq_id integer NOT NULL,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.sbq_checker_log OWNER TO recharge;

--
-- Name: slave_to_bq_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.slave_to_bq_log (
    slave_to_bq_id integer NOT NULL,
    old_dag_id integer,
    old_db_id integer,
    old_df_id integer,
    new_dag_id integer,
    new_db_id integer,
    new_df_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.slave_to_bq_log OWNER TO recharge;

--
-- Name: spark_config_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.spark_config_log (
    spark_config_id integer NOT NULL,
    old_dag_id integer,
    old_subdag_id integer,
    new_dag_id integer,
    new_subdag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.spark_config_log OWNER TO recharge;

--
-- Name: sub_dag_log; Type: TABLE; Schema: log_meta_data; Owner: recharge
--

CREATE TABLE log_meta_data.sub_dag_log (
    subdag_id integer NOT NULL,
    old_dag_id integer,
    new_dag_id integer,
    old_data jsonb,
    new_data jsonb,
    action_type character varying(6) NOT NULL,
    action_by character varying(20) NOT NULL,
    log_time timestamp without time zone NOT NULL
);


ALTER TABLE log_meta_data.sub_dag_log OWNER TO recharge;

--
-- Name: bq_checker; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.bq_checker (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    subdag_id integer,
    task_name character varying(200) NOT NULL,
    column_checker character varying(50),
    minimum_time character varying(20),
    target_table text NOT NULL,
    dependency character varying(2000),
    wait_for jsonb,
    enabled boolean DEFAULT false NOT NULL,
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone,
    updated_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone,
    created_by character varying(50),
    updated_by character varying(50)
);


ALTER TABLE public.bq_checker OWNER TO recharge;

--
-- Name: bq_checker_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.bq_checker_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bq_checker_id_seq OWNER TO recharge;

--
-- Name: bq_checker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.bq_checker_id_seq OWNED BY public.bq_checker.id;


--
-- Name: bq_to_bq; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.bq_to_bq (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    task_name character varying(200) NOT NULL,
    query text NOT NULL,
    target_table text NOT NULL,
    disposition public.disposition DEFAULT 'WRITE_APPEND'::public.disposition,
    dependency character varying(2000),
    enabled boolean DEFAULT false NOT NULL,
    subdag_id integer,
    wait_for jsonb,
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time date DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL
);


ALTER TABLE public.bq_to_bq OWNER TO recharge;

--
-- Name: bq_to_bq_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.bq_to_bq_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bq_to_bq_id_seq OWNER TO recharge;

--
-- Name: bq_to_bq_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.bq_to_bq_id_seq OWNED BY public.bq_to_bq.id;


--
-- Name: bq_to_bt; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.bq_to_bt (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    subdag_id integer,
    task_name character varying(200) NOT NULL,
    df_id integer NOT NULL,
    bt_instance_id character varying(100),
    bigtable_id character varying(100) NOT NULL,
    sql_query text NOT NULL,
    row_keys_builder jsonb DEFAULT '{"row_key": ["field_1", "field_2"], "separator": ":"}'::jsonb NOT NULL,
    cf_mapping jsonb DEFAULT '{"cf_name": ["field_1", "field_2"], "cf_name_1": ["field_x", "field_y"]}'::jsonb,
    dependency character varying(500),
    wait_for jsonb,
    max_numb_worker integer DEFAULT 2,
    enabled boolean DEFAULT false NOT NULL,
    created_time timestamp without time zone DEFAULT now(),
    updated_time timestamp without time zone DEFAULT now(),
    created_by character varying(50) DEFAULT 'airflow'::character varying,
    updated_by character varying(50) DEFAULT 'airflow'::character varying,
    class_name character varying DEFAULT 'MainBQToBT'::character varying,
    protobuf_file text,
    protobuf_mapping jsonb DEFAULT '[{"cf": "0", "message": "MyMesage", "qualifier": "data0"}, {"cf": "1", "message": "OtherMessage", "qualifier": "data1"}]'::jsonb,
    bt_project_id character varying(50),
    interactive_query boolean DEFAULT false
);


ALTER TABLE public.bq_to_bt OWNER TO recharge;

--
-- Name: bq_to_bt_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.bq_to_bt_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bq_to_bt_id_seq OWNER TO recharge;

--
-- Name: bq_to_bt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.bq_to_bt_id_seq OWNED BY public.bq_to_bt.id;


--
-- Name: bq_to_gs; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.bq_to_gs (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    task_name character varying(200) NOT NULL,
    source_table text,
    target_uri text NOT NULL,
    target_format public.target_format DEFAULT 'CSV'::public.target_format,
    dependency character varying(2000),
    enabled boolean DEFAULT false NOT NULL,
    subdag_id integer,
    wait_for jsonb,
    created_time date DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time date DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    query text,
    bq_disposition character varying(50)
);


ALTER TABLE public.bq_to_gs OWNER TO recharge;

--
-- Name: bq_to_gs_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.bq_to_gs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bq_to_gs_id_seq OWNER TO recharge;

--
-- Name: bq_to_gs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.bq_to_gs_id_seq OWNED BY public.bq_to_gs.id;


--
-- Name: bq_to_pubsub; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.bq_to_pubsub (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    subdag_id integer,
    task_name character varying(200) NOT NULL,
    df_id integer NOT NULL,
    sql_query text NOT NULL,
    dependency character varying(500) DEFAULT NULL::character varying,
    wait_for jsonb,
    max_numb_worker integer DEFAULT 1 NOT NULL,
    target_topics text NOT NULL,
    enabled boolean DEFAULT true NOT NULL,
    created_time timestamp without time zone DEFAULT now() NOT NULL,
    updated_time timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) DEFAULT 'airflow'::character varying NOT NULL,
    updated_by character varying(50) DEFAULT 'airflow'::character varying,
    interactive_query boolean DEFAULT false NOT NULL
);


ALTER TABLE public.bq_to_pubsub OWNER TO recharge;

--
-- Name: bq_to_pubsub_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.bq_to_pubsub_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bq_to_pubsub_id_seq OWNER TO recharge;

--
-- Name: bq_to_pubsub_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.bq_to_pubsub_id_seq OWNED BY public.bq_to_pubsub.id;


--
-- Name: slave_to_bq; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.slave_to_bq (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    df_id integer NOT NULL,
    db_id integer NOT NULL,
    source_table_name character varying,
    source_sql_query character varying NOT NULL,
    source_count_query character varying,
    source_table_schema jsonb,
    target_project_id character varying DEFAULT 'tokopedia-970'::character varying NOT NULL,
    target_dataset character varying DEFAULT 'voyager_staging'::character varying NOT NULL,
    target_table_name character varying NOT NULL,
    target_write_disposition character varying DEFAULT 'WRITE_APPEND'::character varying NOT NULL,
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    sla_in_minutes integer,
    enabled boolean DEFAULT false,
    priority_weight integer
);


ALTER TABLE public.slave_to_bq OWNER TO recharge;

--
-- Name: dag_slave_active; Type: VIEW; Schema: public; Owner: recharge
--

CREATE VIEW public.dag_slave_active AS
 SELECT DISTINCT slave_to_bq.dag_id
   FROM public.slave_to_bq
  WHERE (slave_to_bq.enabled IS TRUE);


ALTER TABLE public.dag_slave_active OWNER TO recharge;

--
-- Name: database_connection; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.database_connection (
    db_id integer NOT NULL,
    db_name character varying,
    db_type character varying DEFAULT 'postgresql'::character varying,
    db_username character varying DEFAULT 'bqetl'::character varying,
    db_password character varying DEFAULT 'DaIU2HpfFcJj5d'::character varying,
    db_host character varying,
    db_port character varying DEFAULT '5432'::character varying,
    db_param_str character varying,
    created_time date DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time date DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL
);


ALTER TABLE public.database_connection OWNER TO recharge;

--
-- Name: database_connection_db_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.database_connection_db_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.database_connection_db_id_seq OWNER TO recharge;

--
-- Name: database_connection_db_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.database_connection_db_id_seq OWNED BY public.database_connection.db_id;


--
-- Name: database_connection_log; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.database_connection_log (
    db_id integer NOT NULL,
    db_name character varying,
    db_type character varying DEFAULT 'postgresql'::character varying,
    db_username character varying DEFAULT 'bqetl'::character varying,
    db_password character varying DEFAULT 'DaIU2HpfFcJj5d'::character varying,
    db_host character varying,
    db_port character varying DEFAULT '5432'::character varying,
    db_param_str character varying,
    created_time date DEFAULT ('now'::text)::date NOT NULL,
    updated_time date DEFAULT ('now'::text)::date NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    action character varying NOT NULL,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.database_connection_log OWNER TO recharge;

--
-- Name: dataflow_config; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.dataflow_config (
    df_id integer NOT NULL,
    df_project_id character varying DEFAULT 'tokopedia-970'::character varying,
    df_runner character varying DEFAULT 'DataflowRunner'::character varying,
    df_temp_location character varying DEFAULT 'gs://voyager-staging/temp'::character varying,
    df_staging_location character varying DEFAULT 'gs://voyager-staging/staging'::character varying,
    df_network character varying DEFAULT 'tkpd-networks'::character varying,
    df_region character varying DEFAULT 'us-east1'::character varying,
    df_zone character varying DEFAULT 'asia-southeast1-a'::character varying,
    df_sub_network character varying DEFAULT 'regions/asia-southeast1/subnetworks/app-sea-a'::character varying,
    df_worker_machine_type character varying DEFAULT 'n1-standard-4'::character varying,
    df_worker_disk_type character varying DEFAULT 'compute.googleapis.com/projects//zones//diskTypes/pd-ssd'::character varying,
    df_disk_size_gb integer DEFAULT 30,
    df_description character varying,
    created_time date DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time date DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    df_service_account character varying(150)
);


ALTER TABLE public.dataflow_config OWNER TO recharge;

--
-- Name: dataflow_config_df_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.dataflow_config_df_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dataflow_config_df_id_seq OWNER TO recharge;

--
-- Name: dataflow_config_df_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.dataflow_config_df_id_seq OWNED BY public.dataflow_config.df_id;


--
-- Name: gs_to_bq; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.gs_to_bq (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    task_name character varying,
    source_uri character varying NOT NULL,
    source_format character varying DEFAULT 'CSV'::character varying NOT NULL,
    target_table character varying NOT NULL,
    dependency character varying,
    enabled boolean DEFAULT false,
    subdag_id integer,
    wait_for jsonb,
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone,
    updated_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone,
    created_by character varying,
    updated_by character varying,
    write_disposition character varying DEFAULT 'WRITE_APPEND'::character varying NOT NULL,
    skip_leading_rows integer DEFAULT 1,
    field_delimiter character varying DEFAULT ','::character varying,
    partition_column character varying
);


ALTER TABLE public.gs_to_bq OWNER TO recharge;

--
-- Name: gs_to_bq_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.gs_to_bq_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gs_to_bq_id_seq OWNER TO recharge;

--
-- Name: gs_to_bq_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.gs_to_bq_id_seq OWNED BY public.gs_to_bq.id;


--
-- Name: http_request; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.http_request (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    subdag_id integer,
    task_name character varying(200),
    command_template text DEFAULT 'curl --request {method} --url {endpoint} --header "content-type: application/json" --data ''{data}'''::text NOT NULL,
    method character varying DEFAULT 'GET'::character varying,
    endpoint character varying,
    data jsonb,
    timeout_seconds integer,
    fire_and_forget boolean DEFAULT false NOT NULL,
    dependency character varying(500) DEFAULT NULL::character varying,
    enabled boolean DEFAULT false,
    wait_for jsonb,
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone,
    updated_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone,
    created_by character varying DEFAULT "current_user"(),
    updated_by character varying DEFAULT "current_user"()
);


ALTER TABLE public.http_request OWNER TO recharge;

--
-- Name: http_request_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.http_request_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.http_request_id_seq OWNER TO recharge;

--
-- Name: http_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.http_request_id_seq OWNED BY public.http_request.id;


--
-- Name: main_dag; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.main_dag (
    dag_id integer NOT NULL,
    dag_name character varying(50) NOT NULL,
    owner character varying(50) NOT NULL,
    schedule_interval character varying(30) DEFAULT 'None'::character varying,
    start_date character varying(30) DEFAULT '2019-09-01'::character varying,
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    description character varying(100),
    enabled boolean
);


ALTER TABLE public.main_dag OWNER TO recharge;

--
-- Name: main_dag_dag_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.main_dag_dag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_dag_dag_id_seq OWNER TO recharge;

--
-- Name: main_dag_dag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.main_dag_dag_id_seq OWNED BY public.main_dag.dag_id;


--
-- Name: sbq_checker; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.sbq_checker (
    id integer NOT NULL,
    sbq_id integer NOT NULL,
    number_iteration integer DEFAULT 10,
    column_partition character varying(50) DEFAULT 'processed_dttm'::character varying,
    column_checker character varying(50),
    minimum_time character varying(20),
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL
);


ALTER TABLE public.sbq_checker OWNER TO recharge;

--
-- Name: sbq_checker_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.sbq_checker_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sbq_checker_id_seq OWNER TO recharge;

--
-- Name: sbq_checker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.sbq_checker_id_seq OWNED BY public.sbq_checker.id;


--
-- Name: slave_to_bq_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.slave_to_bq_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.slave_to_bq_id_seq OWNER TO recharge;

--
-- Name: slave_to_bq_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.slave_to_bq_id_seq OWNED BY public.slave_to_bq.id;


--
-- Name: slave_to_bq_log; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.slave_to_bq_log (
    id integer NOT NULL,
    dag_id integer NOT NULL,
    df_id integer NOT NULL,
    db_id integer NOT NULL,
    source_table_name character varying,
    source_sql_query character varying NOT NULL,
    source_count_query character varying,
    source_table_schema jsonb,
    target_project_id character varying DEFAULT 'tokopedia-970'::character varying NOT NULL,
    target_dataset character varying DEFAULT 'voyager_staging'::character varying NOT NULL,
    target_table_name character varying NOT NULL,
    target_write_disposition character varying DEFAULT 'WRITE_APPEND'::character varying NOT NULL,
    created_time timestamp without time zone DEFAULT now() NOT NULL,
    updated_time timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    sla_in_minutes integer,
    enabled boolean DEFAULT false,
    action character varying,
    "timestamp" timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.slave_to_bq_log OWNER TO recharge;

--
-- Name: slave_to_bq_log_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.slave_to_bq_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.slave_to_bq_log_id_seq OWNER TO recharge;

--
-- Name: slave_to_bq_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.slave_to_bq_log_id_seq OWNED BY public.slave_to_bq_log.id;


--
-- Name: spark_config; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.spark_config (
    id integer NOT NULL,
    task_name character varying(200) NOT NULL,
    dag_id integer NOT NULL,
    subdag_id integer,
    submit_type public.spark_submit_type NOT NULL,
    description text,
    file character varying NOT NULL,
    proxy_user character varying,
    class_name character varying,
    args text[],
    jars text[],
    py_files text[],
    files text[],
    driver_memory character varying,
    driver_cores integer,
    executor_memory character varying,
    executor_cores integer,
    num_executors integer,
    archives text[],
    queue character varying,
    session_name character varying,
    conf jsonb,
    enabled boolean DEFAULT false NOT NULL,
    dependency character varying(200),
    wait_for jsonb,
    created_time timestamp without time zone DEFAULT now() NOT NULL,
    updated_time timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    livy_host character varying,
    file_dir character varying,
    requirement_txt character varying,
    python_version integer DEFAULT 3,
    machine_type_id integer,
    final_machine_state public.final_machine_state DEFAULT 'shutdown'::public.final_machine_state
);


ALTER TABLE public.spark_config OWNER TO recharge;

--
-- Name: spark_config_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.spark_config_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.spark_config_id_seq OWNER TO recharge;

--
-- Name: spark_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.spark_config_id_seq OWNED BY public.spark_config.id;


--
-- Name: sub_dag; Type: TABLE; Schema: public; Owner: recharge
--

CREATE TABLE public.sub_dag (
    subdag_id integer NOT NULL,
    dag_id integer NOT NULL,
    subdag_name character varying(50),
    dependency character varying(50),
    wait_for jsonb,
    description character varying(100),
    created_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    updated_time timestamp without time zone DEFAULT ('now'::text)::timestamp without time zone NOT NULL,
    created_by character varying(50) NOT NULL,
    updated_by character varying(50) NOT NULL,
    sla_in_minutes integer,
    priority_weight integer,
    wait_for_fixed_time jsonb,
    slack_webhook character varying(500),
    queue_name character varying(30),
    sa_conn_id character varying(150),
    success_slack_webhook character varying(500)
);


ALTER TABLE public.sub_dag OWNER TO recharge;

--
-- Name: sub_dag_subdag_id_seq; Type: SEQUENCE; Schema: public; Owner: recharge
--

CREATE SEQUENCE public.sub_dag_subdag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sub_dag_subdag_id_seq OWNER TO recharge;

--
-- Name: sub_dag_subdag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: recharge
--

ALTER SEQUENCE public.sub_dag_subdag_id_seq OWNED BY public.sub_dag.subdag_id;


--
-- Name: worker_slot_log; Type: TABLE; Schema: worker_slot; Owner: recharge
--

CREATE TABLE worker_slot.worker_slot_log (
    time_key timestamp without time zone NOT NULL,
    active_worker integer
);


ALTER TABLE worker_slot.worker_slot_log OWNER TO recharge;

--
-- Name: bq_checker id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_checker ALTER COLUMN id SET DEFAULT nextval('public.bq_checker_id_seq'::regclass);


--
-- Name: bq_to_bq id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bq ALTER COLUMN id SET DEFAULT nextval('public.bq_to_bq_id_seq'::regclass);


--
-- Name: bq_to_bt id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bt ALTER COLUMN id SET DEFAULT nextval('public.bq_to_bt_id_seq'::regclass);


--
-- Name: bq_to_gs id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_gs ALTER COLUMN id SET DEFAULT nextval('public.bq_to_gs_id_seq'::regclass);


--
-- Name: bq_to_pubsub id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_pubsub ALTER COLUMN id SET DEFAULT nextval('public.bq_to_pubsub_id_seq'::regclass);


--
-- Name: database_connection db_id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.database_connection ALTER COLUMN db_id SET DEFAULT nextval('public.database_connection_db_id_seq'::regclass);


--
-- Name: dataflow_config df_id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.dataflow_config ALTER COLUMN df_id SET DEFAULT nextval('public.dataflow_config_df_id_seq'::regclass);


--
-- Name: gs_to_bq id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.gs_to_bq ALTER COLUMN id SET DEFAULT nextval('public.gs_to_bq_id_seq'::regclass);


--
-- Name: http_request id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.http_request ALTER COLUMN id SET DEFAULT nextval('public.http_request_id_seq'::regclass);


--
-- Name: main_dag dag_id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.main_dag ALTER COLUMN dag_id SET DEFAULT nextval('public.main_dag_dag_id_seq'::regclass);


--
-- Name: sbq_checker id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.sbq_checker ALTER COLUMN id SET DEFAULT nextval('public.sbq_checker_id_seq'::regclass);


--
-- Name: slave_to_bq id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.slave_to_bq ALTER COLUMN id SET DEFAULT nextval('public.slave_to_bq_id_seq'::regclass);


--
-- Name: slave_to_bq_log id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.slave_to_bq_log ALTER COLUMN id SET DEFAULT nextval('public.slave_to_bq_log_id_seq'::regclass);


--
-- Name: spark_config id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.spark_config ALTER COLUMN id SET DEFAULT nextval('public.spark_config_id_seq'::regclass);


--
-- Name: sub_dag subdag_id; Type: DEFAULT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.sub_dag ALTER COLUMN subdag_id SET DEFAULT nextval('public.sub_dag_subdag_id_seq'::regclass);


--
-- Name: bq_checker bq_checker_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_checker
    ADD CONSTRAINT bq_checker_pk PRIMARY KEY (id);


--
-- Name: bq_to_bq bq_to_bq_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bq
    ADD CONSTRAINT bq_to_bq_pk PRIMARY KEY (id);


--
-- Name: bq_to_bt bq_to_bt_pkey; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bt
    ADD CONSTRAINT bq_to_bt_pkey PRIMARY KEY (id);


--
-- Name: bq_to_gs bq_to_gs_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_gs
    ADD CONSTRAINT bq_to_gs_pk PRIMARY KEY (id);


--
-- Name: bq_to_pubsub bq_to_pubsub_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_pubsub
    ADD CONSTRAINT bq_to_pubsub_pk PRIMARY KEY (id);


--
-- Name: dataflow_config dataflow_config_pkey; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.dataflow_config
    ADD CONSTRAINT dataflow_config_pkey PRIMARY KEY (df_id);


--
-- Name: database_connection etl_source_conn_pkey; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.database_connection
    ADD CONSTRAINT etl_source_conn_pkey PRIMARY KEY (db_id);


--
-- Name: gs_to_bq gs_to_bq_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.gs_to_bq
    ADD CONSTRAINT gs_to_bq_pk PRIMARY KEY (id);


--
-- Name: http_request http_request_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.http_request
    ADD CONSTRAINT http_request_pk PRIMARY KEY (id);


--
-- Name: main_dag main_dag_dag_id_key; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.main_dag
    ADD CONSTRAINT main_dag_dag_id_key UNIQUE (dag_name);


--
-- Name: main_dag main_dag_pkey; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.main_dag
    ADD CONSTRAINT main_dag_pkey PRIMARY KEY (dag_id);


--
-- Name: sbq_checker sbq_checker_pkey; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.sbq_checker
    ADD CONSTRAINT sbq_checker_pkey PRIMARY KEY (id);


--
-- Name: slave_to_bq slave_to_bq_pkey; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.slave_to_bq
    ADD CONSTRAINT slave_to_bq_pkey PRIMARY KEY (id);


--
-- Name: spark_config spark_config_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.spark_config
    ADD CONSTRAINT spark_config_pk PRIMARY KEY (id);


--
-- Name: sub_dag sub_dag_pk; Type: CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.sub_dag
    ADD CONSTRAINT sub_dag_pk PRIMARY KEY (subdag_id);


--
-- Name: worker_slot_log worker_slot_log_pk; Type: CONSTRAINT; Schema: worker_slot; Owner: recharge
--

ALTER TABLE ONLY worker_slot.worker_slot_log
    ADD CONSTRAINT worker_slot_log_pk PRIMARY KEY (time_key);


--
-- Name: bq_checker_log_new_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_checker_log_new_dag_id_index ON log_meta_data.bq_checker_log USING btree (new_dag_id);


--
-- Name: bq_checker_log_new_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_checker_log_new_subdag_id_index ON log_meta_data.bq_checker_log USING btree (new_subdag_id);


--
-- Name: bq_checker_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_checker_log_old_dag_id_index ON log_meta_data.bq_checker_log USING btree (old_dag_id);


--
-- Name: bq_checker_log_old_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_checker_log_old_subdag_id_index ON log_meta_data.bq_checker_log USING btree (old_subdag_id);


--
-- Name: bq_to_bq_log_new_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bq_log_new_dag_id_index ON log_meta_data.bq_to_bq_log USING btree (new_dag_id);


--
-- Name: bq_to_bq_log_new_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bq_log_new_subdag_id_index ON log_meta_data.bq_to_bq_log USING btree (new_subdag_id);


--
-- Name: bq_to_bq_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bq_log_old_dag_id_index ON log_meta_data.bq_to_bq_log USING btree (old_dag_id);


--
-- Name: bq_to_bq_log_old_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bq_log_old_subdag_id_index ON log_meta_data.bq_to_bq_log USING btree (old_subdag_id);


--
-- Name: bq_to_bt_log_new_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bt_log_new_dag_id_index ON log_meta_data.bq_to_bt_log USING btree (new_dag_id);


--
-- Name: bq_to_bt_log_new_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bt_log_new_subdag_id_index ON log_meta_data.bq_to_bt_log USING btree (new_subdag_id);


--
-- Name: bq_to_bt_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bt_log_old_dag_id_index ON log_meta_data.bq_to_bt_log USING btree (old_dag_id);


--
-- Name: bq_to_bt_log_old_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_bt_log_old_subdag_id_index ON log_meta_data.bq_to_bt_log USING btree (old_subdag_id);


--
-- Name: bq_to_gs_log_new_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_gs_log_new_dag_id_index ON log_meta_data.bq_to_gs_log USING btree (new_dag_id);


--
-- Name: bq_to_gs_log_new_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_gs_log_new_subdag_id_index ON log_meta_data.bq_to_gs_log USING btree (new_subdag_id);


--
-- Name: bq_to_gs_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_gs_log_old_dag_id_index ON log_meta_data.bq_to_gs_log USING btree (old_dag_id);


--
-- Name: bq_to_gs_log_old_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_gs_log_old_subdag_id_index ON log_meta_data.bq_to_gs_log USING btree (old_subdag_id);


--
-- Name: bq_to_pubsub_log_new_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_pubsub_log_new_dag_id_index ON log_meta_data.bq_to_pubsub_log USING btree (new_dag_id);


--
-- Name: bq_to_pubsub_log_new_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_pubsub_log_new_subdag_id_index ON log_meta_data.bq_to_pubsub_log USING btree (new_subdag_id);


--
-- Name: bq_to_pubsub_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_pubsub_log_old_dag_id_index ON log_meta_data.bq_to_pubsub_log USING btree (old_dag_id);


--
-- Name: bq_to_pubsub_log_old_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX bq_to_pubsub_log_old_subdag_id_index ON log_meta_data.bq_to_pubsub_log USING btree (old_subdag_id);


--
-- Name: database_connection_log_db_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX database_connection_log_db_id_index ON log_meta_data.database_connection_log USING btree (db_id);


--
-- Name: dataflow_config_log_df_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX dataflow_config_log_df_id_index ON log_meta_data.dataflow_config_log USING btree (df_id);


--
-- Name: main_dag_log_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX main_dag_log_dag_id_index ON log_meta_data.main_dag_log USING btree (dag_id);


--
-- Name: sbq_checker_log_df_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX sbq_checker_log_df_id_index ON log_meta_data.sbq_checker_log USING btree (sbq_id);


--
-- Name: slave_to_bq_log_neq_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX slave_to_bq_log_neq_dag_id_index ON log_meta_data.slave_to_bq_log USING btree (new_dag_id);


--
-- Name: slave_to_bq_log_new_db_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX slave_to_bq_log_new_db_id_index ON log_meta_data.slave_to_bq_log USING btree (new_db_id);


--
-- Name: slave_to_bq_log_new_df_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX slave_to_bq_log_new_df_id_index ON log_meta_data.slave_to_bq_log USING btree (new_df_id);


--
-- Name: slave_to_bq_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX slave_to_bq_log_old_dag_id_index ON log_meta_data.slave_to_bq_log USING btree (old_dag_id);


--
-- Name: slave_to_bq_log_old_db_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX slave_to_bq_log_old_db_id_index ON log_meta_data.slave_to_bq_log USING btree (old_db_id);


--
-- Name: slave_to_bq_log_old_df_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX slave_to_bq_log_old_df_id_index ON log_meta_data.slave_to_bq_log USING btree (old_df_id);


--
-- Name: slave_to_bq_log_slave_to_bq_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX slave_to_bq_log_slave_to_bq_id_index ON log_meta_data.slave_to_bq_log USING btree (slave_to_bq_id);


--
-- Name: spark_config_log_new_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX spark_config_log_new_dag_id_index ON log_meta_data.spark_config_log USING btree (new_dag_id);


--
-- Name: spark_config_log_new_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX spark_config_log_new_subdag_id_index ON log_meta_data.spark_config_log USING btree (new_subdag_id);


--
-- Name: spark_config_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX spark_config_log_old_dag_id_index ON log_meta_data.spark_config_log USING btree (old_dag_id);


--
-- Name: spark_config_log_old_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX spark_config_log_old_subdag_id_index ON log_meta_data.spark_config_log USING btree (old_subdag_id);


--
-- Name: sub_dag_log_old_dag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX sub_dag_log_old_dag_id_index ON log_meta_data.sub_dag_log USING btree (old_dag_id);


--
-- Name: sub_dag_log_old_new_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX sub_dag_log_old_new_id_index ON log_meta_data.sub_dag_log USING btree (new_dag_id);


--
-- Name: sub_dag_log_subdag_id_index; Type: INDEX; Schema: log_meta_data; Owner: recharge
--

CREATE INDEX sub_dag_log_subdag_id_index ON log_meta_data.sub_dag_log USING btree (subdag_id);


--
-- Name: bq_checker_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_checker_dag_id_index ON public.bq_checker USING btree (dag_id);


--
-- Name: bq_checker_subdag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_checker_subdag_id_index ON public.bq_checker USING btree (subdag_id);


--
-- Name: bq_to_bq_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_bq_dag_id_index ON public.bq_to_bq USING btree (dag_id);


--
-- Name: bq_to_bq_dag_id_task_name_uindex; Type: INDEX; Schema: public; Owner: recharge
--

CREATE UNIQUE INDEX bq_to_bq_dag_id_task_name_uindex ON public.bq_to_bq USING btree (dag_id, task_name);


--
-- Name: bq_to_bq_subdag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_bq_subdag_id_index ON public.bq_to_bq USING btree (subdag_id);


--
-- Name: bq_to_bq_task_name_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_bq_task_name_index ON public.bq_to_bq USING btree (task_name);


--
-- Name: bq_to_bt_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_bt_dag_id_index ON public.bq_to_bt USING btree (dag_id);


--
-- Name: bq_to_bt_df_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_bt_df_index ON public.bq_to_bt USING btree (df_id);


--
-- Name: bq_to_bt_subdag_idx; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_bt_subdag_idx ON public.bq_to_bt USING btree (subdag_id);


--
-- Name: bq_to_gs_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_gs_dag_id_index ON public.bq_to_gs USING btree (dag_id);


--
-- Name: bq_to_gs_dag_id_task_name_uindex; Type: INDEX; Schema: public; Owner: recharge
--

CREATE UNIQUE INDEX bq_to_gs_dag_id_task_name_uindex ON public.bq_to_gs USING btree (dag_id, task_name);


--
-- Name: bq_to_gs_subdag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_gs_subdag_id_index ON public.bq_to_gs USING btree (subdag_id);


--
-- Name: bq_to_gs_task_name_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_gs_task_name_index ON public.bq_to_gs USING btree (task_name);


--
-- Name: bq_to_pubsub_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_pubsub_dag_id_index ON public.bq_to_pubsub USING btree (dag_id);


--
-- Name: bq_to_pubsub_df_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_pubsub_df_id_index ON public.bq_to_pubsub USING btree (df_id);


--
-- Name: bq_to_pubsub_subdag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX bq_to_pubsub_subdag_id_index ON public.bq_to_pubsub USING btree (subdag_id);


--
-- Name: http_request_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX http_request_dag_id_index ON public.http_request USING btree (dag_id);


--
-- Name: http_request_id_uindex; Type: INDEX; Schema: public; Owner: recharge
--

CREATE UNIQUE INDEX http_request_id_uindex ON public.http_request USING btree (id);


--
-- Name: http_request_subdag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX http_request_subdag_id_index ON public.http_request USING btree (subdag_id);


--
-- Name: slave_to_bq_db_id_source_table_name_uindex; Type: INDEX; Schema: public; Owner: recharge
--

CREATE UNIQUE INDEX slave_to_bq_db_id_source_table_name_uindex ON public.slave_to_bq USING btree (db_id, source_table_name);


--
-- Name: spark_config_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX spark_config_dag_id_index ON public.spark_config USING btree (dag_id);


--
-- Name: spark_config_subdag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX spark_config_subdag_id_index ON public.spark_config USING btree (subdag_id);


--
-- Name: sub_dag_dag_id_index; Type: INDEX; Schema: public; Owner: recharge
--

CREATE INDEX sub_dag_dag_id_index ON public.sub_dag USING btree (dag_id);


--
-- Name: sub_dag_dag_id_subdag_name_uindex; Type: INDEX; Schema: public; Owner: recharge
--

CREATE UNIQUE INDEX sub_dag_dag_id_subdag_name_uindex ON public.sub_dag USING btree (dag_id, subdag_name);


--
-- Name: bq_checker bq_checker_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER bq_checker_log AFTER INSERT OR DELETE OR UPDATE ON public.bq_checker FOR EACH ROW EXECUTE PROCEDURE public.process_bq_checker_log();


--
-- Name: bq_to_bq bq_to_bq_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER bq_to_bq_log AFTER INSERT OR DELETE OR UPDATE ON public.bq_to_bq FOR EACH ROW EXECUTE PROCEDURE public.process_bq_to_bq_log();


--
-- Name: bq_to_bt bq_to_bt_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER bq_to_bt_log AFTER INSERT OR DELETE OR UPDATE ON public.bq_to_bt FOR EACH ROW EXECUTE PROCEDURE public.process_bq_to_bt_log();


--
-- Name: bq_to_gs bq_to_gs_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER bq_to_gs_log AFTER INSERT OR DELETE OR UPDATE ON public.bq_to_gs FOR EACH ROW EXECUTE PROCEDURE public.process_bq_to_gs_log();


--
-- Name: bq_to_pubsub bq_to_pubsub_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER bq_to_pubsub_log AFTER INSERT OR DELETE OR UPDATE ON public.bq_to_pubsub FOR EACH ROW EXECUTE PROCEDURE public.process_bq_to_pubsub_log();


--
-- Name: database_connection database_connection_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER database_connection_log AFTER INSERT OR DELETE OR UPDATE ON public.database_connection FOR EACH ROW EXECUTE PROCEDURE public.process_database_connection_log();


--
-- Name: dataflow_config dataflow_config_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER dataflow_config_log AFTER INSERT OR DELETE OR UPDATE ON public.dataflow_config FOR EACH ROW EXECUTE PROCEDURE public.process_dataflow_config_log();


--
-- Name: bq_to_bq generate_wait_for; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER generate_wait_for AFTER INSERT OR DELETE OR UPDATE ON public.bq_to_bq FOR EACH ROW EXECUTE PROCEDURE public.process_generate_wait_for();


--
-- Name: bq_to_bt generate_wait_for_bq_to_bt; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER generate_wait_for_bq_to_bt AFTER INSERT OR DELETE OR UPDATE ON public.bq_to_bt FOR EACH ROW EXECUTE PROCEDURE public.process_generate_wait_for();


--
-- Name: bq_to_pubsub generate_wait_for_bq_to_pubsub; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER generate_wait_for_bq_to_pubsub AFTER INSERT OR DELETE OR UPDATE ON public.bq_to_pubsub FOR EACH ROW EXECUTE PROCEDURE public.process_generate_wait_for();


--
-- Name: gs_to_bq gs_to_bq_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER gs_to_bq_log AFTER INSERT OR DELETE OR UPDATE ON public.gs_to_bq FOR EACH ROW EXECUTE PROCEDURE public.process_gs_to_bq_log();


--
-- Name: main_dag main_dag_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER main_dag_log AFTER INSERT OR DELETE OR UPDATE ON public.main_dag FOR EACH ROW EXECUTE PROCEDURE public.process_main_dag_log();


--
-- Name: sbq_checker sbq_checker_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER sbq_checker_log AFTER INSERT OR DELETE OR UPDATE ON public.sbq_checker FOR EACH ROW EXECUTE PROCEDURE public.process_sbq_checker_log();


--
-- Name: slave_to_bq slave_to_bq_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER slave_to_bq_log AFTER INSERT OR DELETE OR UPDATE ON public.slave_to_bq FOR EACH ROW EXECUTE PROCEDURE public.process_slave_to_bq_log();


--
-- Name: spark_config spark_config_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER spark_config_log AFTER INSERT OR DELETE OR UPDATE ON public.spark_config FOR EACH ROW EXECUTE PROCEDURE public.process_spark_config_log();


--
-- Name: sub_dag sub_dag_log; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER sub_dag_log AFTER INSERT OR DELETE OR UPDATE ON public.sub_dag FOR EACH ROW EXECUTE PROCEDURE public.process_sub_dag_log();


--
-- Name: bq_checker update_modified_column_bq_checker; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_bq_checker BEFORE UPDATE ON public.bq_checker FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: bq_to_bq update_modified_column_bq_to_bq; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_bq_to_bq BEFORE UPDATE ON public.bq_to_bq FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: bq_to_bt update_modified_column_bq_to_bt; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_bq_to_bt BEFORE UPDATE ON public.bq_to_bt FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: bq_to_gs update_modified_column_bq_to_gs; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_bq_to_gs BEFORE UPDATE ON public.bq_to_gs FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: bq_to_pubsub update_modified_column_bq_to_pubsub; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_bq_to_pubsub BEFORE UPDATE ON public.bq_to_pubsub FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: database_connection update_modified_column_database_connection; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_database_connection BEFORE UPDATE ON public.database_connection FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: dataflow_config update_modified_column_dataflow_config; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_dataflow_config BEFORE UPDATE ON public.dataflow_config FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: gs_to_bq update_modified_column_gs_to_bq; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_gs_to_bq BEFORE UPDATE ON public.gs_to_bq FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: main_dag update_modified_column_main_dag; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_main_dag BEFORE UPDATE ON public.main_dag FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: sbq_checker update_modified_column_sbq_checker; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_sbq_checker BEFORE UPDATE ON public.sbq_checker FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: slave_to_bq update_modified_column_slave_to_bq; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_slave_to_bq BEFORE UPDATE ON public.slave_to_bq FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: sub_dag update_modified_column_sub_dag; Type: TRIGGER; Schema: public; Owner: recharge
--

CREATE TRIGGER update_modified_column_sub_dag BEFORE UPDATE ON public.sub_dag FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column();


--
-- Name: bq_checker bq_checker_dag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_checker
    ADD CONSTRAINT bq_checker_dag_id_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: bq_checker bq_checker_subdag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_checker
    ADD CONSTRAINT bq_checker_subdag_id_fk FOREIGN KEY (subdag_id) REFERENCES public.sub_dag(subdag_id);


--
-- Name: bq_to_bq bq_to_bq_main_dag_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bq
    ADD CONSTRAINT bq_to_bq_main_dag_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: bq_to_bq bq_to_bq_subdag_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bq
    ADD CONSTRAINT bq_to_bq_subdag_fk FOREIGN KEY (subdag_id) REFERENCES public.sub_dag(subdag_id);


--
-- Name: bq_to_bt bq_to_bt__subdag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bt
    ADD CONSTRAINT bq_to_bt__subdag_id_fk FOREIGN KEY (subdag_id) REFERENCES public.sub_dag(subdag_id);


--
-- Name: bq_to_bt bq_to_bt_dag_id__fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bt
    ADD CONSTRAINT bq_to_bt_dag_id__fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: bq_to_bt bq_to_bt_df__fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_bt
    ADD CONSTRAINT bq_to_bt_df__fk FOREIGN KEY (df_id) REFERENCES public.dataflow_config(df_id);


--
-- Name: bq_to_gs bq_to_gs_main_dag_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_gs
    ADD CONSTRAINT bq_to_gs_main_dag_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: bq_to_gs bq_to_gs_subdag_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_gs
    ADD CONSTRAINT bq_to_gs_subdag_fk FOREIGN KEY (subdag_id) REFERENCES public.sub_dag(subdag_id);


--
-- Name: bq_to_pubsub bq_to_pubsub_dag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_pubsub
    ADD CONSTRAINT bq_to_pubsub_dag_id_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: bq_to_pubsub bq_to_pubsub_df_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_pubsub
    ADD CONSTRAINT bq_to_pubsub_df_id_fk FOREIGN KEY (df_id) REFERENCES public.dataflow_config(df_id);


--
-- Name: bq_to_pubsub bq_to_pubsub_sub_dag_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.bq_to_pubsub
    ADD CONSTRAINT bq_to_pubsub_sub_dag_fk FOREIGN KEY (subdag_id) REFERENCES public.sub_dag(subdag_id);


--
-- Name: slave_to_bq dag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.slave_to_bq
    ADD CONSTRAINT dag_id_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: slave_to_bq db_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.slave_to_bq
    ADD CONSTRAINT db_id_fk FOREIGN KEY (db_id) REFERENCES public.database_connection(db_id);


--
-- Name: slave_to_bq df_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.slave_to_bq
    ADD CONSTRAINT df_id_fk FOREIGN KEY (df_id) REFERENCES public.dataflow_config(df_id);


--
-- Name: http_request http_request_dag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.http_request
    ADD CONSTRAINT http_request_dag_id_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: http_request http_request_sub_dag_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.http_request
    ADD CONSTRAINT http_request_sub_dag_fk FOREIGN KEY (subdag_id) REFERENCES public.sub_dag(subdag_id);


--
-- Name: sbq_checker sbq_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.sbq_checker
    ADD CONSTRAINT sbq_id_fk FOREIGN KEY (sbq_id) REFERENCES public.slave_to_bq(id);


--
-- Name: spark_config spark_config_dag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.spark_config
    ADD CONSTRAINT spark_config_dag_id_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: spark_config spark_config_subdag_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.spark_config
    ADD CONSTRAINT spark_config_subdag_id_fk FOREIGN KEY (subdag_id) REFERENCES public.sub_dag(subdag_id);


--
-- Name: sub_dag sub_dag_main_dag_fk; Type: FK CONSTRAINT; Schema: public; Owner: recharge
--

ALTER TABLE ONLY public.sub_dag
    ADD CONSTRAINT sub_dag_main_dag_fk FOREIGN KEY (dag_id) REFERENCES public.main_dag(dag_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: cloudsqlsuperuser
--



--
-- Name: TABLE bq_checker; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.bq_checker TO recharge;


--
-- Name: TABLE bq_to_bq; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.bq_to_bq TO recharge;


--
-- Name: TABLE bq_to_bt; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.bq_to_bt TO recharge;


--
-- Name: TABLE bq_to_gs; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.bq_to_gs TO recharge;


--
-- Name: TABLE slave_to_bq; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.slave_to_bq TO recharge;


--
-- Name: TABLE dag_slave_active; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.dag_slave_active TO recharge;


--
-- Name: TABLE database_connection; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.database_connection TO recharge;


--
-- Name: TABLE database_connection_log; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.database_connection_log TO recharge;


--
-- Name: TABLE dataflow_config; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.dataflow_config TO recharge;


--
-- Name: TABLE main_dag; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.main_dag TO recharge;


--
-- Name: TABLE sbq_checker; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.sbq_checker TO recharge;


--
-- Name: TABLE slave_to_bq_log; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.slave_to_bq_log TO recharge;


--
-- Name: TABLE spark_config; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.spark_config TO recharge;


--
-- Name: TABLE sub_dag; Type: ACL; Schema: public; Owner: recharge
--

GRANT SELECT ON TABLE public.sub_dag TO recharge;


--
-- PostgreSQL database dump complete
--

