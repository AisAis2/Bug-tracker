from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from jiralike.models import User, Project
from ticket.models import Ticket
from django.core.management import BaseCommand

class Command(BaseCommand):
    help = "Creates Groups"
    def handle(self, *args, **kwargs):
        developers_group, created = Group.objects.get_or_create(name = 'Developers')
        watcher_group, created = Group.objects.get_or_create(name = 'Watchers')
        manager_group, created = Group.objects.get_or_create(name = 'Managers')
        # if created: TODO: deal w/ logging
        #     logger.info('developer created')
        ctp = ContentType.objects.get_for_model(Project)
        ctt = ContentType.objects.get_for_model(Ticket)

        perm_p= Permission.objects.filter(content_type = ctp)
        perm_t = Permission.objects.filter(content_type = ctt)
        for p in perm_p:
            if p.codename =='add_project':
                developers_group.permissions.add(p)
                manager_group.permissions.add(p)
            elif p.codename == 'change_project':
                developers_group.permissions.add(p)
                manager_group.permissions.add(p)
            elif p.codename == 'delete_project':
                manager_group.permissions.add(p)
            elif p.codename == 'view_project':
                developers_group.permissions.add(p)
                manager_group.permissions.add(p)
                watcher_group.permissions.add(p)

            for p in perm_t:
                if p.codename =='add_ticket':
                    developers_group.permissions.add(p)
                    manager_group.permissions.add(p)
                elif p.codename == 'change_ticket':
                    developers_group.permissions.add(p)
                    manager_group.permissions.add(p)
                elif p.codename == 'delete_ticket':
                    manager_group.permissions.add(p)
                elif p.codename == 'view_ticket':
                    developers_group.permissions.add(p)
                    manager_group.permissions.add(p)
                    watcher_group.permissions.add(p)
            Almaz = User.objects.get(username = 'Kamila')
            Almaz.groups.add(watcher_group)