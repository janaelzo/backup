from itertools import combinations_with_replacement
from os import name
from myproject import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    role = db.Column(db.String(50))
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    versions = db.relationship('EDS', backref = 'user', lazy = True)

    # posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self, fname, lname, contact, role, email, username, password):
        self.fname = fname
        self.lname = lname
        self.contact = contact
        self.role = role
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"

class EDS(db.Model,UserMixin):
    
    __tablename__ = 'eds'

    id = db.Column( db.Integer,primary_key=True)
    eds_type = db.Column(db.String(50))
    project_name = db.Column(db.String(80))
    authorized_by = db.Column(db.String(80))
    planner = db.Column(db.String(80))
    team = db.Column(db.String(80))
    contributors = db.Column(db.String(80))
    supporters = db.Column(db.String(80))
    oracle = db.Column(db.String(80))
    rpats = db.Column(db.String(80))
    checked_by = db.Column(db.String(80))
    ca_name = db.Column(db.String(80))
    ca_number = db.Column(db.String(80))
    coord_name = db.Column(db.String(80))
    coord_team = db.Column(db.String(80))
    coord_number = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    priority = db.Column(db.String(80))
    team = db.Column(db.String(80))
    status = db.Column(db.String(80))
    release_date = db.Column(db.String(80))
    target_date = db.Column(db.String(80))
    revision = db.Column(db.String(80))


    # posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self, eds_type, project_name, authorized_by, planner, team, contributors, supporters, oracle,
                 rpats, priority, status, release_date, target_date, revision, revision_date, checked_by,
                   ca_name, ca_number, user_id ):
        self.eds_type = eds_type
        self.project_name = project_name
        self.authorized_by = authorized_by
        self.planner = planner
        self.team = team
        self.contributors = contributors
        self.supporters = supporters
        self.oracle = oracle
        self.rpats = rpats
        self.priority = priority
        self.status = status
        self.release_date = release_date
        self.target_date = target_date
        self.revision = revision
        self.revision_date = revision_date
        self.checked_by = checked_by
        self.ca_name = ca_name
        self.ca_number = ca_number
        self.user_id = user_id
 
    def __repr__(self):
           return f"EDS {self.project_name}"

class EDSTPIA_AEupdate(db.Model,UserMixin):
    
    __tablename__ = 'TPIA_AEupdate'

    id = db.Column( db.Integer,primary_key=True)
    client = db.Column(db.String(80))
    request_code = db.Column(db.String(80))
    overview = db.Column(db.String(80))
    cili = db.Column(db.String(80))
    address = db.Column(db.String(80))
    regions = db.Column(db.String(80))
    site = db.Column(db.String(80))
    router = db.Column(db.String(80))
    platform = db.Column(db.String(80))
    aeid = db.Column(db.String(80))
    port = db.Column(db.String(80))
    port_new = db.Column(db.String(80))
    old_mb = db.Column(db.String(80))
    new_mb = db.Column(db.String(80))
    new_gig = db.Column(db.String(80))
    phys_links = db.Column(db.String(80))
    dependancy = db.Column(db.String(80))
    # burst_limit = db.Column(db.String(80))
    # bandwidth_per_link = db.Column(db.String(80))
    eds_id = db.Column(db.Integer, db.ForeignKey('eds.id'))


    # posts = db.relationship('BlogPost',backref='author',lazy=True)

    def __init__(self, regions, cili,  port, dependancy, phys_links, new_gig, port_new, new_mb, aeid, old_mb, router, platform, client, site, overview, bandwith_per_link, address, request_code, burst_limit, eds_id ):
        self.client = client
        self.request_code = request_code
        self.overview = overview
        self.cili = cili
        self.address = address
        self.regions = regions
        self.site = site
        self.router = router
        self.platform = platform
        self.aeid = aeid
        self.port = port 
        self.port_new = port_new
        self.old_mb = old_mb
        self.new_mb = new_mb
        self.new_gig = new_gig
        self.phys_links = phys_links
        self.dependancy = dependancy
        # self.bandwith_per_link = bandwith_per_link
        # self.burst_limit = burst_limit
        self.eds_id = eds_id
 
    def __repr__(self):
           return f"TPIA_AEupdate{self.site}"

