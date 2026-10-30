CREATE TABLE IF NOT EXISTS websites  (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    url TEXT NOT NULL,
    css_selector TEXT,
    check_interval_minutes INTEGER NOT NULL DEFAULT 60 CHECK (check_interval_minutes >= 5),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS website_checks (
    id BIGSERIAL PRIMARY KEY,
    website_id BIGINT NOT NULL REFERENCES websites(id) ON DELETE CASCADE,
    checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status_code INTEGER,
    content_hash VARCHAR(64),
    has_changed BOOLEAN,
    error_message TEXT
);