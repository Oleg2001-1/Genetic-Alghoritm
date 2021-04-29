# Aleh Iotchanka
# Ćwiczenie numer 2 - realizacja klasycznego algorytmu genetycznego
# Selekcja ruletkowa, jednorodne krzyzowanie, sukcesja generacyjna
# Maksymalizacja funkcji q(x) = max(o(x), z(x)) + REWARD(100)
import numpy as np
import random
import matplotlib.pyplot as pyplot 

length = 14         # długość ciągu bitowego       
popul_size = 400    # rozmiar populacji
iterations = 150    # liczba iteracji algorytmu
T = 3               # wartość stałej
pm = 0.1            # prawdopodobieństwo mutacji
pc = 0.9            # prawdopodobieństwo krzyżowania
attempts = 25       # ilosc razy uruchamiania algorytmu

def generation(popul_size):       
    population = []
    for i in range(popul_size):
        individ = []
        for i in range(length):
            individ.append(np.random.randint(0,2))          
        population.append(individ)
    return population


def population_rating(popul_size, population,T):  
    population_results = []
    for i in range(popul_size):
        maximum = Maximum(population[i],T)
        population_results.append(maximum)
    return population_results

def Maximum(individual , T):               #Znalezienie maximum funkcji
    for i in range(len(individual)):
        individual[i] = str(individual[i])
    max_1 = 1
    max_2 = 1
    maximum = 0
    r_individual = []
    r_individual = individual[::-1]
    for i in range((len(individual)-1)):
        if individual[i] == '1':
            if int(individual[i]) == int(individual[i+1]):
                max_1 += 1
            else:
                break
        else:
            max_1 = 0 
            break
    for i in range(len(r_individual)-1):
        if r_individual[i] == "0":
            if r_individual[i] == r_individual[i+1]:
                max_2 += 1
            else:
                break
        else:
            max_2= 0
            break
    if (max_1 >= T) and (max_2 >= T):
        maximum = 100
    if max_2 > max_1:
        maximum += max_2
    else:
        maximum += max_1
    for i in range(len(individual)):
        individual[i] = int(individual[i])
    return  maximum


def selection(popul_size, population, population_results):
    cumulative_sum = 0
    selected = []
    chances= []
    for i in range(len(population_results)):
        cumulative_sum += population_results[i]
    for i in range(len(population_results)):
        if cumulative_sum != 0:
            chances.append(population_results[i]/cumulative_sum)
    for i in range(len(population)):
        k = random.random()
        for i in range(len(chances)):
            k -= chances[i]
            if k < 0:
                chance = chances[i]
                selecte = population[i]
                selected.append(selecte)
                break
    return selected

def crossover(popul_size, selected, pc):
    population = []
    for i in range(0, int(len(selected))):
        cross = random.random()
        pr_1 = random.randint(0,len(selected)-1)
        pr_2 = random.randint(0,len(selected)-1)
        if cross < pc:
            k = random.randint(0,len(selected[0]))
            child = []
            child = selected[pr_1][0:k] + selected[pr_2][k:]
            population.append(child)
        else:
            population.append(selected[i])

    return population

def mutation(population,pm):
    for i in range(len(population)):
        l = random.random()
        if l < pm:
            for k in range(len(population[i])-1):
                a = random.randint(0, len(population[i])-1)                
                if population[i][a] == 1:
                    population[i][a] = 0
                else:
                    population[i][a] = 1
    return population            

def Best_results(population, population_results):
    best_solution, best_value = population[0], population_results[0]
    for i in range(popul_size):
        if population_results[i] > best_value:
            best_solution, best_value = population[i], population_results[i]
    return best_solution, best_value


def genetic_alg(variables, popul_size, iterations,T):
    population = generation(popul_size)                                    # generacja populacji
    population_results = population_rating(popul_size, population, T)      # ocena populacji
    best = []
    for i in range(int(iterations)):                                       # petla algorytmu                      
        selected = selection(popul_size, population, population_results)   # selekcja ruletkowa
        population = crossover(popul_size, selected, pc)                   # krzyżowanie jednopunktowe
        population = mutation(population, pm)                              # mutacja
        population_results = population_rating(popul_size, population, T)  # ocena populacji
        best.append(max(population_results))
    return Best_results(population, population_results) , best             # wartosc najlepszego osobnika
        
# uruchomienie analizy algorytmu
def Analize(attempts):
    results = []
    for i in range(attempts):
        results.append(genetic_alg(length, popul_size, iterations,T)[0][1])
    print('Długość ciągu: ', length)
    print('Wartość stałej T: ', T)
    print('Liczba elementów populacji: ', popul_size)
    print('Liczba iteracji algorytmu: ', iterations)
    print('Liczba powtórzeń algorytmu: ', attempts)
    print('Prawdopodobieństwo mutacji: ', pm)
    print('Prawdopodobieństwo krzyżowania: ', pc)
    print('Srednia wartosc: ', sum(results)/attempts)
    print('Odchylenie standardowe: ', np.std(results))
    print('Maksymalna wartosc: ', max(results))
    print('Minimalna wartosc: ', min(results))
    
    #Rysowanie wykresu
    figure, ax = pyplot.subplots(1,1)
    itterations = []
    for i in range (iterations):
        itterations.append(i)   
    pyplot.plot(itterations, genetic_alg(length, popul_size, iterations,T)[1], 'o')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Maximum')
    ax.set_title("Zależność funkcji celu od funkcji iteracji algorytmu", fontsize = 13)
    pyplot.grid(True) 
    pyplot.show()


Analize(attempts)
