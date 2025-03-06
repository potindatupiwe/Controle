from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import *
from controle.forms_models import *
class MetaCrud(type):
    def __new__(cls, name, bases, dct):
        main_class = super().__new__(cls, name, bases, dct)
        
       
        if name not in ['AddViews', 'UpdateViews', 'DeleteViews','ShowViews']:
            add_dict = {'form_class':dct['form_class'],
                        'template_name':f'adm/add_{dct['model'].__name__.lower()}.html',
                        'success_url':dct['success_url'],
                        'form_valid':dct['form_valid']}
            add_view = type('AddViews',(main_class,FormView), add_dict)
            setattr(main_class, 'AddViews', add_view)

            update_dict = {
                'fields':dct['fields'],
       
                'model':dct['model'],
                'template_name':f'adm/update_{dct['model'].__name__.lower()}.html',
                'success_url':dct['success_url']
            }
            update_view = type('UpdateViews',(UpdateView,main_class), update_dict)
            setattr(main_class, 'UpdateViews', update_view)
            
           
            delete_dict = {
                'model':dct['model'],
                'success_url':dct['success_url'],
                'template_name':f'adm/delete_{dct['model'].__name__.lower()}.html'
            }
            delete_view = type('DeleteViews',(DeleteView,main_class), delete_dict)
            setattr(main_class, 'DeleteViews', delete_view)
       
            show_dict={
                'model':dct['model'],
                'template_name':f'adm/show_{dct['model'].__name__.lower()}.html',
                'context_object_name':dct['context_object_name']
            }
            show_view = type('ShowViews',(main_class,ListView), show_dict)
            setattr(main_class, 'ShowViews', show_view)
       
        return main_class

