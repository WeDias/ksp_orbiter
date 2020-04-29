#!/usr/bin/env python
# -*- coding: utf-8 -*-

# KSP_ORBITER.py
# Github:@WeDias

# MIT License

# Copyright (c) 2020 Wesley Ribeiro Dias

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import krpc
from time import sleep
from datetime import datetime


def ler_dados():
    """
    Função para obter as configuracoes de orbitas salvas no computador
    Retorna: dict(), com todas as configurcoes de orbita dos astros
    """
    config_padrao = {}
    with open('configs/orbit.config', 'r') as arquivo:
        for linha in arquivo.readlines():
            linha = linha.strip()
            ld_astro = linha[:linha.index(';')]
            ld_apoastro = int(linha[linha.index(';') + 1:linha.rindex(';')])
            ld_periastro = int(linha[linha.rindex(';') + 1:])
            config_padrao[ld_astro] = {'apoastro': ld_apoastro, 'periastro': ld_periastro}
    return config_padrao


def muda_orbita_padrao(mod_astro, mod_apoastro, mod_periastro):
    """
    Função para alterar a configuracao de orbita de determinado astro e salvar
    astro: nome do astro terá seus valores alterados
    apoastro: valor do novo apoastro
    periastro: valor do novo periastro
    Retorna: Sem retorno
    """
    config_padrao = ler_dados()
    config_padrao[mod_astro] = {'apoastro': mod_apoastro, 'periastro': mod_periastro}
    with open('configs/orbit.config', 'w') as arquivo:
        for mod_astro in config_padrao:
            arquivo.write(f'{mod_astro};{config_padrao[mod_astro]["apoastro"]};{config_padrao[mod_astro]["periastro"]}\n')
    return None


def orbita_padrao(op_astro):
    """
    Função para obter a configuracao de orbita padrao em determinado corpo celeste
    astro: nome do astro
    Retorna: dict(), com o valor do apoastro e periastro
    """
    config_padrao = ler_dados()
    op_astro = str(op_astro).lower()
    return config_padrao[op_astro]


def resetar_orbita_padrao():
    """
    Função para resetar os dados de orbita
    Retorna: Sem retorno
    """
    reset = {'moho':
                 {'apoastro': 10000, 'periastro': 10000},

             'eve':
                 {'apoastro': 100000, 'periastro': 100000},

             'gilly':
                 {'apoastro': 10000, 'periastro': 10000},

             'kerbin':
                 {'apoastro': 80000, 'periastro': 80000},

             'mun':
                 {'apoastro': 50000, 'periastro': 50000},

             'minmus':
                 {'apoastro': 10000, 'periastro': 10000},

             'duna':
                 {'apoastro': 60000, 'periastro': 60000},

             'ike':
                 {'apoastro': 10000, 'periastro': 10000},

             'dres':
                 {'apoastro': 12000, 'periastro': 12000},

             'laythe':
                 {'apoastro': 60000, 'periastro': 60000},

             'vall':
                 {'apoastro': 15000, 'periastro': 15000},

             'tylo':
                 {'apoastro': 10000, 'periastro': 10000},

             'bop':
                 {'apoastro': 10000, 'periastro': 10000},

             'pol':
                 {'apoastro': 10000, 'periastro': 10000},

             'eeloo':
                 {'apoastro': 10000, 'periastro': 10000}}

    with open('orbit.config', 'w') as arquivo:
        for rop_astro in reset:
            arquivo.write(f'{rop_astro};{reset[rop_astro]["apoastro"]};{reset[rop_astro]["periastro"]}\n')
    return None


while True:
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
                                                                                                                  BY: WEDIAS''')
    print('=' * 126)
    opcao = input('''[1] INICIAR CONTAGEM E LANCAR
