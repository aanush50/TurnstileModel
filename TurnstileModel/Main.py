from inspect import isclass
import random
from time import sleep
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

from TurnstileModel import TurnstileModel

from TurnstileModel import PedestrianAgent
from TurnstileModel import TurnstileAgentIn
from TurnstileModel import TurnstileAgentOut

from matplotlib.figure import Figure
from mesa.experimental import JupyterViz
pygame.init()

width = 1000
height = 850 

#Запуск имитационной модели MESA


# Set up the drawing window
screen = pygame.display.set_mode([width, height])


slider1 = Slider(screen, 50, 25, 800, 10, min=0, max=300, step=1)
output1 = TextBox(screen, 875, 15, 50, 25, fontSize=20)
output1.disable() 

slider2 = Slider(screen, 50, 50, 800, 10, min=1, max=10, step=1)
output2 = TextBox(screen, 875, 40, 50, 25, fontSize=20)
output2.disable() 

slider3 = Slider(screen, 50, 75, 800, 10, min=1, max=10, step=1)
output3 = TextBox(screen, 875, 60, 50, 25, fontSize=20)
output3.disable() 

slider4 = Slider(screen, 50, 100, 800, 10, min=30, max=54, step=1)
output4 = TextBox(screen, 875, 80, 50, 25, fontSize=20)
output4.disable() 

slider1.setValue(300); # Количество агентов-пешеходов (от 100 до 300)
slider2.setValue(4); # Количество турникетов на вход (от 1 до 10)
slider3.setValue(4); # Количество турникетов на выход (от 1 до 10)
slider4.setValue(50); # Расстояние между турникетами в px (от 30 до 50)

starter_model = TurnstileModel(slider1.value, slider2.value, slider3.value, slider4.value, width, height)

green = (0, 255, 0)
blue = (0, 0, 128)


font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Total pedestrian outflow', True, green, blue)
text2 = font.render('Time', True, green, blue)
text3 = font.render('Enter', True, green, blue)
text4 = font.render('Exit', True, green, blue)

textRect = text.get_rect()
textRect.center = (260, 170)

textRect2 = text2.get_rect()
textRect2.center = (900, 170)

textRect3 = text3.get_rect()
textRect3.center = (320, 450)

textRect4 = text4.get_rect()
textRect4.center = (500, 450)

output = TextBox(screen, 475, 145, 50, 50, fontSize=30)
output.disable() 

output_t = TextBox(screen, 800, 145, 50, 50, fontSize=30)
output_t.disable() 

# Run until the user asks to quit
running = True

# Количество пешеходов которые прошли через турникеты 
ped_out_flow = 0

t = 1
Total_time = 100

