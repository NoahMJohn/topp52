-- Lister alle turer pr bruke
select id, tour_date
from tours
WHERE
user_id = 6
AND
tour_date >= '2021-01-01'
AND
tour_date <= '2021-12-31'
order by tour_date

-- Toppliste
select t.user_id, u.username, count(*) count_tours
from tours t
join users u on u.id = t.user_id
WHERE
t.tour_date >= '2021-01-01' and t.tour_date <= '2021-12-31'
group by t.user_id
order by count(*) DESC
limit 50

-- Siste turer
select t.*, u.username 
from tours t
join users u on u.id = t.user_id
WHERE
u.visible = TRUE
order by t.tour_date desc, t.created desc
limit 10

-- Antall egne turer
select count(*) count_tours
FROM
tours
WHERE
user_id = 6
AND
tour_date >= '2021-01-01'
AND
tour_date <= '2021-12-31'

-- Antall turer i år
select count(*) count_tours
FROM
tours
WHERE
tour_date >= '2021-01-01'
AND
tour_date <= '2021-12-1'

select * from tours;