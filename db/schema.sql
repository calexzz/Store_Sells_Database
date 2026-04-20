CREATE TABLE IF NOT EXISTS `categories` (
	`id_category` integer primary key NOT NULL UNIQUE,
	`name_of_category` TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `products` (
	`id_product` integer primary key NOT NULL UNIQUE,
	`name_of_product` TEXT NOT NULL,
	`price` REAL NOT NULL,
	`id_category` INTEGER NOT NULL,
	`quantity_at_storage` REAL NOT NULL,
FOREIGN KEY(`id_category`) REFERENCES `categories`(`id_category`)
);

CREATE TABLE IF NOT EXISTS `sale_items` (
	`id_sale` integer primary key NOT NULL UNIQUE,
	`id_check` INTEGER NOT NULL,
	`id_product` INTEGER NOT NULL,
	`quantity` REAL NOT NULL,
FOREIGN KEY(`id_check`) REFERENCES `receipt`(`id_check`),
FOREIGN KEY(`id_product`) REFERENCES `products`(`id_product`)
);

CREATE TABLE IF NOT EXISTS `receipt` (
	`id_check` integer primary key NOT NULL UNIQUE,
	`created_at` REAL NOT NULL,
	`id_cashier` INTEGER NOT NULL,
FOREIGN KEY(`id_cashier`) REFERENCES `employers`(`id`)
);

CREATE TABLE IF NOT EXISTS `employers` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
	`surname` TEXT NOT NULL,
	`id_job_titile` INTEGER NOT NULL,
FOREIGN KEY(`id_job_titile`) REFERENCES `job_titles`(`id`)
);

CREATE TABLE IF NOT EXISTS `job_titles` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL
);