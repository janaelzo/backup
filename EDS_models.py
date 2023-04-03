from __future__ import print_function
from mailmerge import MailMerge
import pandas as pd
from myproject.models import EDSTPIA_AEupdate, EDS
from flask_login import login_user, current_user, logout_user, login_required
from myproject import db
from flask import  flash

####################Safe Capture##################
def get_data_from_html(req_EDS,tag):
    data_to_give = ''
    try:
        data_to_give = req_EDS[tag]
    except:
        data_to_give = 'N/A'
    return data_to_give


#####################Send data to database####################
def send_data(req_EDS):

    eds_record = EDS(eds_type = req_EDS['eds'],
                     project_name = req_EDS['Project_Name'],
                     authorized_by = req_EDS['Project_Manager'],
                     planner = req_EDS['Planner_Name'],
                     team = req_EDS['Team_Name'],
                     contributors = req_EDS['Contributors'],
                     supporters = req_EDS['Supporters'],
                     checked_by = req_EDS['Checked_By'],
                     ca_name = req_EDS['CA_Name'],
                     ca_number = req_EDS['CA_Number'],
                     coord_name = req_EDS['Coordinator_Name'],
                     coord_team = req_EDS['Coordinatior Team'],
                     coord_number = req_EDS['Coordinatior Number'],
                     oracle = req_EDS['Oracle'],
                     rpats = req_EDS['Rpats'],
                     priority = req_EDS['Project_Priority'],
                     status = req_EDS['Status_s'],
                     release_date = req_EDS['R_Date'],
                     target_date = req_EDS['TS_Date'],
                     revision = req_EDS['Revision_Number'],
                     revision_date = req_EDS['Revision_Date'],
                     user_id=current_user.id,
                      )                   
    db.create_all()
    db.session.add(eds_record)
    db.session.commit()
    db.session.refresh(eds_record)

    eds_id = eds_record.id
####################  TPIA BW Update  ####################
    if req_EDS['eds'] == 'TPIA - AE Bandwidth Update':
        edsTPIA_AEupdate_record = EDSTPIA_AEupdate(
                    client = req_EDS['Client'],
                    request_code = req_EDS['Request'],
                    overview = req_EDS['Overview'],
                    cili = req_EDS['cili'],
                    address = req_EDS['Address'],
                    regions = req_EDS['Region'],
                    site = req_EDS['Site'],
                    router = req_EDS['Router'],
                    platform = req_EDS['Platform'],
                    aeid = req_EDS['AEID'],
                    port = req_EDS['Port'],
                    port_new = req_EDS['Port_New'],
                    old_mb = req_EDS['Old_MB'],
                    new_mb = req_EDS['New_MB'],
                    new_gig = req_EDS['New_Gig'],
                    phys_links = req_EDS['Phys_Links'],
                    dependancy = req_EDS['Dependancy'],
                    # bandwith_per_link = req_EDS['BW_Calc'],
                    # burst_limit = req_EDS['Burst_Calc'],
                    eds_id=eds_id,
                    )
        db.create_all()
        db.session.add(edsTPIA_AEupdate_record)
        db.session.commit()
    flash('Your version was saved!')

################## Generate TPIA AE Bandwidth Update  ####################
def generate_TPIA_AEupdate(req_EDS, template):

    document = MailMerge(template)
    document.merge(
        Client = req_EDS['client'],
        Request = req_EDS['Request'],
        Overview = req_EDS['Overview'],
        CILI = req_EDS['cili'],
        Address = req_EDS['address'],
        Region = req_EDS['regions'],
        Site = req_EDS['site'],
        Router = req_EDS['router'],
        Platform = req_EDS['platform'],
        AEID = req_EDS['aeid'],
        Port = req_EDS['port'],
        PortNew = req_EDS['Port_New'],
        OldMB = req_EDS['Old_MB'],
        NewMB = req_EDS['New_MB'],
        NewGig = req_EDS['New_Gig'],
        Links = req_EDS['Phys_Links'],
        DDescrip = req_EDS['Dependancy'],
#             # BurstCalc = 
#             # BWCalc = 
        )
    return document 

#####################Generate EDS####################
def generate_EDS(req_EDS):

    if req_EDS['eds'] == 'TPIA - AE Bandwidth Update': 
        template = '../EDS-Automation-TPIA/EDS_TPIA_AEupdate.docx'
        document = generate_TPIA_AEupdate(req_EDS, template)

    else: 
        raise Exception('Invalid Chassis')


    document.merge(
        ProjectManager = req_EDS['Project_Manager'],
        PlannerName = req_EDS['Planner_Name'],
        ProjectName = req_EDS['Project_Name'],
        Priority = req_EDS['Project_Priority'],
        Status = req_EDS['Status_s'],
        TeamName = req_EDS['Team_Name'],
        Rpats = req_EDS['Rpats'],
        Contributors = req_EDS['Contributors'],
        Oracle = req_EDS['Oracle'],
        RevisionDate = req_EDS['Revision_Date'],
        Checked = req_EDS['Checked_By'],
        CAName = req_EDS['CA_Name'],
        CANum = req_EDS['CA_Number'],
        CName = req_EDS['Coordinator_Name'],
        CTeam = req_EDS['Coordinatior Team'],
        CNum = req_EDS['Coordinatior Number'],
        RevisionNumber = req_EDS['Revision_Number'],
        RDate = req_EDS['R_Date'],
        TISD =  req_EDS['TS_Date'],
        Role = current_user.role,
        Contact = current_user.contact,
    )

    document.write('/opt/EDS-Automation-TPIA/testoutput.docx')
    return '/opt/EDS-Automation-TPIA/testoutput.docx'

if __name__ == '__main__':
    generate_EDS('')    
