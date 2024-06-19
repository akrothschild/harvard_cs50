-- Keep a log of any SQL queries you execute as you solve the mystery.

/*
========================
SOLVING CS50X MYSTERY.
Disappearance of the Duck.
========================
*/

/*
========================
Get the DB schema
========================
*/
.schema

/*
========================
Check crime_scene_reports table
========================
*/
SELECT *
FROM crime_scene_reports
LIMIT 10;

/*
========================
Get all theft that happened on July, 28th
========================
*/
SELECT *
FROM crime_scene_reports
WHERE description LIKE 'Theft%'
  AND day = 28
  AND month = 7;

/*
========================
Check bakery_security_logs
========================
*/
SELECT *
FROM bakery_security_logs
WHERE year = 2023
  AND month = 7
  AND DAY = 28
  AND hour < 11;

/*
========================
Find out who's license plate it is.
========================
*/
SELECT *
FROM people AS p
         JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
WHERE bsl.year = 2023
  AND bsl.month = 7
  AND bsl.day = 28
  AND ((hour < 10) OR (hour = 10 AND minute < 15));

/*
========================
Check interviews mentioning bakery
========================
*/
SELECT *
FROM interviews
WHERE transcript LIKE '%bakery%';
/*
+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id  |  name   | year | month | day |                                                                                                                                                     transcript                                                                                                                                                      |
+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 161 | Ruth    | 2023 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
| 162 | Eugene  | 2023 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
| 163 | Raymond | 2023 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
| 192 | Kiana   | 2023 | 5     | 17  | I saw Richard take a bite out of his pastry at the bakery before his pastry was stolen from him.                                                                                                                                                                                                                    |
+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
*/

/*
========================
Find out who's license plate it is.
========================
*/
SELECT *
FROM people AS p
         JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
WHERE bsl.year = 2023
  AND bsl.month = 7
  AND bsl.day = 28
  AND (hour = 10)
  AND (minute > 4 AND minute < 26);

/*
+--------+---------+----------------+-----------------+---------------+-----+------+-------+-----+------+--------+----------+---------------+
|   id   |  name   |  phone_number  | passport_number | license_plate | id  | year | month | day | hour | minute | activity | license_plate |
+--------+---------+----------------+-----------------+---------------+-----+------+-------+-----+------+--------+----------+---------------+
| 325548 | Brandon | (771) 555-6667 | 7874488539      | R3G7486       | 258 | 2023 | 7     | 28  | 10   | 8      | entrance | R3G7486       |
| 745650 | Sophia  | (027) 555-1068 | 3642612721      | 13FNH73       | 259 | 2023 | 7     | 28  | 10   | 14     | entrance | 13FNH73       |
| 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       | 260 | 2023 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       | 261 | 2023 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       | 262 | 2023 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       | 263 | 2023 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       | 264 | 2023 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       | 265 | 2023 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       | 266 | 2023 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       | 267 | 2023 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
+--------+---------+----------------+-----------------+---------------+-----+------+-------+-----+------+--------+----------+---------------+
*/

/*
========================
Find out who withdrew money from ATM on Legget
========================
*/
SELECT *
FROM people AS p
         JOIN bank_accounts AS ba ON p.id = ba.person_id
         JOIN atm_transactions AS atm ON ba.account_number = atm.account_number
WHERE atm.day = 28
  AND atm.month = 7
  AND atm.atm_location LIKE '%Leggett%';

/*
========================
Get their names
========================
*/
SELECT p.name, p.phone_number
FROM people AS p
         JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
         JOIN (SELECT *
               FROM people AS p
                        JOIN bank_accounts AS ba ON p.id = ba.person_id
                        JOIN atm_transactions AS atm ON ba.account_number = atm.account_number
               WHERE atm.day = 28
                 AND atm.month = 7
                 AND atm.atm_location LIKE '%Leggett%') AS p_ba ON p.license_plate = p_ba.license_plate
WHERE bsl.year = 2023
  AND bsl.month = 7
  AND bsl.day = 28
  AND (hour = 10)
  AND (minute > 4 AND minute < 26);
/*
+-------+----------------+
| name  |  phone_number  |
+-------+----------------+
| Bruce | (367) 555-5533 |
| Diana | (770) 555-1861 |
| Iman  | (829) 555-5269 |
| Luca  | (389) 555-5198 |
+-------+----------------+
*/

/*
========================
Find out who had a call that lasted <60 seconds
========================
*/
SELECT *
FROM phone_calls
WHERE duration < 60
  AND day = 28
  AND month = 7;

