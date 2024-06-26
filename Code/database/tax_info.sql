CREATE TABLE tax_info (
 national_id INTEGER,
 marital_status TEXT,
 tax_rate INTEGER,
 yearly_income INTEGER,
 advance_tax INTEGER,
 tax_paid_this_year INTEGER,
 property_value INTEGER,
 loans INTEGER,
 property_tax INTEGER
);

INSERT INTO tax_info VALUES
(1, 'married',	34,	400000,	NULL, 108800,	600000,	400000,	18000),
(2, 'single',	26,	300000,	NULL, 62400,	NULL,	NULL,	NULL),
(3, 'married',	8,	50000,	NULL, 3200, NULL,	NULL,	NULL),		
(4, 'single',	15,	100000,	NULL, 12000,	NULL,	NULL,	NULL),		
(5, 'married',	50,	1000000,	60000,	400000,	1500000,	2000000,	45000),
(6, 'married',	13,	95000,	NULL, 9880,	NULL,	NULL,	NULL),
(7, 'single',	45,	900000,	55000,	324000,	1000000,	900000,	30000),
(8, 'single',	33,	380000,	NULL, 100320, NULL,	NULL,	NULL),
(9, 'married',	20,	150000,	NULL, 24000,	NULL,	NULL,	NULL);		