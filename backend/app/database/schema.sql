CREATE TABLE websites (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    url TEXT NOT NULL,
    css_selector TEXT,
    check_interval_minutes INTEGER NOT NULL DEFAULT 60 CHECK (check_interval_minutes >= 5),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);