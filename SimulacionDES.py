import simpy
import random

def NuevoProceso(env, intervalo, num, RAM):
    for _ in range(int(num)):
        yield env.timeout(intervalo)
        cantidad_memoria = random.randint(1, 10)
        instruc = random.randint(1, 10)

        if RAM.level >= cantidad_memoria:
            global process_count
            process_count += 1
            print(f"Proceso {process_count} a {env.now:7.4f}. ms")
            Sistema(env, process_count, cantidad_memoria, instruc, RAM)
            yield env.timeout(1)
        else:
            print(f'{env.now}: No hay suficiente memoria disponible: {process_count}')

#Declaracion del sistema y la ejecución de cada proceso.
class Sistema:
    def __init__(self, env, Proceso, cantidad_memoria, instruc, RAM):
        self.env = env
        self.Proceso = Proceso
        self.cantidad_memoria = cantidad_memoria
        self.instruc = instruc
        self.RAM = RAM
        self.action = env.process(self.Ejecucion_sistema())

    def Ejecucion_sistema(self):
        with self.RAM.get(self.cantidad_memoria) as required:
            yield required
            print(f"Proceso {self.Proceso} entró a ready en el tiempo {self.env.now:7.4f} y se le asignó {self.cantidad_memoria} en la RAM")

        while self.instruc > 0:
            ins_ejecutados = min(self.instruc, 3)
            print(f"El cliclo {self.Proceso} con {self.env.now:7.4f} faltan {self.instruc} ins")

            self.instruc -= ins_ejecutados
            yield self.env.timeout(1)

            if self.instruc == 0:
                global ciclos
                ciclos += 1
                print(f'{self.env.now}: Proceso {self.Proceso} ha terminado,  {self.env.now:7.4f} ms')
                self.RAM.put(self.cantidad_memoria)
                break

            if random.choice([True, False]):
                print(f'Proceso {self.Proceso} entró en el proceso de waiting en el tiempo {self.env.now:7.4f} ms')
                yield self.env.timeout(1)
                print(f'Proceso {self.Proceso} ha terminado los procesos correspondientes a I/O en el tiempo {self.env.now:7.4f} ms')
            else:
                print(f'Proceso {self.Proceso} entró al proceso de ready en el tiempo {self.env.now:7.4f} ms')



# Parámetros para realizar la simulación correspondiente.
intervalo_between_processes = random.expovariate(1/10)
random.seed(100)
env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100)
ciclos = 0
process_count = 0

# Al ya tener inicializado, correr el programa.
num_to_generate = input("Ingrese el número de procesos: ")
if num_to_generate.isnumeric():
    simulation_process = env.process(NuevoProceso(env, intervalo_between_processes, num_to_generate, RAM))
    env.run(until=simulation_process)