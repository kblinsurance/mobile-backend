STATE = [('Abia','Abia'),
('Abuja',' Abuja'),
('Adamawa',' Adamawa'),
('Akwa Ibom','Akwa Ibom'),
('Anambra','Anambra'),
('Bauchi','Bauchi'),
('Bayelsa','Bayelsa'),
('Benue','Benue'),
('Borno','Borno'),
('Cross River',' Cross River'),
('Delta','Delta'),
('Ebonyi','Ebonyi'),
('Edo','Edo'),
('Ekiti','Ekiti'),
('Enugu','Enugu'),
('Gombe','Gombe'),
('Imo','Imo'),
('Jigawa','Jigawa'),
('Kaduna','Kaduna'),
('Kano','Kano'),
('Katsina','Katsina'),
('Kebbi','Kebbi'),
('Kogi','Kogi'),
('Kwara','Kwara'),
('Lagos','Lagos'),
('Nasarawa','Nasarawa'),
('Niger','Niger'),
('Ogun','Ogun'),
('Ondo','Ondo'),
('Osun','Osun'),
('Oyo','Oyo'),
('Plateau','Plateau'),
('Rivers','Rivers'),
('Sokoto','Sokoto'),
('Taraba','Taraba'),
('Yobe','Yobe'),
('Zamfara','Zamfara')]


NIN = 'National ID'
DL = 'Drivers License'
INT = 'Int Passport'
VC = 'Voters card'
INC = 'Certificate of Incorporation'
ID_TYPES = [
    (NIN, 'National ID'), (DL, 'Drivers License'),
    (INT, 'Int Passport'), (VC, 'Voters Card'),
    (INC, 'Certificate of Incorporation')
]

MALE = "Male"
FEMALE = "Female"
GENDER = [
    (MALE, 'Male'), (FEMALE, "Female")
]

site_key = '6LeivvQZAAAAAOQTUxCVefO04Kc26Oj8W7DD3lXo'

SECTORS = [
    ('Agriculture','Agriculture'),
    ('Co-operative','Co-operative'), ('Association','Association'),
    ('Construction','Construction'), ('Energy', 'Energy'),
    ('Engineering', 'Engineering'),
    ('Estate', 'Estate'),
    ('Financial Services','Financial Services'),
    ('Foreign Mission/Diplomat','Foreign Mission/Diplomat'),
    ('General Merchant','General Merchant'),
    ('Government','Government'),
    ('Hotels / Hospitality','Hotels / Hospitality'),
    ('Information Technology','Information Technology'),
    ('Insurance','Insurance'),
    ('Logistics','Logistics'),
    ('Manufacturing','Manufacturing'),
    ('Medical','Medical'),
    ('NGO','NGO'),
    ('Oil and Gas','Oil and Gas'),
    ('Power','Power'),
    ('Real Estates','Real Estates'),
    ('Religious Institutions','Religious Institutions'),
    ('Schools','Schools'),
    ('Ship Building / Maintenance','Ship Building / Maintenance'),
    ('SME','SME'),
    ('Supermarkets / Stores','Supermarkets / Stores'),
    ('Telecoms','Telecoms'),
    ('Transportation','Transportation')
]

PRODUCTS = [
    ('Motor Comprehensive', 'Motor Comprehensive'),
    ('Motor Third-Party', 'Motor Third-Party'),
    ('Home Xtra', 'Home Xtra Tenant’s Plan')
]

STATUS = [
    ('Processing','Processing'),
    ('Completed','Completed'),
    ('Cancelled','Cancelled'),
]

PLAN = [
    ('Bronze', 'Bronze'),
    ('Silver', 'Silver'),
    ('Gold', 'Gold'),
]

BUILDING = [
    ('Flat', 'Flat'),
    ('Detached Bungalow', 'Detached Bungalow'),
    ('Terrace Bungalow', 'Terrace Bungalow'),
    ('Detached Duplex', 'Detached Duplex'),
    ('Semi-detached Duplex', 'Semi-detached Duplex'),
    ('Terrace Duplex', 'Terrace Duplex'),
    ('Semi-detached Bungalow', 'Semi-detached Bungalow'),
]

DURATION = [
    ('Half Yearly', 'Half Yearly'),
    ('Quarterly', 'Quarterly'),
    ('Yearly', 'Yearly')
]