[2] DADOS DE ORBITA ATUAL
[3] ALTERAR DADOS DE ORBITA
[0] FECHAR O PROGRAMA
[DIGITE UMA OPCAO]:  ''')
    while opcao not in '0123':
        opcao = input('ERRO: OPCAO INVALIDA, [DIGITE UMA OPCAO]: ')
    print('=' * 126)

    if opcao == '0':
        break

    elif opcao == '1':
        # Conecxao com o foguete
        conn = krpc.connect()
        vessel = conn.space_center.active_vessel

        # Definindo as constantes
        constante_gravitacional = 6.674184 * 10 ** -11
        nome_planeta = str(vessel.orbit.body.name).lower()
        massa_planeta = vessel.orbit.body.mass
        raio_planeta = vessel.orbit.body.equatorial_radius
        dados_de_orbita = orbita_padrao(nome_planeta)
        apoastro_alvo = int(dados_de_orbita['apoastro'])
        periastro_alvo = int(dados_de_orbita['periastro'])
        margem_erro = 500

        # Contagem regressiva de 10s
        for c in range(10, 0, - 1):
            print(f'\rCONTAGEM REGRESSIVA: {c}', end='')
            sleep(1)

        print(f'\rFOGUETE LANÇADO {datetime.today()}')
        vessel.auto_pilot.engage()
        vessel.auto_pilot.target_pitch_and_heading(90, 90)
        print(f'DADOS DE TELEMETRIA DO FOGUETE: "{vessel.name}"')

        # Instrucoes de voo/orbita | Computador de bordo
        grupo1 = queda_sub_orbital = sub_orbital = False
        print(f"CONFIGURACAO DE ORBITA: APOASTRO: {apoastro_alvo}M | PERIASTRO:{periastro_alvo}M")
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
            print(f'\rALT:{altura_mar:.2f}M | APO:{apoastro:.2f}M | TEMPA:{tempo_apoastro}S | PER:{periastro:.2f}M | VELSUP:{ace_sup:.2f}M/S | VELORB:{ace_orb:.2f}M/S | SITU:{situacao.upper()} | TEMPO:{int(vessel.met)}S', end='')

            #Controle da potencia dos motores
            if twr != 0:
                tempo = (18.5 * 5) / 2

                if altura_mar < (apoastro_alvo * 0.35):
                    vessel.control.throttle = 1.5 / twr
                    vessel.control.gear = False

                elif vessel.orbit.time_to_apoapsis <= tempo or queda_sub_orbital:

                    if 0 < vessel.orbit.time_to_apoapsis < 3 or queda_sub_orbital:
                        vessel.control.throttle = 1
                        queda_sub_orbital = True

                    else:
                        vessel.control.throttle = 2 / twr

                elif ((apoastro_alvo * 0.95) + margem_erro) > altura_mar > (apoastro_alvo * 0.35):

                    if apoastro >= (apoastro_alvo + margem_erro):
                        vessel.control.throttle = 0

            # Separacao de estagio
            if vessel.available_thrust == 0 and vessel.control.current_stage != 0:
                print(f'\rSEPARAÇÃO DE ESTÁGIO {datetime.today()}')
                vessel.control.activate_next_stage()

            # Plano de inclinacao
            if 100 < altura_mar < (apoastro_alvo + 100):
                vessel.auto_pilot.target_pitch_and_heading(90 - ((altura_mar / 100) * (90 / (apoastro_alvo / 100))), 90)

            # Orbita com sucesso !
            if (apoastro + margem_erro) >= periastro > (periastro_alvo - margem_erro):

                if not grupo1:
                    vessel.control.toggle_action_group(1)
                    grupo1 = True

                vessel.control.throttle = 0
                print(f'\nSUCESSO ! FOGUETE EM ORBITA DE {nome_planeta.upper()} {datetime.today()}')
                sleep(1)
                print(f'APOASTRO:{vessel.orbit.apoapsis_altitude:.2f}M | PERIASTRO:{vessel.orbit.periapsis_altitude:.2f}M | TEMPO:{int(vessel.met)}S')
                vessel.auto_pilot.disengage()
                vessel.control.sas = True
                break

    elif opcao == '2':
        print('DADOS DE ORBITA:')
        dados_de_orbita = ler_dados()
        for nome in dados_de_orbita:
            print(nome, dados_de_orbita[f'{nome}'])

    elif opcao == '3':
        print('ALTERAR DADOS DE ORBITA:\n[1] ALTERAR DADOS\n[0] RESETAR DADOS')
        opcao = input('[DIGITE UMA OPCAO]: ').lower()

        if opcao == '0':
            resetar_orbita_padrao()
            print('DADOS RESETADOS COM SUCESSO !')

        elif opcao == '1':
            astro = input('DIGITE O NOME DO ASTRO: ').lower()
            print(f'DADOS ATUAIS DE {astro.upper()}:', ler_dados()[astro])
            novo_apoastro = int(input('DIGITE O NOVO APOASTRO: '))
            novo_periastro = int(input('DIGITE O NOVO PERIASTRO: '))
            muda_orbita_padrao(astro, novo_apoastro, novo_periastro)
            print(f'DADOS DE ORBITA DE {astro.upper()} ALTERADO COM SUCESSO:', ler_dados()[astro])
    input('PRESSIONE ENTER PARA VOLTAR')
