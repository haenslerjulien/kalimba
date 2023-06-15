from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Sum
from redis import Redis

class Command(BaseCommand):
    help = 'Build the leaderboard in Redis cache'

    def handle(self, *args, **options):
        r = Redis(host='redis', port=6379, db=0)
        
        users = User.objects.all()

        for user in users:
            #Get votecount sum
            vote_count_sum = user.guesses.aggregate(Sum('votecount'))['votecount__sum']
            
            vote_count_sum = vote_count_sum or 0
    
            #Get approved guesses which counts for 5 points
            approved_guess_count = user.guesses.filter(approved=True).count()
            
            score = vote_count_sum + (approved_guess_count * 5)

            user_key = f"{user.username}:{user.id}"

            r.zadd('players:score', {user_key: score})

        #print leaderboard
        leaderboard = r.zrevrange('players:score', 0, -1, withscores=True)
        for rank, (username, score) in enumerate(leaderboard, start=1):
            print(f"Rank {rank}: {username.decode()} - Score: {score}")
        