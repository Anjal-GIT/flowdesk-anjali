task1: backend

Create a fastapi backend for a shipment management system-flowdesk: create one sql model: Shipment
id integer, primary key
tracking_code string, unique, auto-generated (format: SHP-YYYYMMDD-XXXXX)
origin string
destination string
status string → 'pending' | 'in_transit' | 'delivered' | 'cancelled'
weight_kg float
created_at datetime, default now()

Requirements: Use fastapi,SQLAlchemy,postgreSQL,pydanric

Authentication:

tracking_code is auto-generated and unique — format: SHP-YYYYMMDD-XXXXX
implement a reusable fastapi dependency using API key header: X-API-Key: secret..
return http 401 for missing or invalid key
add todo comment to replace with jwt in production



create clean folder structure:

database:
configure postgreql connection using sqlalchemy]

create base and engine