while t <= Total_time:

    pygame.time.delay(100) # Время задержки кадра
    
    if pygame.mouse.get_pressed()[0] != 0:
        # collision detection also needed here
        a = pygame.mouse.get_pos()[0] - 5
        if a < 0:
            a = 0
    
   
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Управление количеством агентов-пешеходов
    delta_agents1 = slider1.getValue() - len(starter_model.get_agents_of_type(PedestrianAgent))
    
    if delta_agents1 > 0:
        for i in range(0, delta_agents1):
            starter_model.add_agent1()
            
    
    if delta_agents1 < 0:
        while slider1.getValue() -  len(starter_model.get_agents_of_type(PedestrianAgent)) < 0:
            i_rez = int(random.random()* len(starter_model.get_agents_of_type(PedestrianAgent)))
            agent = starter_model.get_agents_of_type(PedestrianAgent)[i_rez]

            if isinstance(agent, PedestrianAgent):
                starter_model.schedule.remove(agent)
                agent.remove()
                
    distance = slider4.value # Расстояние между турникетами 
    # Управление количеством агентов-турникетов на вход
    delta_agents2 = slider2.getValue() - len(starter_model.get_agents_of_type(TurnstileAgentIn))
    
    if delta_agents2 > 0:
        for i in range(0, delta_agents2):
            turn_count = len(starter_model.get_agents_of_type(TurnstileAgentIn))
            x_last = starter_model.get_agents_of_type(TurnstileAgentIn)[turn_count-1].x
            y_last = starter_model.get_agents_of_type(TurnstileAgentIn)[turn_count-1].y
            starter_model.add_agent2(y_last, distance)
            
    
    if delta_agents2 < 0:
        while slider2.getValue() -  len(starter_model.get_agents_of_type(TurnstileAgentIn)) < 0:
            i_rez = len(starter_model.get_agents_of_type(TurnstileAgentIn)) - 1
            agent = starter_model.get_agents_of_type(TurnstileAgentIn)[i_rez]

            if isinstance(agent, TurnstileAgentIn):
                starter_model.schedule.remove(agent)
                agent.remove()
                starter_model.arr_list1.pop(i_rez-1)
                
 # Управление количеством агентов-турникетов на выход
    delta_agents3 = slider3.getValue() - len(starter_model.get_agents_of_type(TurnstileAgentOut))
    
    if delta_agents3 > 0:
        for i in range(0, delta_agents3):
            turn_count = len(starter_model.get_agents_of_type(TurnstileAgentOut))
            x_last = starter_model.get_agents_of_type(TurnstileAgentOut)[turn_count-1].x
            y_last = starter_model.get_agents_of_type(TurnstileAgentOut)[turn_count-1].y
            starter_model.add_agent3(y_last, distance)
            
    
    if delta_agents3 < 0:
        while slider3.getValue() -  len(starter_model.get_agents_of_type(TurnstileAgentOut)) < 0:
            i_rez = len(starter_model.get_agents_of_type(TurnstileAgentOut)) - 1
            agent = starter_model.get_agents_of_type(TurnstileAgentOut)[i_rez]

            if isinstance(agent, TurnstileAgentOut):
                starter_model.schedule.remove(agent)
                agent.remove()
                starter_model.arr_list2.pop(i_rez-1)

    pedestrian_agents = starter_model.get_agents_of_type(PedestrianAgent)
    turnistile_agents_in = starter_model.get_agents_of_type(TurnstileAgentIn)
    turnistile_agents_out = starter_model.get_agents_of_type(TurnstileAgentOut)

    for i in range(0, len(pedestrian_agents)):
        screen.blit(pedestrian_agents[i].human, (pedestrian_agents[i].x, pedestrian_agents[i].y))
        if ((pedestrian_agents[i].x > 450 and pedestrian_agents[i].type == 1) or (pedestrian_agents[i].x < 450 and pedestrian_agents[i].type == 2)) and pedestrian_agents[i].state == 0:
            pedestrian_agents[i].state = 1
            ped_out_flow += 1 
            
        
    for i in range(0, len(turnistile_agents_in)):
        screen.blit(turnistile_agents_in[i].turn, (turnistile_agents_in[i].x, turnistile_agents_in[i].y))
    
    for i in range(0, len(turnistile_agents_out)):
        screen.blit(turnistile_agents_out[i].turn, (turnistile_agents_out[i].x, turnistile_agents_out[i].y))
       
    # Шаг модели
    starter_model.step()
    
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text4, textRect4)
    output.setText(ped_out_flow)
    
    output1.setText(slider1.getValue())
    output2.setText(slider2.getValue())
    output3.setText(slider3.getValue())
    output4.setText(slider4.getValue())
    
    pygame_widgets.update(event)

    # Отрисовка помещения
    pygame.draw.line(screen, (0, 0, 0), (420, 200), (420, 800))
    pygame.draw.line(screen, (0, 0, 0), (850, 200), (850, 800))
    pygame.draw.line(screen, (0, 0, 0), (420, 200), (850, 200))
    pygame.draw.line(screen, (0, 0, 0), (420, 800), (850, 800))
           
    t = t + 1
    output_t.setText(t)
    # Flip the display
    if t>=Total_time:
       pygame.time.wait(10000)
    pygame.display.flip()
# Done! Time to quit.
pygame.quit()
