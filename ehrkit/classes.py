"""Class definitions used in ehrkit.py"""
from datetime import date

class Patient:
    """Patient with biographical and medical history data

    Attributes:
        id (int): unique patient ID
        sex (str): patient sex ('M' or 'F')
        dob (datetime): date of birth
        dod (datetime): date of death
        alive (bool): True if patient alive, else False
    """

    def __init__(self, data):
        # Biographical Data:
        if "id" in data:  #int
            self.id = data["id"] #should we use pid in case of conflict with python keyword?
        else:
            self.id = None

        if "sex" in data:
            self.sex = data["sex"]
        else:
            self.sex = None

        if "dob" in data:
            self.dob = data["dob"]
        else:
            self.dob = None

        if "dod" in data:
            self.dod = data["dod"]
        else:
            self.dod = None

        if "alive" in data:
            self.alive = data["alive"]
        else:
            self.alive = None

        ### MEDICAL DATA: ###
        # Current patient diagnoses (Array of diagnosis objects)
        if "diagnosis" in data:
            self.diagnosis = data["diagnosis"]
        else:
            self.diagnosis = None
        # Prescriptions patient is currently taking (Array of prescription objects)
        if "current_prescriptions" in data:
            self.prescriptions = data["current_prescriptions"]
        else:
            self.prescriptions = None
        # Primary care provider (Foreign Key on Provider object):
        if "primary_provider" in data:
            self.primary_provider = data["primary_provider"]
        else:
            self.primary_provider = None
        ### NOTEEVENTS data(list of nltk separated sentences):###
        if "Text" in data:
            self.note_events = data["Text"]
        else:
            self.note_events = None


        ### MEDICAL HISTORY: ###
        # 1.) Past prescriptions (Array of prescription objects)
        if "past_prescriptions" in data:
            self.prescriptHistory = data["past_prescriptions"]
        else:
            self.prescriptHistory = None
        # 2.) Past diagnoses (Array of diagnosis objects)
        if "past_diagnoses" in data:
            self.diagHistory = data["past_diagnoses"]
        else:
            self.diagHistory = None
        # 3) Procedures (Array of procedure objects)
        if "procedures" in data:
            self.procedures = data["procedures"]
        else:
            self.procedures = None
    def addNE(self, textlist):
        """List of all note events for patient, in tuple format (docID, content).
        """
        self.note_events = textlist

    def addPrescriptions(self, textlist):
        self.prescriptions = textlist

    def diagnose(self, disease, start = None, end = None):
        """Adds diagnosis to Patient history:"""
        data = {"name": disease, "id": None, "start": start, "end": end}
        newDiag = Diagnosis(data)
        if not self.diagnosis: self.diagnosis = []
        self.diagnosis.append(newDiag)

    def add_procedure(self, procedure):
        """Adds procedure to Patient history"""
        data = {"name": procedure}
        new_proc = Procedure(data)
        if not self.procedures: self.procedures = []
        self.procedures.append(new_proc)

    def age(self):
        """Compute patient age using birthdate"""
        today = date.today()
        birthdate = self.dob
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


# Disease Object

class Disease:

    def __init__(self, data):
        self.name = data["name"]
        # Foreign key for diagnosis object
        self.id = data["id"]
        # Symptoms — array of strings
        self.symptoms = data["symptoms"]
        self.abbreviation = data["abbreviations"]

# Diagnosis Object
# - Foreign Key on Disease Object

class Diagnosis:

    def __init__(self, data):
        # Foreign key on disease object
        self.name = data["name"]
        # Date of diagnosis
        self.start = data["start"]
        # End date, if patient cured:
        self.end = data["end"]

# Prescription object

class Prescription:

    def __init__(self, data):
        # Generic or Brand Name or Compound Name:
        self.name = data["name"]
        # Is there a standardized drug ID?
        # This is important b/c patient could have
        # been prescribed a generic
        self.id = data["id"]
        #Foreign key on patient object
        self.patient_id = data["patient_id"]
        self.indication = data["indication"]
        # How often medicine is taken:
        self.freq = data["frequency"]
        #Unit of time for frequency (daily, weekly, monthly)
        self.freq = data["frequency_unit"]
        # Numerical quantity of dose — float
        self.dosage = data["dosage"]
        # Units of dosage (e.g. mg, ml, etc.) — str
        self.units = data["dosage_units"]
        self.start = data["start_date"]
        self.end = data["end_date"]
        # Not sure if need to record drug manufacturer — str
        self.manufacturer = data["manufacturer"]
        # Foreign key on Provider() object for prescriber:
        self.prescriber_id = data["prescriber_id"]

    # Length of prescription in days:
    def duration(self):
        if self.start == None and self.end == None:
            return None

        if self.end == None:
            end = date.today()
        else:
            end = self.end

        duration = end - self.start

        return duration.days

# Unsure about this class; is it too generic for our data?

class Procedure:

    def __init__(self, data):
        # Can be a foreign key on charge list,
        # enabling us to capture procedure cost data
        self.name = data["name"]


# Medical facility class:
class Facility:

    def __init__(self, data):
        # Unique facility ID:
        self.id = data["id"]
        self.name = data["name"]
        self.state = data["state"]
        self.city = data["city"]
        self.address = data["address"]
        # For instance "hospital", "out-patient clinic", etc.
        self.type = data["type"]

# Healthcare provider class:
class Provider:

    def __init__(self, data):
        # Unique physician ID:
        self.id = data["id"]
        # Primary facility for physician, foreign key on Facility objects
        self.facility_id = data["facility_id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        # Provider type: RN, EMT, MD, etc.
        self.type = data["type"]
        # Provider title:
        self.title = data["title"]
