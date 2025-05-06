# Idea
This script checks for active connections that have been open longer than 5 minutes. It returns:
• OK (0) if there are none
• WARNING (1) if there are fewer than five
• CRITICAL (2) if there are five or more

# Preparations

## Data base preparations
Create user:
```sql
CREATE USER monitor WITH PASSWORD 'PASSWORD';
```
Create a function. 
```sql
CREATE OR REPLACE FUNCTION public.get_long_running_queries()
RETURNS bigint AS $$
BEGIN
    RETURN (
        SELECT count(*) 
        FROM pg_stat_activity 
        WHERE state <> 'idle' 
          AND now() - query_start > interval '5 minutes'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```
Creating a function is safer than using a direct query since users will not gain direct access to _pg_stat_activity_.
Grant permissions
```sql
GRANT EXECUTE ON FUNCTION public.get_long_running_queries() TO monitor;
```
Check permissions:
```sql
SET ROLE monitor;
SELECT public.get_long_running_queries();
```
## Nagios server preprations

Copy script file then create .env file:
```bash
DB_USER=monitor
DB_PASSWORD=PASSWORD
DB_NAME=DB_NAME
```

## Nagios command config
```conf

```
