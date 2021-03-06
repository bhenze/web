'''
    Copyright (C) 2017 Gitcoin Core

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from dashboard.models import Bounty
from dashboard.notifications import maybe_post_on_craigslist


class Command(BaseCommand):

    help = 'posts bounties created in provided hours on craigslist'

    def add_arguments(self, parser):
        parser.add_argument('hours', type=int)

    def handle(self, *args, **options):
        hours = options['hours']
        one_hour_back = timezone.now()-timedelta(hours=hours)
        bounties_to_post = Bounty.objects.filter(web3_created__gte=one_hour_back)
        for bounty in bounties_to_post:
            # print(bounty)
            link = maybe_post_on_craigslist(bounty)
            print("Posted {}".format(link))
