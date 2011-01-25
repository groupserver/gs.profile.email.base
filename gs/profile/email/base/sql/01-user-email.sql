SET CLIENT_ENCODING = 'UTF8';
SET CLIENT_MIN_MESSAGES = WARNING;

CREATE TABLE USER_EMAIL (
    USER_ID         TEXT                      NOT NULL,
    EMAIL           TEXT                      UNIQUE NOT NULL,
    IS_PREFERRED    BOOLEAN                   NOT NULL DEFAULT 'false',
    VERIFIED_DATE   TIMESTAMP WITH TIME ZONE  DEFAULT NULL
);

-- The combination of user_id and email is unique within the system
CREATE UNIQUE INDEX USER_ID_EMAIL_PKEY ON USER_EMAIL
       USING BTREE (user_id, email);

-- Email is unique within the system
CREATE UNIQUE INDEX USER_EMAIL_EMAIL_LOWER_IDX ON USER_EMAIL
       USING BTREE (lower(email));


