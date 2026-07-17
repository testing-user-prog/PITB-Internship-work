--orders where a transaction failed, and the customer never successfully processed a follow-up payment
select * from orders o 
where o.id not in (
	Select order_id from payments p 
	where status!='Failed'
)


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

