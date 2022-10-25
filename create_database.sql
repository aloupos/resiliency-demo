
/*
needs password authentication and authorization set in cassandra.yaml
or setup other authorization
*/
/* use this keyspace for single cluster demos
*/
create user 'demo' with password 'Demo123!';
create keyspace demo
   WITH REPLICATION = {
   'class' : 'SimpleStrategy',
   'replication_factor' : 1
   };

   /* or this for multi-cluster resiliency demos
   */

   /* first we need to ensure replication of user data accross
   both data centers is setup */

ALTER KEYSPACE "system_auth"
  WITH REPLICATION = {
    'class' : 'NetworkTopologyStrategy',
    'cl1-us-south' : 2 , // Datacenter 1
    'cl2-us-east'   : 2   // Datacenter 2
  };

   CREATE KEYSPACE "demo"
     WITH REPLICATION = {
      'class' : 'NetworkTopologyStrategy',
      'cl1-us-south' : 2 , // Datacenter 1
      'cl2-us-east'   : 2   // Datacenter 2
     };


grant all on keyspace demo to demo;


use demo;

DROP TABLE demo.customers;
DROP TABLE demo.account;
DROP TABLE demo.account_type;
DROP TABLE demo.transactions;

  CREATE TABLE demo.customers (
    id int PRIMARY KEY,
    first_name text,
    last_name text,
    date_of_birth date,
    username text,
    member_since date,
    social_sec_number	int);

    CREATE TABLE demo.account (
      id int PRIMARY KEY,
      customer_id int,
      account_type_id int,
      account_number int,
      opened_date date,
      credit_limit  decimal,
      credit_int_rate decimal,
      acct_int_rate decimal);

    CREATE TABLE demo.account_type (
      id int PRIMARY KEY,
      descripton text,
      product_name text,
      credit_limit decimal,
      min_balance decimal,
      overdraft_fee decimal,
      domestic_wire_fee decimal,
      overseas_wire_fee decimal );

    CREATE TABLE demo.transactions (
      id int,
      account_id int,
      date timestamp,
      type int,
      debit_amount decimal,
      debit_type int,
      credit_amount	decimal,
      credit_type	int,
      merchant	text,
      description	text,
      PRIMARY KEY (account_id,id)) WITH CLUSTERING ORDER BY (id DESC);


insert into demo.customers (id,first_name,last_name,date_of_birth,username,member_since,social_sec_number )
values(
1,'bob','smith','1994-10-01','bsmith1@gmail.com','2005-01-14',199949999
);
insert into demo.customers (id,first_name,last_name,date_of_birth,username,member_since,social_sec_number )
values(
2,'ralph','dunn','1998-11-07','rdun14@gmail.com','2008-03-13',175541986
);
insert into demo.customers (id,first_name,last_name,date_of_birth,username,member_since,social_sec_number )
values(
3,'ron','johnson','2001-04-26','rj179@gmail.com','2018-03-17',233441993
);

insert into account_type (id,descripton,product_name,credit_limit,min_balance,overdraft_fee,domestic_wire_fee,overseas_wire_fee) VALUES (
1,'acq1 savings','Premier Savings',0,0,15.00,10.00,25.00
);
insert into account_type (id,descripton,product_name,credit_limit,min_balance,overdraft_fee,domestic_wire_fee,overseas_wire_fee) VALUES (
2,'acq1 checking','Premier Checking',0,0,15.00,10.00,25.00
);

insert into account (id,customer_id,account_type_id,account_number,opened_date,credit_limit,credit_int_rate,acct_int_rate)
  VALUES (
    1,2,1,400751985,'1998-11-07',0,0,1.74
  );
  insert into account (id,customer_id,account_type_id,account_number,opened_date,credit_limit,credit_int_rate,acct_int_rate)
    VALUES (
      2,2,2,400751985,'1998-11-07',0,0,1.74
  );
