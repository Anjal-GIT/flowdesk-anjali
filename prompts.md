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

track code geneartor:

create an utility function

pydantic schemas:

create 
shipmentcreate:
fields: origin,destination,weight_kg

shipment response:

fields: id,tracking code,origin,destination,status,weight_kg,created_at


use pydantic from attributes


create apis:

get/shipments:no authentication
features should be:
list of shipments
filters
pagination

response:
items:[]
total:0
page:1
page_size:5


post/shipments: required authentication
input: origin,destination,weight_kg
generate the tracking code automatically
default status:pending
return 201

GET /shipments/{id}
return shipment
if not found:401

PATCH /shipments/{id}/status: required authentication
input: status
rules are: pending → in_transit | cancelled
in_transit → delivered | cancelled
delivered → (terminal — no further updates allowed)
cancelled → (terminal — no further updates allowed)
invalid transition: return http 422 with error message


