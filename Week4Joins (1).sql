Use pawsomepet;

-- Scenario 1: Cross Join (Cartesian Product)
-- This will display every possible combination of pets and clients
SELECT p.pet_name, c.first_name, c.last_name
FROM pets p
CROSS JOIN clients c;

-- Scenario 2: Inner Join
-- This retrieves all appointments including pet names and their owner's names
SELECT a.appointment_date, p.pet_name, c.first_name, c.last_name
FROM appointments a
INNER JOIN pets p ON a.pet_id = p.pet_id
INNER JOIN clients c ON p.client_id = c.client_id;

-- Scenario 3: Subquery as a Table in an Inner Join
-- This finds pets whose weight is above the average weight of all pets
SELECT p.pet_name, p.weight
FROM pets p
INNER JOIN (
    SELECT AVG(weight) AS avg_weight
    FROM pets
) avg_table ON p.weight > avg_table.avg_weight;

-- Scenario 4: Multi-Table Inner Join
-- This shows all appointments along with the pet name and service performed
SELECT a.appointment_date, p.pet_name, s.name AS service_name
FROM appointments a
INNER JOIN appointmentservices aps ON a.appointment_id = aps.appointment_id
INNER JOIN services s ON aps.service_id = s.service_id
INNER JOIN pets p ON a.pet_id = p.pet_id;

-- Scenario 5: Self-Join
-- This finds clients with the same last name (excluding matches to themselves)
SELECT c1.first_name AS client1_first, c2.first_name AS client2_first, c1.last_name
FROM clients c1
JOIN clients c2 ON c1.last_name = c2.last_name AND c1.client_id < c2.client_id;
