CREATE TABLE contact_info (
    national_id INTEGER PRIMARY KEY,
    address_country TEXT,
    address_zip_code TEXT,
    address_city TEXT,
	address_street TEXT,
	address_house_number INTEGER,
	phone_country_code TEXT,
	phone_number INTEGER
	);
	
	INSERT INTO contact_info VALUES
(1, 'Denmark',	'8800',	'Viborg',	'Solvang',	2,	'+45',	465189064),
(2, 'Finland',	'99800',	'Ivalo',	'Teknikontie',	34,	'+358',	129984022),
(3, 'Norway',	'7010',	'Trondheim',	'Skolevegen',	4,	'+47',	432189031),
(4, 'Sweden',	'98130',	'Kiruna',	'Enbergsgatan',	74,	'+46',	654890242),
(5, 'Finland',	'0150',	'Helsinki',	'Ilmailutie',	253,	'+358',	646874690),
(6, 'Finland',	'90120',	'Oulu',	'Parkkitie',	71,	'+358',	767486786),
(7, 'Denmark',	'2630',	'Taastrup',	'Jovavej',	3,	'+45',	789746518),
(8, 'Denmark',	'8600',	'Silkeborg',	'Brandorffsvej',	65,	'+45',	789998733),
(9, 'Norway',	'0010',	'Oslo',	'Kirkevegen',	453, '+47',	468767836);