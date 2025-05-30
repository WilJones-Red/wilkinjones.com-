USE pawsomepet;

-- I used these queries to verify that each table is populated with data.
-- I also used DESCRIBE (not shown here) to understand each table's structure.
SELECT * FROM pets;
SELECT * FROM breeds;
SELECT * FROM appointments;
SELECT * FROM services;
SELECT * FROM appointmentservices;

-- Scenario 1: Find all appointments after 2025-03-01
SELECT * 
FROM appointments
WHERE appointment_date > '2025-03-01';
-- This query returns all appointments scheduled after March 1, 2025.
-- I used a range condition (>) to filter by date.
-- The condition helps isolate upcoming or recent appointments after that point.

-- Scenario 2: Find clients with specific email addresses
SELECT * 
FROM clients
WHERE email IN ('johndoe@example.com');
-- This query finds clients who match a specific email address.
-- I used the IN operator to match against one or more known values.
-- It filters the dataset by checking if the email column matches any listed value.

-- Scenario 2 from Task 1: Find clients who are NOT using certain email addresses
SELECT * 
FROM clients
WHERE email NOT IN ('alice.johnson@example.com', 'bob.smith@example.com');
-- This query excludes clients with these specific emails.
-- I used NOT IN to show a non-equality comparison.
-- This filters out the specified values and keeps everything else.

-- Scenario 3: Find pets with names ending in 'a'
SELECT * 
FROM pets
WHERE pet_name LIKE '%a';
-- This finds all pets whose names end in the letter 'a'.
-- I used the LIKE operator with a wildcard pattern.
-- The pattern '%a' matches any name that ends with 'a'.

-- Scenario 4: Find pets with no weight recorded
SELECT * 
FROM pets
WHERE weight IS NULL;
-- This finds pets that have no value recorded for weight.
-- I used IS NULL because regular comparison operators don't work with NULL.
-- This lets us specifically find records with missing data.