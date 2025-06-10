from django.db import models
from django.contrib.auth.models import User

# Physician Model
class Physician(models.Model):
    employee_id = models.IntegerField(primary_key=True, db_column='EmployeeID')
    name = models.CharField(max_length=30, db_column='Name')
    position = models.CharField(max_length=30, db_column='Position')
    ssn = models.IntegerField(db_column='SSN')

    class Meta:
        managed = False
        db_table = 'Physician'

# Department Model
class Department(models.Model):
    department_id = models.IntegerField(primary_key=True, db_column='DepartmentID')
    name = models.CharField(max_length=30, db_column='Name')
    head = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='Head')

    class Meta:
        managed = False
        db_table = 'Department'

# Affiliated_With Model
class AffiliatedWith(models.Model):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='Physician')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='Department')
    primary_affiliation = models.BooleanField(db_column='PrimaryAffiliation')

    class Meta:
        managed = False
        db_table = 'Affiliated_With'
        unique_together = ('physician', 'department')

# Procedures Model
class Procedures(models.Model):
    code = models.IntegerField(primary_key=True, db_column='Code')
    name = models.CharField(max_length=30, db_column='Name')
    cost = models.FloatField(db_column='Cost')

    class Meta:
        managed = False
        db_table = 'Procedures'

# Trained_In Model
class TrainedIn(models.Model):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='Physician')
    treatment = models.ForeignKey(Procedures, on_delete=models.CASCADE, db_column='Treatment')
    certification_date = models.DateTimeField(db_column='CertificationDate')
    certification_expires = models.DateTimeField(db_column='CertificationExpires')

    class Meta:
        managed = False
        db_table = 'Trained_In'
        unique_together = ('physician', 'treatment')

# Patient Model
class Patient(models.Model):
    ssn = models.IntegerField(primary_key=True, db_column='SSN')
    name = models.CharField(max_length=30, db_column='Name')
    address = models.CharField(max_length=30, db_column='Address')
    phone = models.CharField(max_length=30, db_column='Phone')
    insurance_id = models.IntegerField(db_column='InsuranceID')
    pcp = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='PCP')

    class Meta:
        managed = False
        db_table = 'Patient'

# Nurse Model
class Nurse(models.Model):
    employee_id = models.IntegerField(primary_key=True, db_column='EmployeeID')
    name = models.CharField(max_length=30, db_column='Name')
    position = models.CharField(max_length=30, db_column='Position')
    registered = models.BooleanField(db_column='Registered')
    ssn = models.IntegerField(db_column='SSN')

    class Meta:
        managed = False
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
        managed = False
        db_table = 'Appointment'

# Medication Model
class Medication(models.Model):
    code = models.IntegerField(primary_key=True, db_column='Code')
    name = models.CharField(max_length=30, db_column='Name')
    brand = models.CharField(max_length=30, db_column='Brand')
    description = models.CharField(max_length=30, db_column='Description')

    class Meta:
        managed = False
        db_table = 'Medication'

# Prescribes Model
class Prescribes(models.Model):
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='Physician')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='Patient')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, db_column='Medication')
    date = models.DateTimeField(db_column='Date')
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.SET_NULL, db_column='Appointment')
    dose = models.CharField(max_length=30, db_column='Dose')

    class Meta:
        managed = False
        db_table = 'Prescribes'
        unique_together = ('physician', 'patient', 'medication', 'date')

# Block Model
class Block(models.Model):
    block_floor = models.IntegerField(db_column='BlockFloor')
    block_code = models.IntegerField(db_column='BlockCode')

    class Meta:
        managed = False
        db_table = 'Block'
        unique_together = ('block_floor', 'block_code')

# Room Model
class Room(models.Model):
    room_number = models.IntegerField(primary_key=True, db_column='RoomNumber')
    room_type = models.CharField(max_length=30, db_column='RoomType')
    block_floor = models.IntegerField(db_column='BlockFloor')
    block_code = models.IntegerField(db_column='BlockCode')
    unavailable = models.BooleanField(db_column='Unavailable')

    class Meta:
        managed = False
        db_table = 'Room'

# On_Call Model
class OnCall(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, db_column='Nurse')
    block_floor = models.IntegerField(db_column='BlockFloor')
    block_code = models.IntegerField(db_column='BlockCode')
    on_call_start = models.DateTimeField(db_column='OnCallStart')
    on_call_end = models.DateTimeField(db_column='OnCallEnd')

    class Meta:
        managed = False
        db_table = 'On_Call'
        unique_together = ('nurse', 'block_floor', 'block_code', 'on_call_start', 'on_call_end')

# Stay Model
class Stay(models.Model):
    stay_id = models.IntegerField(primary_key=True, db_column='StayID')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='Patient')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, db_column='Room')
    stay_start = models.DateTimeField(db_column='StayStart')
    stay_end = models.DateTimeField(db_column='StayEnd')

    class Meta:
        managed = False
        db_table = 'Stay'

# Undergoes Model
class Undergoes(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='Patient')
    procedures = models.ForeignKey(Procedures, on_delete=models.CASCADE, db_column='Procedures')
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, db_column='Stay')
    date_undergoes = models.DateTimeField(db_column='DateUndergoes')
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE, db_column='Physician')
    assisting_nurse = models.ForeignKey(Nurse, null=True, on_delete=models.SET_NULL, db_column='AssistingNurse')

    class Meta:
        managed = False
        db_table = 'Undergoes'
        unique_together = ('patient', 'procedures', 'stay', 'date_undergoes')
