-- 1 Output the number of movies in each category, sorted descending.
SELECT
	c.name AS category,
	COUNT(*) AS movie_count
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
GROUP BY c.name
ORDER BY movie_count DESC;

-- 2 Output the 10 actors whose movies rented the most, sorted in descending order.
SELECT
	a.first_name,
	a.last_name,
	COUNT(r.rental_id) AS rental_count
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
JOIN inventory i ON fa.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY
	a.first_name,
	a.last_name
ORDER BY rental_count DESC
LIMIT 10;
	
-- 3 Output the category of movies on which the most money was spent.
SELECT
	c.name AS category_name,
	SUM(p.amount) AS money_spent_on_a_movie

FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN inventory i ON fc.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY 
	c.category_id,
	c.name
ORDER BY money_spent_on_a_movie DESC
LIMIT 1;
	
-- 4 Print the names of movies that are not in the inventory. Write a query without using the IN operator.
SELECT
	f.title
FROM film f
WHERE NOT EXISTS(
	SELECT 1
	FROM inventory i
	WHERE i.film_id = f.film_id
);

-- 5 Output the top 3 actors who have appeared the most in movies in the “Children” category. If several actors have the same number of movies, output all of them.
WITH actors_in_children_movies AS (
	SELECT 
		a.first_name,
		a.last_name,
		COUNT(*) AS times_appeared
	FROM actor a
	JOIN film_actor fa ON a.actor_id = fa.actor_id
	JOIN film_category fc ON fa.film_id = fc.film_id
	JOIN category c ON fc.category_id = c.category_id
	WHERE c.name = 'Children'
	GROUP BY 
		a.first_name,
		a.last_name
),
ranked_actors AS(
	SELECT
		*,
		DENSE_RANK()OVER(ORDER BY times_appeared DESC) as "rank"
	FROM actors_in_children_movies
)
SELECT
	first_name,
	last_name,
	times_appeared
FROM ranked_actors
WHERE "rank" <= 3;

-- 6 Output cities with the number of active and inactive customers (active - customer.active = 1). Sort by the number of inactive customers in descending order.
SELECT 
	c.city,
	COUNT(*) FILTER (WHERE cu.active = 1) AS active_customers,
	COUNT(*) FILTER (WHERE cu.active = 0) AS inactive_customers
FROM city c
JOIN address a ON c.city_id = a.city_id
JOIN customer cu ON a.address_id = cu.address_id
GROUP BY 
	c.city_id,
	c.city
ORDER BY inactive_customers DESC;

-- 7 Output the category of movies that have the highest number of total rental hours in the city (customer.address_id in this city) and that start with the letter “a”. Do the same for cities that have a “-” in them. Write everything in one query.
WITH rental_term AS (
	SELECT
		cat.name AS category_name,
		ci.city,
		ROUND(
			SUM(
			    EXTRACT(EPOCH FROM (r.return_date - r.rental_date)) / 3600
			), 2
		) AS rental_hours
	FROM rental r
	JOIN customer c ON r.customer_id = c.customer_id
	JOIN address a ON c.address_id = a.address_id
	JOIN city ci ON a.city_id = ci.city_id
	
	JOIN inventory i ON r.inventory_id = i.inventory_id
	JOIN film_category fc ON i.film_id = fc.film_id
	JOIN category cat ON fc.category_id = cat.category_id
	GROUP BY
		cat.name,
		ci.city
),
ranked_category AS(
	SELECT
		r.city,
		r.category_name,
		r.rental_hours,
		DENSE_RANK() OVER (
			PARTITION BY r.city
			ORDER BY r.rental_hours DESC
		) AS "rank"
	FROM rental_term r	
)
(
SELECT
	rc.city,
	rc.category_name,
	rc.rental_hours
FROM ranked_category rc
WHERE ("rank" = 1) AND (rc.category_name LIKE 'A%')
ORDER BY rental_hours DESC
LIMIT 1
)

UNION

(
SELECT
	rc.city,
	rc.category_name,
	rc.rental_hours
FROM ranked_category rc
WHERE ("rank" = 1) AND (rc.city LIKE '%-%')
ORDER BY rental_hours DESC
LIMIT 1
);


