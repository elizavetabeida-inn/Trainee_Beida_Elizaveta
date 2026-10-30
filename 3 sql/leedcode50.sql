------- 10 easy:
-- 1757. Recyclable and Low Fat Products
SELECT product_id
FROM Products
WHERE (low_fats = 'Y') AND (recyclable = 'Y')

-- 584. Find Customer Referee
SELECT name
FROM Customer
WHERE (referee_id != 2) OR (referee_id IS NULL);

-- 1068. Product Sales Analysis I
SELECT
    p.product_name,
    s.year,
    s.price
FROM Sales s
JOIN Product p ON s.product_id = p.product_id;

-- 1581. Customer Who Visited but Did Not Make Any Transactions
SELECT
    v.customer_id,
    COUNT(*) AS count_no_trans
FROM Visits v
LEFT JOIN Transactions t ON v.visit_id = t.visit_id
WHERE t.transaction_id IS NULL
GROUP BY v.customer_id;

-- 1075. Project Employees I
SELECT 
    p.project_id,
    ROUND(AVG(e.experience_years), 2) AS average_years
FROM Project p
JOIN Employee e ON p.employee_id = e.employee_id
GROUP BY p.project_id;

-- 1141. User Activity for the Past 30 Days I
SELECT
    activity_date AS day,
    COUNT(DISTINCT user_id) AS active_users
FROM Activity
WHERE activity_date BETWEEN '2019-06-28' AND '2019-07-27'
GROUP BY activity_date

-- 1729. Find Followers Count
SELECT
    user_id,
    COUNT(*) AS followers_count
FROM Followers
GROUP BY user_id
ORDER BY user_id;

-- 1789. Primary Department for Each Employee
SELECT employee_id, department_id
FROM Employee
WHERE primary_flag = 'Y'
   OR employee_id IN (
       SELECT employee_id
       FROM Employee
       GROUP BY employee_id
       HAVING COUNT(*) = 1
   );

-- 1978. Employees Whose Manager Left the Company
SELECT employee_id
FROM Employees
WHERE salary < 30000 
    AND
    manager_id NOT IN (
        SELECT employee_id
        FROM Employees
    )
ORDER BY employee_id;

-- 1527. Patients With a Condition
SELECT
    patient_id,
    patient_name,
    conditions
FROM Patients
WHERE conditions REGEXP '(^| )DIAB1'





---------------- Medium:
-- 570. Managers with at Least 5 Direct Reports
SELECT
    e.name
FROM Employee e
JOIN Employee r ON e.id = r.managerId
GROUP BY e.id, e.name
HAVING COUNT(*) >= 5

-- 1934. Confirmation Rate
SELECT
    s.user_id,
    ROUND(
        COALESCE(
            AVG(c.action = 'confirmed'), 0
        ), 2
    ) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c ON s.user_id = c.user_id
GROUP BY s.user_id
    
-- 1193. Monthly Transactions I

SELECT
    DATE_FORMAT(trans_date, '%Y-%m') AS month,
    country,
    COUNT(*) AS trans_count,
    SUM(state = 'approved') AS approved_count,
    SUM(amount) AS trans_total_amount,
    SUM(IF(state = 'approved', amount, 0)) AS approved_total_amount
FROM Transactions
GROUP BY
    DATE_FORMAT(trans_date, '%Y-%m'),
    country;

-- 550. Game Play Analysis IV
SELECT 
    ROUND(
        COUNT(DISTINCT a.player_id)/
        (SELECT COUNT(DISTINCT player_id) FROM Activity)
        , 2
    ) AS fraction
FROM Activity a
JOIN (
    SELECT
        player_id,
        MIN(event_date) AS first_login
    FROM Activity
    GROUP BY player_id
) first_logins
    ON a.player_id = first_logins.player_id
    AND DATEDIFF(a.event_date, first_logins.first_login) = 1;


-- 1070. Product Sales Analysis III
SELECT 
    product_id,
    year AS first_year,
    quantity,
    price
FROM Sales
WHERE (product_id, year) IN (
    SELECT 
        product_id,
        MIN(year) AS year
    FROM Sales
    GROUP BY product_id
)
    
-- 1045. Customers Who Bought All Products
    
SELECT 
    customer_id
FROM Customer
GROUP BY customer_id
HAVING  COUNT(DISTINCT product_key) = (SELECT COUNT(*) FROM Product)

