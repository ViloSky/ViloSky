""" Models for the ViloSky app. """
from django.db import models
from cuser.models import AbstractCUser


class CustomUser(AbstractCUser):
    """ A model to hold the user entity with a unique email instead of username.
    Otherwise, it contains all other fields that a normal user has (first_name,
    last_name, email, password, etc.)

    Via OneToOne relationship, the model has a single CustomUser it is related to:
        * user_profile = UserProfile that the given user has created.
    """
    middle_names = models.CharField(max_length=100)


class UserProfile(models.Model):
    """ A model to hold the actual user profile related to a user. It also contains
    flags relevant to permissions indicating if the user is an HR rep or a ViloSky
    admin.

    Via ForeignKeys, the model has reverse relationships:
        * qualifications = All qualifications related to a user.
        * paragraphs_created = All paragraphs created by the user. ( When an admin )
        * inputs_created = All inputs created by the user. ( When admin )
        * admin_inputs_created = All admin inputs created by the user. ( When admin )
        * reports_assigned = All reports assigned to the user. Given on user input.
        * sessions_made = All sessions made by the user while logged in.
        * partial_input_created = All partial inputs created by the user.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    is_vilosky_admin = models.BooleanField(default=False)
    is_hr_representative = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    company = models.CharField(max_length=255, blank=True)
    employment_sector = models.CharField(max_length=255, blank=True)
    employment_status = models.CharField(max_length=255, blank=True)
    time_worked_in_industry = models.DurationField(null=True, blank=True)


class Qualification(models.Model):
    """ A model to hold all qualifications related to a user.
    """
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='qualifications')
    level = models.CharField(max_length=255)
    subjects = models.CharField(max_length=255)


class Paragraph(models.Model):
    """ A model to hold paragraphs of text which will form a report.
    Related to the ViloSky admin who has created them.

    Via Foreign keys, the model has reverse relationships:
        * links = Links related to the paragraph
        * keywords = Keywords related to the paragraph
        * actions = Actions related to the paragraph
    Via a Many-to-Many relationship, the model has:
        * reports_included_in = Reports that include this paragraph
    """
    created_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='paragraphs_created')
    static_text = models.TextField()


class Link(models.Model):
    """ A model to hold links, part of each paragraph. """
    paragraph = models.ForeignKey(
        Paragraph, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()


class Keyword(models.Model):
    """ A model to hold keywords, part of each paragraph. """
    paragraph = models.ForeignKey(
        Paragraph, on_delete=models.CASCADE, related_name='keywords')
    key = models.CharField(max_length=255)
    score = models.IntegerField()


class Action(models.Model):
    """ A model to hold static actions, related to a specific paragraph. """
    paragraph = models.ForeignKey(
        Paragraph, on_delete=models.CASCADE, related_name='actions')
    title = models.CharField(max_length=255)


class Report(models.Model):
    """ A model to hold reports consisting of multiple paragraphs.
    Each report is assigned to an individual user.
    """
    paragraphs = models.ManyToManyField(
        Paragraph, related_name='reports_included_in')
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='reports_assigned')
    datetime_created = models.DateTimeField()


class UserAction(models.Model):
    """ A model to hold user actions, all related to an assigned report. 
    As it is for each user, it has a value (changeable by the user).
    """
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name='user_actions')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)


class Session(models.Model):
    """ A model to hold page sessions data. A session may be related to a user
    but it may also not if the actual user is not register or logged in.
    """
    user = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, related_name="sessions_made")
    page = models.CharField(max_length=255)
    time_spent_on_page = models.DurationField()
    clicks_on_page = models.PositiveIntegerField()


class AdminInput(models.Model):
    """ A model to general information for admin inputs. All types of inputs
    may contain different info through inheritance.

    Via ForeignKeys, the model has the reverse relationships:
    * partial_inputs = All partial inputs created for this input.

    Via OneToOne relationship, the model has a single AdminInput of each type
    """
    class AdminInputTypes(models.TextChoices):
        """ A class containing all possible admin input types"""
        DROPDOWN = 'DROPDOWN'
        TEXT = 'TEXT'
        TEXTAREA = 'TEXTAREA'
        CHECKBOX = 'CHECKBOX'

    created_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='admin_inputs_created')
    label = models.CharField(max_length=255)
    input_type = models.CharField(
        max_length=255, choices=AdminInputTypes.choices)
    is_required = models.BooleanField(default=False)


class DropdownAdminInput(AdminInput):
    """ A model to information about dropdown admin inputs."""
    admin_input = models.OneToOneField(
        AdminInput, parent_link=True, on_delete=models.CASCADE)
    # Must be a single array of values in JSON.
    choices = models.JSONField()


class CheckboxAdminInput(AdminInput):
    """ A model to information about checkbox admin inputs."""
    admin_input = models.OneToOneField(
        AdminInput, parent_link=True, on_delete=models.CASCADE)
    default_value = models.BooleanField(default=False)


class TextareaAdminInput(AdminInput):
    """ A model to information about textbox admin inputs."""
    admin_input = models.OneToOneField(
        AdminInput, parent_link=True, on_delete=models.CASCADE)
    max_length = models.PositiveIntegerField(null=True, blank=True)


class TextAdminInput(AdminInput):
    """ A model to information about text admin inputs."""
    admin_input = models.OneToOneField(
        AdminInput, parent_link=True, on_delete=models.CASCADE)
    max_length = models.PositiveIntegerField(null=True, blank=True)


class PartialInput(models.Model):
    """ A model to information about partially filled inputs for each user.
    Contains a value for each user and admininput."""
    created_by = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='partial_input_created')
    admin_input = models.ForeignKey(
        AdminInput, on_delete=models.CASCADE, related_name='partial_inputs')
    value = models.TextField()
