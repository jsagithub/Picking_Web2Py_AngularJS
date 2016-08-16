# -*- coding: utf-8 -*-
import gluon.contrib.simplejson

def get_pick(pick_id):  
    """
    App need to have at least 1 barcode
    >>> len(db(db.pickings.id==None).select()) ### test NULL
    0
    """  
    pick= db(db.pickings.id==pick_id).select().first().as_dict()
    return pick

def add_pick():
    """
        len barcode need to be 13
    >>> barcodes=db(db.pickings).select(db.pickings.barcode).first()
    >>> len(barcodes.barcode)
    13
    """
    new_pick=gluon.contrib.simplejson.loads(request.body.read())
    pick_id=db.pickings.validate_and_insert(barcode=new_pick['barcode'])
    new_pick=get_pick(pick_id)
    return  gluon.contrib.simplejson.dumps(dict(newPick=new_pick))

def index():
    """ 
    Get all barcode from DB
    """
    rows = db(db.pickings).select().as_list()
    return dict(pick_list=gluon.contrib.simplejson.dumps(rows))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
