from math import atan2, cos, sin
from re import A
from turtle import distance
import mesa
from mesa.space import F, ContinuousSpace
import random
import math

# Data visualization tools.
# import seaborn as sns

# Has multi-dimensional arrays and matrices. Has a large collection of
# mathematical functions to operate on these arrays.
import numpy as np
import pygame

# Data manipulation and analysis.
# import pandas as pd

class PedestrianAgent(mesa.Agent): #Класс агента
    """An agent with fixed initial wealth."""
  
    def __init__(self, unique_id, type, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the agent's attribute and set the initial values.
        self.human = pygame.image.load('human.png')
        self.type = type # Направление движение агента-пешехода: 1-на вход, 2 - на выход
        self.state = 0 # Состояние агента-пешехода: 0-еще не прошел турникет, 1 - прошел турникет
        self.x = 0
        self.y = 0

    def step(self):
        
        #Оцениваем количество агентов расположенных в области с фиксированным радиусом R независимо от направления их движения
        R = 100
        po = 10 #Пороговая плотность пространства
        nearest_agents2 = self.model.get_agents_of_type(PedestrianAgent).select(lambda a: self.get_distance(a.x, self.x, a.y, self.y) < R and (a.x!=self.x or a.y!=self.y))
            
        if(len(nearest_agents2)<=po):
            self.human = pygame.image.load('human.png')
        if(len(nearest_agents2)>po):
            self.human = pygame.image.load('human2.png')

        #Движение пешехода на вход до прохождения турникета
        if self.type == 1 and self.state==0:
            irez = int(random.random()* len(self.model.arr_list1))
            alpha = atan2(self.model.arr_list1[irez-1] - self.y, 400 - self.x)
            
            #Отбираем близко расположенных агентов
            nearest_agents = self.model.get_agents_of_type(PedestrianAgent).select(lambda a: self.get_distance(a.x, self.x, a.y, self.y) < 10 and a.type==self.type and (a.x!=self.x or a.y!=self.y))
            
            if(len(nearest_agents)>0):
                min_dist = 10000
                for i in range(0, len(nearest_agents)):
                    if self.get_distance(nearest_agents[i].x, self.x, nearest_agents[i].y, self.y) < min_dist:
                         min_dist = self.get_distance(nearest_agents[i].x, self.x, nearest_agents[i].y, self.y)
                         nearest_agent_index = i # Ближайший агент
                

            #Если нет препятствий в виде других агентов, то агент движется к турникету
            if(len(nearest_agents)==0):
                self.x = self.x + 1*cos(alpha)
                self.y = self.y + 1*sin(alpha)
                
            #Если есть препятствие в виде других агентов, то агент смещается в противоположную сторону
            if(len(nearest_agents)>0):
                gamma = math.pi + atan2(nearest_agents[nearest_agent_index].y - self.y, nearest_agents[nearest_agent_index].x - self.x)
                self.x = self.x + min_dist*cos(gamma)
                self.y = self.y + min_dist*sin(gamma) 
            
        #Движение пешехода на выход до прохождения турникета
        if self.type == 2  and self.state==0:
            irez = int(random.random()* len(self.model.arr_list2))
            alpha = atan2(self.model.arr_list2[irez-1] - self.y, 400 - self.x)
            
            #Отбираем близко расположенных агентов
            nearest_agents = self.model.get_agents_of_type(PedestrianAgent).select(lambda a: self.get_distance(a.x, self.x, a.y, self.y) < 10 and a.type==self.type and (a.x!=self.x or a.y!=self.y))
            
            if(len(nearest_agents)>0):
                min_dist = 10000
                for i in range(0, len(nearest_agents)):
                    if self.get_distance(nearest_agents[i].x, self.x, nearest_agents[i].y, self.y) < min_dist:
                         min_dist = self.get_distance(nearest_agents[i].x, self.x, nearest_agents[i].y, self.y)
                         nearest_agent_index = i # Ближайший агент
                         
                
            #Если нет препятствий в виде других агентов, то агент движется к турникету
            if(len(nearest_agents)==0):
                self.x = self.x + 1*cos(alpha)
                self.y = self.y + 1*sin(alpha)
                
            #Если есть препятствие в виде других агентов, то агент смещается в противоположную сторону
            if(len(nearest_agents)>0):
                gamma = math.pi + atan2(nearest_agents[nearest_agent_index].y - self.y, nearest_agents[nearest_agent_index].x - self.x)
                self.x = self.x + min_dist*cos(gamma)
                self.y = self.y + min_dist*sin(gamma) 

        #Движение пешехода на вход после прохождения турникета
        if self.type == 1 and self.state==1:
            self.x = self.x + 1
        #Движение пешехода на выход после прохождения турникета
        if self.type == 2  and self.state==1:
            self.x = self.x - 1
        
        #Смена состояния агента при проходе через турникет
        if (self.x > 400 and self.type == 1) or (self.x < 400 and self.type == 2):
            self.state = 1
    
    # Расчёт Евклидова расстояния     
    def get_distance(self, x1, x2, y1, y2):
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx**2 + dy**2)

       
class TurnstileAgentIn(mesa.Agent): #Турникеты на вход
    """An agent with fixed initial wealth."""
    # Списки y-координат турникетов

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the agent's attribute and set the initial values.
        self.turn = pygame.image.load('turn1.png')
        self.x = 0
        self.y = 0
        
