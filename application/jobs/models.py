from application import db
from sqlalchemy.sql import text
from application.models import Base

user_jobs = db.Table('userjobs',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'))
)

class Job(Base):
    name = db.Column(db.String(144), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    intrest_user = db.relationship('User', secondary = user_jobs, backref= db.backref('interested'), lazy=True)
    question = db.relationship("Question", backref="job",lazy=True)
    def __init__(self, name,salary,description,account_id):
        self.name = name
        self.salary =salary
        self.description = description
        self.active = False
        self.account_id = account_id
    @staticmethod

    def interested_jobs(accountID):

        stmt = text("SELECT Job.id, Job.name, Job.salary,Job.description, CASE WHEN Job.id IN (SELECT UJ.job_id FROM Account A LEFT JOIN userjobs UJ on A.id = UJ.account_id WHERE UJ.account_id = :accountID)"
        " THEN 'Interested' ELSE 'Not interested' END, Job.account_id FROM Job").params(accountID = accountID)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0],"name":row[1],"salary":row[2],"description":row[3],"interested":row[4], "account_id":row[5]})

        return response

    @staticmethod
    def my_interested_jobs(accountID):
        stmt = text("SELECT Account.username FROM Account")
      
    
    @staticmethod
    def jobs_offers():
        stmt = text("SELECT COUNT(job.id) FROM Job")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"count":row[0]})
        
        return response
    

    @staticmethod
    def job_author(accountID):
       #stmt = text("SELECT A.username from account A WHERE A.id = (SELECT account_id FROM Job WHERE A.id = :accountID)").params(accountID = accountID)
        stmt = text("SELECT A.username FROM Account A, Job j WHERE j.id = :accountID AND J.account_id = :accountID").params(accountID = accountID)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"author":row[0]})
        
        return response

    @staticmethod
    def jobs_listed(jobID):
        stmt = text("SELECT * FROM Account A, Job J WHERE A.id = 1 AND J.account_id = A.id;")

    # SELECT * FROM Account A, Job J WHERE A.id = 1 AND J.account_id = A.id;
    #SELECT A.id from account A WHERE A.id = (SELECT account_id FROM Job WHERE A.id == account_id);
   # SELECT A.username FROM Account A WHERE account_id = 1;
    #SELECT A.username FROM Account A, Job j WHERE A.id = 2 AND J.account_id = 2;
    #SELECT A.username FROM Account A, Job j WHERE j.id = 1 AND J.account_id = 1