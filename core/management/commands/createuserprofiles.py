from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import Profile

class Command(BaseCommand):
    help = 'Create Profiles for Users who do not currently have a Profile'

    def handle(self, *args, **options):

        def get_users_without_profiles():
            userIDsWithProfiles = [profile.user_id for profile in Profile.objects.all()]
            return User.objects.exclude(id__in=userIDsWithProfiles)
        
        usersWop = get_users_without_profiles()
        if len(usersWop) == 0:
            self.stdout.write('All Users already have Profiles. Canceling')
            return
        self.stdout.write('Found users without profiles:')
        self.stdout.write(str(usersWop))
        self.stdout.write('Continue? (Y/n)')
        if input() != 'Y':
            self.stdout.write('Canceling')
            return
        for user in usersWop:
            Profile.objects.create(user=user)
        self.stdout.write('Done')
        usersWop = get_users_without_profiles()
        if len(usersWop) == 0:
            self.stdout.write('Sucess! all Users now have Profiles')
        else:
            self.stdout.write('Error! the following Users still lack Profiles:')
            self.stdout.write(str(usersWop))