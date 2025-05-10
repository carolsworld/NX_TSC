SELECT 
    ae.eventtime,
    ae.source,
    ae.priority,
    ae.eventtype,
    ae.eventflags,
    aed.floatvalue
FROM 
    public.alarm_events ae
JOIN 
    public.alarm_event_data aed
ON 
    ae.id = aed.id
WHERE 
    ae.eventtime::date = '2025-05-09'
ORDER BY 
    ae.id, aed.propname;
	