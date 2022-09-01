from django.contrib.auth.mixins import UserPassesTestMixin

class StaffMixing(UserPassesTestMixin):
    """
    Lo scopo di questo mixing è fare ciò che solo
    lo staff possa creare sezioni
    """

    def test_func(self):
        return self.request.user.is_staff