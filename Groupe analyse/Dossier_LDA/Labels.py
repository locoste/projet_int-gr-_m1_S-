#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:46:30 2020

@author: darankoum_davy_b
"""

class Labels():
    instances = [] #Ici, j'ai tous les topics
    NumeroOccurence = 0
    
    def __init__(self, topic_number, label, mots):
        self.__topic_number = topic_number
        self.__label=label
        self.__mots=mots
        self.__occurence = Labels.NumeroOccurence
        Labels.instances.append(self)
        
    def get_topic_number(self):
        return self.__topic_number
    
    def set_num_topic(self, num_topic):
        self.__topic_number = num_topic
        
    def get_label_name(self):
        return self.__label
    
    def get_occurenceMot(self):
        return self.__occurence
    
    def get_mots(self):
        return self.__mots
    
    def set_label(self, label):
        self.__label=label
     
    '''@classmethod
    def get(cls, label):
        return [inst for inst in cls.instances if inst.__id_publication == label]
    '''
    @classmethod
    def get_all_instances(cls):
        return Labels.instances
    
    @classmethod
    def get_occurence(cls):
        return Labels.NumeroOccurence
    
    @classmethod
    def set_occurence(cls):
        Labels.NumeroOccurence +=1
        
    @classmethod
    def set_instances(cls, inst):
        Labels.instances =  inst