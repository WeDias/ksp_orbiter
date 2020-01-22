#-------------------------------------------------------------#
#                                        KSP ORBITER          #
#                                      Github:@WeDias         #
#                                   Licença: MIT License      #
#                               Copyright © 2020 Wesley Dias  #
#-------------------------------------------------------------#

import krpc
from time import sleep
from datetime import datetime

print('=' * 126)
print('''
888    d8P   .d8888b.  8888888b.        .d88888b.  8888888b.  888888b.  8888888 88888888888 8888888888 8888888b.  
888   d8P   d88P  Y88b 888   Y88b      d88P" "Y88b 888   Y88b 888  "88b   888       888     888        888   Y88b 
888  d8P    Y88b.      888    888      888     888 888    888 888  .88P   888       888     888        888    888 
888d88K      "Y888b.   888   d88P      888     888 888   d88P 8888888K.   888       888     8888888    888   d88P 
8888888b        "Y88b. 8888888P"       888     888 8888888P"  888  "Y88b  888       888     888        8888888P"  
888  Y88b         "888 888             888     888 888 T88b   888    888  888       888     888        888 T88b   
888   Y88b  Y88b  d88P 888             Y88b. .d88P 888  T88b  888   d88P  888       888     888        888  T88b  
888    Y88b  "Y8888P"  888              "Y88888P"  888   T88b 8888888P" 8888888     888     8888888888 888   T88b 
                                                                                                                  BY: WeDias''')
print('=' * 126)
input('>>PRESSIONE ENTER PARA INICIAR O LANÇAMENTO, AGUARDANDO...')

# Conecxao com o foguete
conn = krpc.connect()
vessel = conn.space_center.active_vessel

# Contagem regressiva de 10s
for c in range(10, 0, - 1):
    print(f'\r    >>CONTAGEM REGRESSIVA: {c}', end='')
    sleep(1)

print(f'\r    >>FOGUETE LANÇADO {datetime.today()}')
vessel.control.activate_next_stage()
vessel.auto_pilot.engage()
vessel.auto_pilot.target_pitch_and_heading(90, 90)
print(f'        DADOS DE TELEMETRIA DO FOGUETE: "{vessel.name}"')

# Definindo as constantes
constante_gravitacional = 6.674184 * 10 ** -11
massa_planeta = vessel.orbit.body.mass
raio_planeta = vessel.orbit.body.equatorial_radius

# Instrucoes de voo/orbita | Computador de bordo
grupo1 = queda_sub_orbital = False
while True:
    # Dados de telemetria do foguete
    altura_mar = vessel.flight().mean_altitude
    apoastro = vessel.orbit.apoapsis_altitude
    periastro = vessel.orbit.periapsis_altitude
    ace_sup = vessel.flight(vessel.orbit.body.reference_frame).speed
    ace_orb = vessel.flight(vessel.orbit.body.non_rotating_reference_frame).speed
    situacao = vessel.situation.name
    aceleracao_gravidade = constante_gravitacional * massa_planeta / (raio_planeta + altura_mar) ** 2
    twr = vessel.available_thrust / (vessel.mass * aceleracao_gravidade)
    tempo_apoastro = int(vessel.orbit.time_to_apoapsis)
    print(f'\r        Alt:{altura_mar:.2f}m | Apo:{apoastro:.2f}m | TempA:{tempo_apoastro}s | Per:{periastro:.2f}m | VelSup:{ace_sup:.2f}m/s | VelOrb:{ace_orb:.2f}m/s | Situ:{situacao} | Tempo:{int(vessel.met)}s', end='')

    # Potencia dos motores
    if twr != 0:
        if altura_mar < 35000:
            vessel.control.throttle = 1.50 / twr

        else:
            if 95000 > altura_mar > 35000:
                vessel.control.throttle = 1.15 / twr

            else:
                if int(vessel.orbit.time_to_apoapsis) <= 5 or queda_sub_orbital:
                    vessel.control.throttle = 1
                    queda_sub_orbital = True

                else:
                    vessel.control.throttle = 1.02 / twr

    # Separacao de estagio
    if vessel.available_thrust == 0:
        print(f'\r        SEPARAÇÃO DE ESTÁGIO {datetime.today()}')
        vessel.control.activate_next_stage()

    # Plano de inclinacao
    if 100 < altura_mar < 100100:
        vessel.auto_pilot.target_pitch_and_heading(90 - ((altura_mar / 100) * 0.09), 90)

    # Orbita com sucesso !
    if apoastro >= periastro - 250 and periastro > 100000:
        if not grupo1:
            vessel.control.toggle_action_group(1)
            grupo1 = True
        vessel.control.throttle = 0
        vessel.auto_pilot.disengage()
        vessel.control.sas = True
        print(f'\n    >>SUCESSO ! FOGUETE EM ORBITA DE KERBIN {datetime.today()}')
        sleep(1)
        print(f'        Apoastro:{vessel.orbit.apoapsis_altitude:.2f}m | Periastro:{vessel.orbit.periapsis_altitude:.2f}m | Tempo à orbita:{int(vessel.met)}s')
        break

input('>>PRESSIONE ENTER PARA FECHAR O PROGRAMA, AGUARDANDO...')
print('=' * 126)
