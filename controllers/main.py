from django.shortcuts import render
from odoo import http
from odoo.http import request

class website(http.Controller):
    
    @http.route('/hello')
    def hello_world(self, **kw):
        return "hello"
        
    @http.route('/hello_all', auth="public")
    def hello(self, **kw):
        return "Hello World"
    
    @http.route('/hello_user',auth="user")
    def hello_user(self, **kw):
        return "hello %s" %request.env.user.name
    
    @http.route('/hello_world1')
    def hello_template(self, **kw):
        return request.render('estate.hello_world', {'name':'Smit'})
    
    @http.route('/template')
    def hello_(self, **kw):
        property = request.env['estate.property'].search([('state','=','sold')])
        return request.render('estate.hello_user', {'name':'Smit', 'property':property})
