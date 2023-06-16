from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Sum
from leaderboard.services.leaderboard_caching import get_redis_instance, get_user_key

class Command(BaseCommand):
    help = 'Build the leaderboard in Redis cache'

    def handle(self, *args, **options):
        r = get_redis_instance()
        
        users = User.objects.all()

        for user in users:
            #Get votecount sum
            vote_count_sum = user.guesses.aggregate(Sum('votecount'))['votecount__sum']
            
            vote_count_sum = vote_count_sum or 0
    
            #Get approved guesses which counts for 5 points
            approved_guess_count = user.guesses.filter(approved=True).count()
            
            score = vote_count_sum + (approved_guess_count * 5)

            user_key = get_user_key(user)

            r.zadd('players:score', {user_key: score})

        #print leaderboard
        leaderboard = r.zrevrange('players:score', 0, -1, withscores=True)
        for rank, (username, score) in enumerate(leaderboard, start=1):
            print(f"Rank {rank}: {username.decode()} - Score: {score}")
        