/*
========================
Join call results with ATM and bakery security results
========================
*/
SELECT peeps.name, pc.caller, pc.receiver
FROM phone_calls AS pc
         JOIN (SELECT p.name, p.phone_number
               FROM people AS p
                        JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
                        JOIN (SELECT *
                              FROM people AS p
                                       JOIN bank_accounts AS ba ON p.id = ba.person_id
                                       JOIN atm_transactions AS atm ON ba.account_number = atm.account_number
                              WHERE atm.day = 28
                                AND atm.month = 7
                                AND atm.atm_location LIKE '%Leggett%') AS p_ba ON p.license_plate = p_ba.license_plate
               WHERE bsl.year = 2023
                 AND bsl.month = 7
                 AND bsl.day = 28
                 AND (hour = 10)
                 AND (minute > 4 AND minute < 26)) AS peeps ON pc.caller = peeps.phone_number
WHERE pc.duration < 60
  AND pc.day = 28
  AND pc.month = 7;
/*
+-------+----------------+----------------+
| name  |     caller     |    receiver    |
+-------+----------------+----------------+
| Bruce | (367) 555-5533 | (375) 555-8161 |
| Diana | (770) 555-1861 | (725) 555-3243 |
+-------+----------------+----------------+
*/

/* OPTIMIZE INPUT */

SELECT peeps.name, peeps.passport_number, pc.caller, pc.receiver
FROM phone_calls AS pc
         JOIN (SELECT p.name, p.phone_number, p.passport_number
               FROM people AS p
                        JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
                        JOIN bank_accounts AS ba ON p.id = ba.person_id
                        JOIN atm_transactions AS atm ON ba.account_number = atm.account_number
               WHERE atm.day = 28
                 AND atm.month = 7
                 AND atm.atm_location LIKE '%Leggett%'
                 AND bsl.year = 2023
                 AND bsl.month = 7
                 AND bsl.day = 28
                 AND bsl.hour = 10
                 AND bsl.minute > 4
                 AND bsl.minute < 26) AS peeps ON pc.caller = peeps.phone_number
WHERE pc.duration < 60
  AND pc.day = 28
  AND pc.month = 7;

/*
========================
Get EARLIEST flight and join with previous table.
(Yeah, it took some time, before I got that we need an EARLIEST flight. Otherwise, we get Diana as well)
Also join peoples table to find out the name of their accomplice.
========================
*/
SELECT pass.name,
       pass.passport_number,
       pass.caller,
       pass.receiver,
       people.name,
       pass.license_plate,
       f.id,
       f.hour,
       f.minute,
       f.day,
       f.month,
       a.city,
       a.full_name,
       f.month,
       f.day
FROM flights AS f
         JOIN passengers AS p on f.id = p.flight_id
         JOIN airports AS a ON f.destination_airport_id = a.id
         JOIN (SELECT *
               FROM phone_calls AS pc
                        JOIN (SELECT *
                              FROM people AS p
                                       JOIN bakery_security_logs AS bsl ON p.license_plate = bsl.license_plate
                                       JOIN bank_accounts AS ba ON p.id = ba.person_id
                                       JOIN atm_transactions AS atm ON ba.account_number = atm.account_number
                              WHERE atm.day = 28
                                AND atm.month = 7
                                AND atm.atm_location LIKE '%Leggett%'
                                AND bsl.year = 2023
                                AND bsl.month = 7
                                AND bsl.day = 28
                                AND bsl.hour = 10
                                AND bsl.minute > 4
                                AND bsl.minute < 26) AS peeps ON pc.caller = peeps.phone_number
               WHERE pc.duration < 60
                 AND pc.day = 28
                 AND pc.month = 7) AS pass ON p.passport_number = pass.passport_number
         JOIN people ON pass.receiver = people.phone_number
WHERE f.day = 29
ORDER BY f.hour, f.minute
LIMIT 1;

/*
+-------+-----------------+----------------+----------------+-------+---------------+----+------+--------+-----+-------+---------------+-------------------+-------+-----+
| name  | passport_number |     caller     |    receiver    | name  | license_plate | id | hour | minute | day | month |     city      |     full_name     | month | day |
+-------+-----------------+----------------+----------------+-------+---------------+----+------+--------+-----+-------+---------------+-------------------+-------+-----+
| Bruce | 5773159633      | (367) 555-5533 | (375) 555-8161 | Robin | 94KL13X       | 36 | 8    | 20     | 29  | 7     | New York City | LaGuardia Airport | 7     | 29  |
+-------+-----------------+----------------+----------------+-------+---------------+----+------+--------+-----+-------+---------------+-------------------+-------+-----+

*/

/*
========================
The THIEF is: Bruce
The city the thief ESCAPED TO: New York City
The ACCOMPLICE is: Robin
========================
*/

/*
========================
    MYSTERY SOLVED
========================
*/