from django.db import models
from django.db.models.deletion import CASCADE, RESTRICT, SET_NULL

# Create your models here.
class Staduim(models.Model):
    staduim_name  = models.CharField(max_length=200)
    staduim_town  = models.CharField(max_length=200)
    Staduim_image = models.ImageField()
    def __str__(self):
        return self.staduim_name

class Team(models.Model):
    team_name = models.CharField(max_length = 200)
    team_shortname = models.CharField(max_length=3,null=True)
    team_flag = models.ImageField(upload_to = 'media/teams')
    
    class Meta:
        ordering = ['team_name','team_shortname']

    def __str__(self):
        return self.team_shortname  
     

class Match(models.Model):
    match_staduim = models.ForeignKey(Staduim,on_delete=SET_NULL,null=True)
    match_tickets = models.IntegerField()
    match_time    = models.DateTimeField()
    match_round   = models.CharField(max_length=200,null=True)
    home_team = models.ForeignKey(Team,on_delete=SET_NULL,null=True,verbose_name='Home Team', related_name='game')
    away_team = models.ForeignKey(Team,on_delete=SET_NULL,null=True,verbose_name='Away Team')

    def __str__(self):
        return str(self.home_team) + ' vs ' + str(self.away_team)

    
class Tickets(models.Model)	:
    ticket_name     = models.CharField(max_length=200)
    ticket_category = models.CharField(max_length=200)
    ticket_match    = models.ForeignKey(Match ,on_delete= CASCADE)


    def __str__(self):
        return self.ticket_name

class Customer(models.Model):
    customer_first_name = models.CharField(max_length=200)
    customer_last_name  = models.CharField(max_length=200)
    customer_email      = models.EmailField()
    customer_phone      = models.PositiveIntegerField(max_length=9)
    customer_idcard     = models.PositiveIntegerField(max_length=9)

    def __str__(self):
        return self.customer_first_name + '' + self.customer_last_name

class Sales(models.Model):
    sales_name = models.CharField(max_length=200)
    sales_ticket = models.ForeignKey(Tickets,on_delete=RESTRICT)
    sales_customer = models.ForeignKey(Customer,on_delete=RESTRICT)
    sales_date    = models.DateField(null=True)

    def __str__(self):
        return self.sales_name

