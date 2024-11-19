CREATE TABLE email_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    recipient TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    error TEXT
);
