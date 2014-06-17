SET CLIENT_ENCODING = 'UTF8';
SET CLIENT_MIN_MESSAGES = WARNING;

CREATE TABLE user_email (
    user_id         TEXT                      NOT NULL,
    email           TEXT                      UNIQUE NOT NULL,
    is_preferred    BOOLEAN                   NOT NULL DEFAULT 'false',
    verified_date   TIMESTAMP WITH TIME ZONE  DEFAULT NULL
);

-- The combination of user_id and email is unique within the system
CREATE UNIQUE INDEX USER_ID_EMAIL_PKEY ON USER_EMAIL
       USING BTREE (user_id, email);

-- The **lowered** form of the email-address is unique within the
-- system, and needs to be accessed quickly.
CREATE UNIQUE INDEX USER_EMAIL_EMAIL_LOWER_IDX ON USER_EMAIL
       USING BTREE (lower(email));


