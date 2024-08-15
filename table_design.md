# Database Schema for Wedding Band Song Request App

## Table: guests
- **id**: SERIAL PRIMARY KEY
- **name**: VARCHAR(255) (optional, can be NULL)
- **email**: VARCHAR(255) UNIQUE NOT NULL
- **password**: VARCHAR(255) NOT NULL (store hashed)

## Table: bands
- **band_id**: SERIAL PRIMARY KEY
- **band_name**: VARCHAR(255) NOT NULL
- **band_email**: VARCHAR(255) UNIQUE NOT NULL

## Table: events
- **event_id**: SERIAL PRIMARY KEY
- **event_name**: VARCHAR(255) NOT NULL
- **location**: VARCHAR(255) NOT NULL
- **event_start**: TIMESTAMP NOT NULL
- **event_end**: TIMESTAMP NOT NULL
- **qr_code_content**: VARCHAR(2048) NOT NULL
- **band_id**: INTEGER NOT NULL REFERENCES bands(band_id)

## Table: requests
- **request_id**: SERIAL PRIMARY KEY
- **song_name**: VARCHAR(255) NOT NULL
- **guest_id**: INTEGER NOT NULL REFERENCES guests(id)
- **event_id**: INTEGER NOT NULL REFERENCES events(event_id)