-- 180. Consecutive Numbers
SELECT DISTINCT l1.num AS ConsecutiveNums 
FROM Logs l1
JOIN Logs l2 ON l1.id = l2.id - 1
JOIN Logs l3 ON l2.id = l3.id - 1
WHERE l1.num = l2.num AND l2.num = l3.num

-- 1164. Product Price at a Given Date
SELECT
    product_id,
    10 AS price
FROM Products
GROUP BY product_id
HAVING MIN(change_date) > '2019-08-16'

UNION

SELECT
    product_id,
    new_price AS price
FROM Products
WHERE (product_id, change_date) IN (
    SELECT
        product_id,
        MAX(change_date) 
    FROM Products
    WHERE change_date <= '2019-08-16'
    GROUP BY product_id
)

-- 1204. Last Person to Fit in the Bus
SELECT person_name
FROM (
    SELECT
        person_name,
        SUM(weight) OVER (ORDER BY turn) AS total_weight
    FROM Queue
) AS q
WHERE total_weight <= 1000
ORDER BY total_weight DESC
LIMIT 1;

-- 1907. Count Salary Categories
SELECT
    'Low Salary' AS category,
    COUNT(*) AS accounts_count
FROM Accounts
WHERE income < 20000

UNION

SELECT
    'Average Salary' AS category,
    COUNT(*) AS accounts_count
FROM Accounts
WHERE income BETWEEN 20000 AND 50000

UNION

SELECT
    'High Salary' AS category,
    COUNT(*) AS accounts_count
FROM Accounts
WHERE income > 50000

-- 626. Exchange Seats
SELECT
    CASE
        WHEN id % 2 = 1 AND id < (SELECT MAX(id) FROM Seat)
            THEN id + 1
        WHEN id % 2 = 0
            THEN id - 1
        ELSE id
    END AS id,
    student
FROM Seat
ORDER BY id ASC

-- 1341. Movie Rating
(
    SELECT u.name AS results
    FROM Users u
    JOIN MovieRating mr ON u.user_id = mr.user_id
    GROUP BY u.user_id, u.name
    ORDER BY COUNT(*) DESC, u.name ASC
    LIMIT 1
)

UNION ALL

(
    SELECT m.title AS results
    FROM Movies m
    JOIN MovieRating mr ON m.movie_id = mr.movie_id
    WHERE mr.created_at >= '2020-02-01' AND mr.created_at < '2020-03-01'
    GROUP BY m.movie_id, m.title
    ORDER BY AVG(mr.rating) DESC, m.title ASC
    LIMIT 1
);

-- 1321. Restaurant Growth
SELECT
    visited_on,
    amount,
    ROUND(average_amount, 2) AS average_amount
FROM (
    SELECT
        visited_on,
        daily_amount,
        SUM(daily_amount) OVER (
            ORDER BY visited_on
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS amount,
        AVG(daily_amount) OVER (
            ORDER BY visited_on
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS average_amount,
        ROW_NUMBER() OVER (ORDER BY visited_on) AS rn
    FROM (
        SELECT
            visited_on,
            SUM(amount) AS daily_amount
        FROM Customer
        GROUP BY visited_on
    ) AS daily
) AS t
WHERE rn >= 7
ORDER BY visited_on;

-- 602. Friend Requests II: Who Has the Most Friends
SELECT
    id,
    COUNT(*) AS num
FROM (
    SELECT requester_id AS id
    FROM RequestAccepted

    UNION ALL

    SELECT accepter_id AS id
    FROM RequestAccepted
) AS friends
GROUP BY id
ORDER BY num DESC
LIMIT 1;

-- 585. Investments in 2016
SELECT
    ROUND(SUM(tiv_2016), 2) AS tiv_2016
FROM (
    SELECT
        tiv_2016,
        COUNT(*) OVER (PARTITION BY tiv_2015) AS tiv_count,
        COUNT(*) OVER (PARTITION BY lat, lon) AS location_count
    FROM Insurance
) AS t
WHERE tiv_count > 1 AND location_count = 1

-- 185. Department Top Three Salaries
SELECT 
    Department,
    Employee,
    Salary
FROM (
    SELECT
        d.name AS Department,
        e.name AS Employee,
        e.salary AS Salary,
        DENSE_RANK() OVER (
            PARTITION BY d.name
            ORDER BY e.salary DESC
        ) AS rnk
        
    FROM Employee e
    JOIN Department d ON e.departmentId = d.id

) AS t
WHERE rnk BETWEEN 1 AND 3

-- 176. Second Highest Salary
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS SecondHighestSalary

