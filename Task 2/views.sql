create view top5customers
as
select c.*,totalspent from customers c join 
	(select o.customer_id,
	sum(o.quantity* (select p.price from products p where o.product_id=p.id )) as totalspent 
	from orders o
	group by o.customer_id
	limit 5) as a
	on a.customer_id=c.id
	order by totalspent desc
	
	

create view revenuepercategory
as
select p.category,sum(o.quantity * p.price ) as totalprice
from products p
join orders o on o.product_id=p.id
group by p.category 


create view ordercountsbystatus
as
select a.order_status, sum(a.amount) as totalamount from
(
	select p.order_id, p.amount,
	case 
	when p.status='Completed' then 'Completed'
	when p.status='Refunded' and 
	not exists(select * from payments p2 where p.order_id=p2.order_id and p2.status='Completed')
	then 'Refunded'
	when p.status='Failed' and
	not exists(select * from payments p2 where p.order_id=p2.order_id and p2.status='Refunded')
	then 'Failed'
	when p.status='Pending' and
	not exists(select * from payments p2 where p.order_id=p2.order_id and p2.status='Failed')
	then 'Pending'
	else 'to be removed'
	end as order_status
	from payments p
) as a
where a.order_status !='to be removed'
group by a.order_status





create view month_over_month_revenue
as
SELECT 
    DATE_TRUNC('month', payment_date) AS revenue_month,
    SUM(amount) AS current_revenue,
    LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', payment_date)) AS previous_revenue,
    SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY DATE_TRUNC('month', payment_date)) AS revenue_change
FROM payments
WHERE status = 'Completed'
GROUP BY DATE_TRUNC('month', payment_date);






