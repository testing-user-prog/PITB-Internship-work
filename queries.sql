


--look for the orders of which the customer has done payment more than two times
select * from orders where id in (
	select order_id from payments p 
	where exists (select * from payments p1 where p.id !=p1.id and p1.status='Completed' and p.order_id=p1.order_id )
	and p.status='Completed'
)

--users whose total spending is higher than the avg spending of all users on the platform
with getaverage as
(
select avg(total) as avg_amount from (
	select distinct o.customer_id as id,sum(p.amount ) as total 
	from orders o 
	join payments p on p.order_id = o.id
	where status='Completed'
	group by customer_id
	) as a
)
select * from customers c 
where c.id in
(
	select distinct o.customer_id 
	from orders o 
	join payments p on p.order_id = o.id
	where status='Completed'
	group by customer_id
	having sum(p.amount )> (select avg_amount from getaverage)
)



-- customers who have never placed a single order larger than $500, but whose total lifecycle spending is still higher than the global average lifecycle spending of all customers.
with customerstotals as
	(
	select c.id as cusid, sum(p.amount ) as custotal from orders o 
	join payments p on o.id=p.order_id and p.status ='Completed'
	join customers c on c.id =o.customer_id 
	group by c.id 
)
select * from customers c where c.id in
(
	select cusid from customerstotals where custotal > (select avg(custotal) from customerstotals)
	intersect 
	select c.id  from customers c where c.id not in(  
		select customer_id from orders o 
		join payments p on p.order_id =o.id 
		where p.status ='Completed' and p.amount >=500
)
)

-- Each products title, category, and price along with the row_number and its rank

select row_number() over (partition by category order by price desc) as row_num,rank() over (partition by category order by price desc) as rank_num,title,category,price
from products p
 
-- query to display each customer's first_name, last_name, total number of payment attempts made across all their orders, count of successful payments, and count of failed payments

with getuniqueorderids
as
(
select distinct  id,customer_id
from orders o  
)
select (select c.first_name  from customers c where c.id =b.id ),(select c.last_name  from customers c where c.id=b.id ),b.totalorders ,b.completedorders 
from
(
	select c.id,0 as totalorders, 0 as CompletedOrders
	from customers c 
	where not exists(select * from orders o where o.customer_id =c.id  )
	UNION
	select a.customer_id as cid ,a.totalorders,count(*) as CompletedOrders 
	from
	(
	select *, count(o.id) over (partition by c.id) as totalorders
	from customers c
	left join getuniqueorderids o on o.customer_id =c.id 
	join payments p on p.order_id = o.id  
	) as a
	where a.status='Completed'
	group by a.customer_id,a.first_name,a.last_name ,a.totalorders
) as b



-- For an order placed by a customer show the difference of dates between the next and the previous order
with getuniqueorders
as
(
select distinct id,o.customer_id ,o.order_date
from orders o  
)
select a.customer_id,a.id,a.order_date,
case 
	when a.prev_orderdate is null then 0
	else a.order_date::date-a.prev_orderdate::date
end as date_difference
from
	(
	select *, lag(o.order_date) over (partition by o.customer_id order by o.order_date) as prev_orderdate
	from getuniqueorders o 
	) as a


	
-- For each customer find the date of their first order, date of their recent order and total orders
with getuniqueorders
as
(
select distinct id,o.customer_id ,o.order_date  
from orders o  
)
select distinct o.customer_id ,count(o.id ) over(partition by o.customer_id  ) as total_orders, MAX(o.order_date ) over (partition by o.customer_id ) as RecentOrder,MIN(o.order_date ) over (partition by o.customer_id ) as firstorder
from getuniqueorders o



-- Customer along with their total spendings on each order
with getvalidordernumbers
as
(
select o.id,o.customer_id,o.product_id,o.quantity 
from orders o 
where exists (select * from payments p where o.id =p.order_id and p.status ='Completed' )
)
select b.customer_id,sum(b.totalorderspendings ) as customertotals
from
(
	select t1.customer_id,sum(t1.quantity * p1.price ) as totalorderspendings
	from getvalidordernumbers t1
	join products p1 on p1.id=t1.product_id
	group by t1.customer_id,t1.id
) as b
group by b.customer_id
order by sum(b.totalorderspendings ) desc



-- Top Selling product for each Customer

with totalproductsofcustomer
as
(
select a.customer_id,a.product_id,sum(a.quantity ) as totalpurchased
from
(
	select * from orders o
	where exists(select * from payments p where o.id =p.order_id and p.status ='Completed')
) as a
group by a.customer_id,a.product_id 
)
select a1.customer_id,a1.product_id ,a1.totalpurchased 
from totalproductsofcustomer a1 
where a1.totalpurchased =(select Max(a2.totalpurchased)
							from totalproductsofcustomer a2 where
							a1.customer_id =a2.customer_id )
							
							
-- categorize each order's payment status into simple, human-readable labels.'PAID', 'NEEDS ATTENTION', 'UNSUCCESSFUL'
with successful
as
(	
	select distinct o.id  
	from orders o 
	join payments p on o.id=p.order_id 
	where p.status = 'Completed'
),
pending
as
(
	select distinct o.id 
	from orders o 
	join payments p on o.id=p.order_id 
	where p.status = 'Pending'

)
select distinct o.id,
case
when o.id in (select id from successful ) then 'PAID'
when o.id in (select id from pending)  then 'NEEDS ATTENTION'
else 'Failed'
end as Payment_flag
from orders o

						