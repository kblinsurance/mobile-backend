# Generated by Django 3.1.3 on 2021-02-08 13:26

import ckeditor.fields
import cloudinary_storage.storage
import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import kbl.models.claim
import kbl.models.policy


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('phone', models.CharField(max_length=50, unique=True)),
                ('address', models.CharField(blank=True, max_length=254, null=True, verbose_name='Contact Address')),
                ('state', models.CharField(blank=True, choices=[('Abia', 'Abia'), ('Abuja', ' Abuja'), ('Adamawa', ' Adamawa'), ('Akwa Ibom', 'Akwa Ibom'), ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', ' Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara')], max_length=50, null=True)),
                ('is_corporate', models.BooleanField(help_text='Select if corporate', null=True, verbose_name='Corporate organization')),
                ('is_individual', models.BooleanField(help_text='Select if individual', null=True, verbose_name='Individual')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=50, verbose_name='Region')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('tel_one', models.CharField(max_length=15, verbose_name='Telphone 1')),
                ('tel_two', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telephone 2')),
                ('last_modified', models.DateField(auto_now_add=True, verbose_name='Last Modified')),
            ],
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_number', models.CharField(default=kbl.models.claim.get_clm_num, max_length=50, verbose_name='Claim Number')),
                ('accident_date', models.DateField(verbose_name='Date of Accident/loss')),
                ('accident_time', models.TimeField(verbose_name='Time of Accident/loss')),
                ('accident_place', models.CharField(blank=True, max_length=255, null=True, verbose_name='Place of Accident/loss')),
                ('desc', models.TextField(help_text='Please describe how the loss occurred', verbose_name='Description')),
                ('damage_desc', models.TextField(blank=True, help_text='Describe extent of direct damage resulting from the accident', null=True, verbose_name='Damage Description')),
                ('est_cost', models.FloatField(help_text='Estimated cost of repair', verbose_name='Estimate')),
                ('police_report', models.TextField(blank=True, null=True, verbose_name='Policy Report')),
                ('other_policy', models.TextField(blank=True, help_text='Please give details of any other insurance cover on the vehicle', null=True, verbose_name='Other Insurance')),
                ('witness_name', models.CharField(max_length=255, verbose_name='Witness Name')),
                ('witness_address', models.CharField(max_length=255, verbose_name='Witness Address')),
                ('witness_signature', models.ImageField(help_text='Upload image of Signature', upload_to='signature', verbose_name='Witness Signature')),
                ('witness_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('status', models.CharField(choices=[('Processing', 'Processing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Processing', max_length=50, verbose_name='Status')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created At')),
                ('last_modified', models.DateTimeField(auto_now_add=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name_plural': 'Claims',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InsuredOfficer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['officer'],
            },
        ),
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy', models.CharField(max_length=255, verbose_name='Policy')),
                ('ref_num', models.CharField(max_length=255, verbose_name='Reference Code')),
                ('platform', models.CharField(choices=[('Flutterwave', 'Flutterwave'), ('QuickTeller', 'QuickTeller')], max_length=255, verbose_name='Payment Gateway')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Time of Payment')),
            ],
            options={
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('policy_number', models.CharField(default=kbl.models.policy.get_pol_num, max_length=255, verbose_name='Policy Number')),
                ('premium', models.FloatField(help_text='Leave blank! Auto calculated on save.', verbose_name='Premium')),
                ('value', models.FloatField(help_text='market cost of item', null=True, verbose_name='Value')),
                ('front_image', models.ImageField(help_text='Front image of property', max_length=255, null=True, upload_to='policy', verbose_name='Front Image')),
                ('back_image', models.ImageField(help_text='Back image of property', max_length=255, null=True, upload_to='policy', verbose_name='Back Image')),
                ('valid_till', models.DateTimeField(null=True, verbose_name='Valid Till')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created At')),
                ('last_modified', models.DateTimeField(auto_now_add=True, verbose_name='Last Modified')),
            ],
            options={
                'verbose_name_plural': 'All Policies',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PolicyCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='Count')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Motor Comprehensive', 'Motor Comprehensive'), ('Motor Third-Party', 'Motor Third-Party'), ('Home Xtra', 'Home Xtra Tenant’s Plan')], max_length=255, verbose_name='Name')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('featured_image', models.ImageField(blank=True, help_text='Product Featured Image', null=True, upload_to='products/images', verbose_name='Upload Image')),
                ('mobile_icon', models.ImageField(blank=True, help_text='Icon Image for mobile app', null=True, upload_to='products/icons', verbose_name='Mobile_icon')),
                ('on_mobile', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text='Is it purchasable on the mobile app', verbose_name='On mobile?')),
                ('purchase_link', models.CharField(blank=True, help_text='link to purchase policy', max_length=50, null=True, verbose_name='Link')),
                ('category', models.CharField(choices=[('Motor', 'Motor'), ('Home', 'Home')], default='Home', help_text='Product Category', max_length=50, verbose_name='Category')),
                ('icon', models.CharField(blank=True, max_length=50, null=True, verbose_name='Mobile Icon')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
            ],
        ),
        migrations.CreateModel(
            name='HomeXtra',
            fields=[
                ('policy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kbl.policy')),
                ('plan', models.CharField(choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold')], default='Gold', max_length=50, verbose_name='Plan')),
                ('building_type', models.CharField(choices=[('Flat', 'Flat'), ('Detached Bungalow', 'Detached Bungalow'), ('Terrace Bungalow', 'Terrace Bungalow'), ('Detached Duplex', 'Detached Duplex'), ('Semi-detached Duplex', 'Semi-detached Duplex'), ('Terrace Duplex', 'Terrace Duplex'), ('Semi-detached Bungalow', 'Semi-detached Bungalow')], default='Detached Duplex', max_length=50, verbose_name='Type of Building')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
            ],
            bases=('kbl.policy',),
        ),
        migrations.CreateModel(
            name='InsuredProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='kbl.user')),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('origin_state', models.CharField(blank=True, choices=[('Abia', 'Abia'), ('Abuja', ' Abuja'), ('Adamawa', ' Adamawa'), ('Akwa Ibom', 'Akwa Ibom'), ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', ' Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara')], max_length=50, null=True, verbose_name='State of Origin')),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('bvn', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='MotorClaim',
            fields=[
                ('claim_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kbl.claim')),
                ('driver', models.CharField(help_text='Person Driving at the time of accident', max_length=50, verbose_name='Driver')),
                ('driver_phone', models.CharField(max_length=15, verbose_name="Driver's Phone")),
                ('driver_licence', models.CharField(help_text='Licence Number', max_length=50, verbose_name="Driver's Licence")),
                ('licence_date_issued', models.DateField(verbose_name='Date Issed')),
                ('licence_date_expired', models.DateField(verbose_name='Expiry Date')),
                ('present_in_vehicle', models.BooleanField(verbose_name='Were you in the vehicle?')),
                ('current_location', models.CharField(help_text='Where can we inspect the vehicle?', max_length=50, verbose_name='Location of vehicle')),
                ('cause_by_tp', models.BooleanField(verbose_name='Caused By Third Party?')),
                ('tp_name', models.CharField(max_length=50, verbose_name='Name')),
                ('tp_phone', models.CharField(max_length=15, verbose_name='Phone')),
                ('tp_address', models.CharField(max_length=255, verbose_name='Address')),
                ('damage_prop_live', models.TextField(verbose_name='Damaged Livestock/Property')),
            ],
            options={
                'verbose_name_plural': 'Motor Claims',
                'abstract': False,
            },
            bases=('kbl.claim',),
        ),
        migrations.CreateModel(
            name='MotorComprehensivePolicy',
            fields=[
                ('policy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kbl.policy')),
                ('rate', models.FloatField(help_text='Rate applied on Item Value', verbose_name='Rate')),
                ('registration_number', models.CharField(max_length=50, verbose_name='Registration Number')),
                ('engine_number', models.CharField(max_length=50, verbose_name='Engine Number')),
                ('chasis_number', models.CharField(max_length=50, verbose_name='Chasis Number')),
                ('vehicle_class', models.CharField(choices=[('Commercial', 'Commercial'), ('Company, Taxi, Car Hire', 'Company, Taxi, Car Hire'), ('Stage Carriage 8 - 15 persons', 'Stage Carriage 8 - 15 persons'), ('Stage Carriage over 15 persons', 'Stage Carriage over 15 persons'), ('Buses, Omnibus', 'Buses, Omnibus'), ('Motorcycle/Tricycle', 'Motorcycle/Tricycle'), ('Tractor & Equipment', 'Tractor & Equipment'), ('Private Vehicle / Car', 'Private Vehicle / Car')], max_length=50, verbose_name='Vehicle Class')),
                ('vehicle_model', models.CharField(blank=True, help_text='Format Vehicle model', max_length=50, null=True, verbose_name='Vehicle Model')),
                ('vehicle_make', models.CharField(blank=True, help_text='Format vehicle_name vehicle make', max_length=50, null=True, verbose_name='Vehicle Make')),
                ('vehicle_year', models.CharField(blank=True, help_text='Format vehicle_name vehicle model year', max_length=50, null=True, verbose_name='Vehicle Year')),
                ('vehicle_license', models.ImageField(max_length=255, null=True, upload_to='licenses', verbose_name='Vehicle License')),
                ('proof_of_ownership', models.ImageField(max_length=255, null=True, upload_to='pow', verbose_name='Proof of ownership')),
            ],
            options={
                'verbose_name_plural': 'Motor Comprehensive polices',
            },
            bases=('kbl.policy',),
        ),
        migrations.CreateModel(
            name='MotorThirdPartyPolicy',
            fields=[
                ('policy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kbl.policy')),
                ('registration_number', models.CharField(max_length=50, verbose_name='Registration Number')),
                ('engine_number', models.CharField(max_length=50, verbose_name='Engine Number')),
                ('chasis_number', models.CharField(max_length=50, verbose_name='Chasis Number')),
                ('vehicle_class', models.CharField(choices=[('Commercial', 'Commercial'), ('Company, Taxi, Car Hire', 'Company, Taxi, Car Hire'), ('Stage Carriage 8 - 15 persons', 'Stage Carriage 8 - 15 persons'), ('Stage Carriage over 15 persons', 'Stage Carriage over 15 persons'), ('Buses, Omnibus', 'Buses, Omnibus'), ('Motorcycle/Tricycle', 'Motorcycle/Tricycle'), ('Tractor & Equipment', 'Tractor & Equipment'), ('Private Vehicle / Car', 'Private Vehicle / Car')], max_length=50, verbose_name='Vehicle Class')),
                ('vehicle_model', models.CharField(blank=True, help_text='Format Vehicle model', max_length=50, null=True, verbose_name='Vehicle Model')),
                ('vehicle_make', models.CharField(blank=True, help_text='Format vehicle_name vehicle make', max_length=50, null=True, verbose_name='Vehicle Make')),
                ('vehicle_year', models.CharField(blank=True, help_text='Format vehicle_name vehicle model year', max_length=50, null=True, verbose_name='Vehicle Year')),
                ('vehicle_license', models.ImageField(max_length=255, null=True, upload_to='licenses', verbose_name='Vehicle License')),
                ('proof_of_ownership', models.ImageField(max_length=255, null=True, upload_to='pow', verbose_name='Proof of ownership')),
            ],
            options={
                'verbose_name_plural': 'Motor Third-Party polices',
            },
            bases=('kbl.policy',),
        ),
        migrations.CreateModel(
            name='PushNotificationToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, verbose_name='Push Token')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=50, verbose_name='Option')),
                ('amount', models.FloatField(help_text='Enter rate between 0.0 - 1.0 or Fixed amount', verbose_name='Amount/Rate')),
                ('type', models.CharField(choices=[('Rate', 'Rate'), ('Fixed', 'fixed')], help_text='Fixed amount or rate', max_length=50, verbose_name='Type')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Created At')),
                ('last_modified', models.DateTimeField(auto_now_add=True, verbose_name='Last Modified')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbl.product', verbose_name='Product')),
            ],
        ),
        migrations.AddField(
            model_name='policy',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='kbl.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='policy',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='claim',
            name='policy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kbl.policy', verbose_name='Policy'),
        ),
        migrations.AddField(
            model_name='claim',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.FileField(help_text='Downloadable as PDF', storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='certificate', verbose_name='Certificate')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate', to='kbl.policy', verbose_name='Policy')),
            ],
        ),
        migrations.CreateModel(
            name='OfficerProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='officer', serialize=False, to='kbl.user')),
                ('branch', models.CharField(blank=True, max_length=50, null=True)),
                ('accounts', models.ManyToManyField(through='kbl.InsuredOfficer', to='kbl.InsuredProfile', verbose_name='List of Account under officer')),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255, verbose_name='Item')),
                ('value', models.FloatField(verbose_name='Value')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='kbl.homextra', verbose_name='Policy')),
            ],
        ),
        migrations.AddField(
            model_name='insuredofficer',
            name='insured',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbl.insuredprofile', verbose_name='Insured'),
        ),
        migrations.AddField(
            model_name='insuredofficer',
            name='officer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbl.officerprofile', verbose_name='Officer'),
        ),
        migrations.CreateModel(
            name='Injured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('injury', models.CharField(max_length=255, verbose_name='Nature of injuries')),
                ('is_passenger', models.CharField(max_length=255, verbose_name='Passenger')),
                ('in_hospital', models.CharField(blank=True, max_length=255, null=True, verbose_name='In Hospital')),
                ('hospital_detail', models.CharField(blank=True, max_length=1025, null=True, verbose_name='Hostipal Details')),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='injureds', to='kbl.motorclaim', verbose_name='Claim')),
            ],
        ),
        migrations.CreateModel(
            name='Identification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('National ID', 'National ID'), ('Drivers License', 'Drivers License'), ('Int Passport', 'Int Passport'), ('Voters card', 'Voters Card')], max_length=50)),
                ('id_number', models.BigIntegerField()),
                ('image', models.ImageField(help_text='upload a clear picture of your ID', upload_to='static/identifications/')),
                ('date_issued', models.DateField()),
                ('expiry_date', models.DateField()),
                ('insured', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kbl.insuredprofile', verbose_name='Valid ID')),
            ],
        ),
    ]