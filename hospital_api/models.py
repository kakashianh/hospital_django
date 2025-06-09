from django.db import models
from django.contrib.auth.models import User

# Physician Model
class Physician(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    ssn = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User    

    def __str__(self):
        return self.name

# Department Model
class Department(models.Model):
    department_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    head = models.ForeignKey(Physician, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

    def __str__(self):
        return self.name

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
    ssn = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    insurance_id = models.IntegerField()
    pcp = models.ForeignKey(Physician, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

    def __str__(self):
        return self.name

# Nurse Model
class Nurse(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    registered = models.BooleanField()
    ssn = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

    def __str__(self):
        return self.name

# Appointment Model
class Appointment(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prep_nurse = models.ForeignKey(Nurse, null=True, on_delete=models.SET_NULL)
    physician = models.ForeignKey(Physician, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    examination_room = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Created at timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to User

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
