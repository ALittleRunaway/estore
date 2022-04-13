create table role
(
	id int primary key auto_increment,
	name nvarchar(100) not null
);

create table user
(
	id int primary key auto_increment,
	name nvarchar(100) not null,
	surname nvarchar(100) not null,
	patronymic nvarchar(100) not null,
	login nvarchar(255) not null,
	password nvarchar(255) not null,
	role_id int not null,
	foreign key(role_id) references role(id)
);

create table pickup_point
(
	id int primary key auto_increment,
	address nvarchar(255) not null
);

create table status
(
	id int primary key auto_increment,
	name nvarchar(100) not null
);

create table `order`
(
	id int primary key auto_increment,
	status_id int not null,
	order_date datetime not null default current_timestamp,
	delivery_date datetime not null,
	pickup_point_id int not null,
	user_id int not null,
    foreign key(pickup_point_id) references pickup_point(id),
    foreign key(status_id) references status(id),
    foreign key(user_id) references user(id)
);

create table category
(
	id int primary key auto_increment,
	name nvarchar(255) not null
);

create table manufacturer
(
	id int primary key auto_increment,
	name nvarchar(255) not null
);

create table supplier
(
	id int primary key auto_increment,
	name nvarchar(255) not null
);

create table product
(
	id int primary key auto_increment,
	vendor_code nvarchar(255) not null,
	name nvarchar(255) not null,
	description nvarchar(255) not null,
	category_id int not null,
	photo varchar(255) not null,
	manufacturer_id int not null,
	supplier_id int not null,
	price decimal(19,4) not null,
	discount int null,
	max_discount int null,
	amount int not null,
	foreign key(category_id) references category(id),
	foreign key(manufacturer_id) references manufacturer(id),
	foreign key(supplier_id) references supplier(id)
);

create table order_details
(
	id int primary key auto_increment,
	order_id int not null,
	product_id int not null,
    amount int not null,
	foreign key(order_id) references `order`(id),
	foreign key(product_id) references product(id)
);