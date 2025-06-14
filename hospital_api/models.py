from django.db import models
from django.contrib.auth.models import User

# Physician Model
class Physician(models.Model):
    employee_id = models.IntegerField(primary_key=True, db_column='EmployeeID')
    name = models.CharField(max_length=30, db_column='Name')
    position = models.CharField(max_length=30, db_column='Position')
    ssn = models.IntegerField(db_column='SSN')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Physician'

# Department Model
class Department(models.Model):
    department_id = models.IntegerField(primary_key=True, db_column='DepartmentID')
    name = models.CharField(max_length=30, db_column='Name')
    head = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='Head')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Department'

# Affiliated_With Model (Many-to-Many relationship between Physician and Department)
class AffiliatedWith(models.Model):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    primary_affiliation = models.BooleanField()

    class Meta:
        unique_together = ('physician', 'department')

# Procedures Model
class Procedures(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

    def __str__(self):
        return self.name

# Trained_In Model (Many-to-Many relationship between Physician and Procedures)
class TrainedIn(models.Model):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Procedures, on_delete=models.CASCADE)
    certification_date = models.DateTimeField()
    certification_expires = models.DateTimeField()

    class Meta:
        unique_together = ('physician', 'treatment')

# Patient Model
class Patient(models.Model):
    ssn = models.IntegerField(primary_key=True, db_column='SSN')
    name = models.CharField(max_length=30, db_column='Name')
    address = models.CharField(max_length=30, db_column='Address')
    phone = models.CharField(max_length=30, db_column='Phone')
    insurance_id = models.IntegerField(db_column='InsuranceID')
    pcp = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='PCP')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Patient'

# Nurse Model
class Nurse(models.Model):
    employee_id = models.IntegerField(primary_key=True, db_column='EmployeeID')
    name = models.CharField(max_length=30, db_column='Name')
    position = models.CharField(max_length=30, db_column='Position')
    registered = models.BooleanField(db_column='Registered')
    ssn = models.IntegerField(db_column='SSN')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Nurse'
# Appointment Model
class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True, db_column='AppointmentID')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='Patient')
    prep_nurse = models.ForeignKey(Nurse, null=True, on_delete=models.SET_NULL, db_column='PrepNurse')
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='Physician')
    start_time = models.DateTimeField(db_column='Starto')
    end_time = models.DateTimeField(db_column='Endo')
    examination_room = models.TextField(db_column='ExaminationRoom')

    class Meta:
        db_table = 'Appointment'

# Medication Model
class Medication(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

    def __str__(self):
        return self.name

# Prescribes Model (Many-to-Many relationship between Physician, Patient, and Medication)
class Prescribes(models.Model):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    date = models.DateTimeField()
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET_NULL)
    dose = models.CharField(max_length=30)

    class Meta:
        unique_together = ('physician', 'patient', 'medication', 'date')

# Block Model
class Block(models.Model):
    block_floor = models.IntegerField()
    block_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

    class Meta:
        unique_together = ('block_floor', 'block_code')

# Room Model
class Room(models.Model):
    room_number = models.IntegerField(primary_key=True)
    room_type = models.CharField(max_length=30)
    block_floor = models.IntegerField()
    block_code = models.IntegerField()
    unavailable = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

    class Meta:
        unique_together = ('block_floor', 'block_code')

# On_Call Model (Many-to-Many relationship between Nurse and Block)
class OnCall(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    block_floor = models.IntegerField()
    block_code = models.IntegerField()
    on_call_start = models.DateTimeField()
    on_call_end = models.DateTimeField()

    class Meta:
        unique_together = ('nurse', 'block_floor', 'block_code', 'on_call_start', 'on_call_end')

# Stay Model
class Stay(models.Model):
    stay_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    stay_start = models.DateTimeField()
    stay_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

# Undergoes Model (Many-to-Many relationship between Patient, Procedures, Stay)
class Undergoes(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    procedures = models.ForeignKey(Procedures, on_delete=models.CASCADE)
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE)
    date_undergoes = models.DateTimeField()
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    assisting_nurse = models.ForeignKey(Nurse, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('patient', 'procedures', 'stay', 'date_undergoes')
