# Database Schema for Wedding Band Song Request App

## Table: guests
- **id**: SERIAL PRIMARY KEY
- **name**: VARCHAR(255) (optional, can be NULL)
- **email**: VARCHAR(255) UNIQUE NOT NULL
- **password**: VARCHAR(255) NOT NULL (store hashed)
- **oauth_provider**: VARCHAR(255) -- Nullable, stores OAuth provider name
- **oauth_provider_id**: VARCHAR(255), -- Nullable, stores unique ID from the OAuth provider
- **created_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- **updated_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Table: bands
- **band_id**: SERIAL PRIMARY KEY
- **band_name**: VARCHAR(255) NOT NULL
- **band_email**: VARCHAR(255) UNIQUE NOT NULL
- **password**: VARCHAR(255) NOT NULL (store hashed)
- **oauth_provider**: VARCHAR(255) -- Nullable, stores OAuth provider name
- **oauth_provider_id**: VARCHAR(255), -- Nullable, stores unique ID from the OAuth provider
- **created_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- **updated_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Table: events
- **event_id**: SERIAL PRIMARY KEY
- **event_name**: VARCHAR(255) NOT NULL
- **location**: VARCHAR(255) NOT NULL
- **event_start**: TIMESTAMP NOT NULL
- **event_end**: TIMESTAMP NOT NULL
- **qr_code_content**: VARCHAR(2048) NOT NULL
- **band_id**: INTEGER NOT NULL REFERENCES bands(band_id)
- **max_requests_per_user** INTEGER DEFAULT NULL
- **created_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- **updated_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Table: requests
- **request_id**: SERIAL PRIMARY KEY
- **song_name**: VARCHAR(255) NOT NULL
- **guest_id**: INTEGER NOT NULL REFERENCES guests(id)
- **event_id**: INTEGER NOT NULL REFERENCES events(event_id)
- **created_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- **updated_at**: TIMESTAMP DEFAULT CURRENT_TIMESTAMP


## Table: OAuth Tokens

| Field           | Data Type          | Description                                             |
|-----------------|---------------------|---------------------------------------------------------|
| `token_id`      | `SERIAL PRIMARY KEY` | Unique identifier for each token entry                 |
| `user_id`       | `INTEGER`           | Foreign key linking to the `guests` table (nullable)   |
| `band_id`       | `INTEGER`           | Foreign key linking to the `bands` table (nullable)    |
| `access_token`  | `TEXT`              | The actual access token provided by the OAuth provider |
| `refresh_token` | `TEXT`              | The refresh token provided by the OAuth provider (nullable) |
| `token_type`    | `VARCHAR(255)`      | Type of token (e.g., 'Bearer')                          |
| `expires_at`    | `TIMESTAMP`         | Expiry timestamp of the access token                   |
| `created_at`    | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | Timestamp when the token was created  |
| `updated_at`    | `TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | Timestamp when the token was last updated |

### Constraints
- **Valid User or Band**: Ensures that either `user_id` or `band_id` is provided, but not both.
  ```sql
  CONSTRAINT valid_user_or_band CHECK (
      (user_id IS NOT NULL AND band_id IS NULL) OR
      (user_id IS NULL AND band_id IS NOT NULL)
  )
