docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres
gunzip -k dellstore.sql.gz
sleep 5
psql -p 5432 -h localhost -U postgres postgres < dellstore.sql
rm dellstore.sql