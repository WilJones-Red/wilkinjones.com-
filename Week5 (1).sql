-- Scenario 1: Using the UNION Operator
-- This query retrieves all email addresses from the clients and pets tables, combining them into a single set.
-- It avoids duplicates automatically by using UNION.
SELECT email FROM clients
UNION
SELECT email FROM pets
WHERE email IS NOT NULL;

-- Scenario 2: Using the INTERSECT Operator
-- This query finds phone numbers that are present in both the clients table and emergency contacts
-- INTERSECT returns only the values that appear in both queries.
SELECT phone_number FROM clients
INTERSECT
SELECT phone_number FROM EmergencyContacts;

-- Scenario 3: Using the EXCEPT Operator
-- This query lists all pet names that do not have an appointment.
-- EXCEPT removes pet names that appear in the result of the second query (i.e., pets with appointments).
SELECT pet_name FROM pets
EXCEPT
SELECT p.pet_name
FROM pets p
JOIN appointments a ON p.pet_id = a.pet_id;

-- Scenario 4: Sorting Compound Queries
-- This query merges names from clients and pets into a single column and sorts them alphabetically.
-- UNION is used to avoid duplicate names in the final result.
SELECT first_name AS na FROM clients
UNION
SELECT pet_name AS name FROM pets
ORDER BY name ASC;