class TurnstileAgentOut(mesa.Agent): #Турникеты на выход
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the agent's attribute and set the initial values.
        self.turn = pygame.image.load('turn2.png')
        self.x = 0
        self.y = 0


class TurnstileModel(mesa.Model): #Класс модели
    """A model with some number of agents."""
    
    # Списки координат турникетов
    arr_list1 = list()
    arr_list2 = list()

    def __init__(self, N1, N2, N3, dist, width, height):
        super().__init__()

        self.num_agents1 = N1
        self.num_agents2 = N2
        self.num_agents3 = N3
        
        
        # Create scheduler and assign it to the model
        self.schedule = mesa.time.RandomActivation(self)
        
        self.space = mesa.space.ContinuousSpace(width, height, True)
        
        
        # Create agents
        for i in range(self.num_agents1):
                        
            # Add the agent to a space
            p = self.random.random()
            if p < 0.5:
                   x_min = 10
                   y_min  = 200
                   x_max = self.space.x_max / 2
                   y_max = self.space.y_max - 300
                   a = PedestrianAgent(i, 1, self)
                  
            if p >= 0.5:
                   x_min = self.space.x_max / 2 
                   y_min  = 200
                   x_max = self.space.x_max - 700
                   y_max = self.space.y_max - 300
                   a = PedestrianAgent(i, 2, self)
                   
            x = x_min + self.random.random() * x_max
            y = y_min + self.random.random() * y_max
            a.x = x
            a.y = y
            
            # Add the agent to the scheduler
            self.schedule.add(a)
            
            pos = np.array((x, y))
                        
            self.space.place_agent(a, pos)
            
        y = 160
        for i in range(self.num_agents2):
                    a = TurnstileAgentIn(i, self)
                    # Add the agent to the scheduler
                    self.schedule.add(a)
            
                    # Add the agent to a space
                    x = 400
                    y = y + dist;
                    self.arr_list1.insert(len(self.get_agents_of_type(TurnstileAgentIn)) + 1, y)
                    a.x = x
                    a.y = y
                    pos = np.array((x, y))
            
                    self.space.place_agent(a, pos)
                    
        y = 460
        for i in range(self.num_agents3):
                    a = TurnstileAgentOut(i, self)
                    # Add the agent to the scheduler
                    self.schedule.add(a)
            
                    # Add the agent to a space
                    x = 400
                    y = y + dist;
                    self.arr_list2.insert(len(self.get_agents_of_type(TurnstileAgentOut)) + 1, y)
                    a.x = x
                    a.y = y
                    pos = np.array((x, y))
            
                    self.space.place_agent(a, pos)

    def step(self):
        """Advance the model by one step."""

        # The model's step will go here for now this will call the step method of each agent and print the agent's unique_id
      
        self.schedule.step() 
        
    def add_agent1(self):

             p = self.random.random()
             if p < 0.5:
                   x_min = 10
                   y_min = 200 
                   x_max = self.space.x_max / 2
                   y_max = self.space.y_max - 300
                   a = PedestrianAgent(len(self.get_agents_of_type(PedestrianAgent)) + 1, 1, self)
                  
             if p >= 0.5:
                   x_min = self.space.x_max / 2
                   y_min = 200
                   x_max = self.space.x_max - 700
                   y_max = self.space.y_max - 300
                   a = PedestrianAgent(len(self.get_agents_of_type(PedestrianAgent)) + 1, 2, self)
                   
             x = x_min + self.random.random() * x_max
             y = y_min + self.random.random() * y_max
             a.x = x
             a.y = y
             pos = np.array((x, y))
             
             self.schedule.add(a)
             self.space.place_agent(a, pos)
             
    def add_agent2(self, y, d):

             a = TurnstileAgentIn(len(self.get_agents_of_type(TurnstileAgentIn)) + 1, self)
             self.schedule.add(a)
             
             x = 400
             y = y + d
             
             self.arr_list1.insert(len(self.get_agents_of_type(TurnstileAgentIn)) + 1, y)
             
             a.x = x
             a.y = y
             pos = np.array((x, y))
             self.space.place_agent(a, pos)
             
             
    def add_agent3(self, y, d):

             a = TurnstileAgentOut(len(self.get_agents_of_type(TurnstileAgentOut)) + 1, self)
             self.schedule.add(a)
             
             x = 400
             y = y + d
             
             self.arr_list2.insert(len(self.get_agents_of_type(TurnstileAgentOut)) + 1, y)

             a.x = x
             a.y = y
             pos = np.array((x, y))
             self.space.place_agent(a, pos)
             