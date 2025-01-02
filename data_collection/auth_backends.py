from django.contrib.auth.backends import BaseBackend
from .models import Monitor, Member
from django.contrib.auth import get_user_model

class MonitorBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            monitor = Monitor.objects.get(email=email)
            if monitor.check_password(password):
                return monitor
        except Monitor.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Monitor.objects.get(pk=user_id)
        except Monitor.DoesNotExist:
            return None


class AgentCodeBackend(BaseBackend):
    def authenticate(self, request, agent_code=None, password=None):
        try:
            # Authenticate using the custom Member model
            member = Member.objects.get(agent_code=agent_code)
            if member.check_password(password):
                return member
        except Member.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None
