CREATE TABLE IF NOT EXISTS purchasing.sales AS
  SELECT d.duedate, SUM(d.unitprice) "USD", SUM(d.unitprice * c.currency_value) "PLN"
            FROM purchasing.purchaseorderdetail d
            INNER JOIN purchasing.pln_currencies c ON d.duedate = c.currency_date
            GROUP BY d.duedate
			ORDER BY d.duedate;