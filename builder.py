#!/usr/bin/python
# @author: Fernando Pontes <fernandopontesws@gmail.com>
# @subject: CLI to automatizate flutter build and run using compilation environment declarations
import os
import json

# ENVIRONMENTS AND VARIABLES - EDITABLE
environments = ['prod', 'dev', 'hml', 'qa']

variables = {
    'prod': {
        'DEFINE_APP_NAME': 'App Produtos',
        'DEFINE_APP_SUFIX_NAME': 'PROD',
        'DEFINE_APP_HOST': 'https://www.seusite.com.br',
    },
    'dev': {
        'DEFINE_APP_NAME': 'App Produtos',
        'DEFINE_APP_SUFIX_NAME': 'DEV',
        'DEFINE_APP_HOST': 'https://dev.seusite.com.br',
    },
    'hml': {
        'DEFINE_APP_NAME': 'App Produtos',
        'DEFINE_APP_SUFIX_NAME': 'HML',
        'DEFINE_APP_HOST': 'https://hml.seusite.com.br',
    },
    'qa': {
        'DEFINE_APP_NAME': 'App Produtos',
        'DEFINE_APP_SUFIX_NAME': 'QA',
        'DEFINE_APP_HOST': 'https://qa.seusite.com.br',
    }
}

# WARNING: EDIT THE CODE BELOW, ONLY IF YOU KNOW THE THAT DOING
folderVscode = ".vscode"
fileVsCode = "launch.json"
folderEnvironments = "environments"
fileEnvironments = "config.json"
msgNotFoundFileEnvironment = "O arquivo config.json da variáveis de ambiente não foi encontrado!"

def checkFilesExists():
    filesExists = 0
    if os.path.isfile('%s/%s' % (folderVscode, fileVsCode)):
        filesExists+=1
    if os.path.isfile('%s/%s' % (folderEnvironments, fileEnvironments)):
        filesExists+=1

    if filesExists == 2:
        return True
    else:
        return False
    
def createUpdateConfigFiles(currentEnvironment, environments, variables):
    errors = []
    # CREATE/UPDATE launch.json (VS CODE)
    contentFileLaunchJson = {
        "version": "0.2.0",
        "configurations": []
    }

    for environment in environments:
        if environment in variables:
            configuration = {
            "name": "%s (%s)" % (variables[environment]['DEFINE_APP_NAME'], variables[environment]['DEFINE_APP_SUFIX_NAME']),
            "request": "launch",
            "type": "dart",
            "args": []
            }
            for variable in variables:
                if environment == variable:
                    for item in variables[variable]:
                        configuration['args'].append("--dart-define=%s=%s" % (item, variables[variable][item]))

            contentFileLaunchJson['configurations'].append(configuration) 
        else:
            errors.append("Você precisa preencher as variáveis de ambiente para: %s" % environment)      
    
    if not os.path.exists(folderVscode):
        os.makedirs(folderVscode)
    json_object = json.dumps(contentFileLaunchJson, indent = 4) 
    with open("%s/%s" % (folderVscode, fileVsCode), "w") as outfile: 
        outfile.write(json_object) 
    
    print("#####################################################\n")
    print("## Arquivo launch.json (VS Code) criado/atualizado ##\n")
    print("#####################################################\n")

    # CREATE/UPDATE config.json (ENVIRONMENTS)
    contentFileConfigJson = {}

    for variable in variables:
        if variable == currentEnvironment:
            for item in variables[variable]:
                contentFileConfigJson[item] = variables[variable][item]

    if not os.path.exists(folderEnvironments):
        os.makedirs(folderEnvironments)
    json_object = json.dumps(contentFileConfigJson, indent = 4) 
    with open("%s/%s" % (folderEnvironments, fileEnvironments), "w") as outfile: 
        outfile.write(json_object) 
    
    print("##########################################################\n")
    print("## Arquivo config.json (Environments) criado/atualizado ##\n")
    print("##########################################################\n")

    if len(errors) > 0:
        print("################# ERROS ENCONTRADOS #################")
        for error in errors:
            print("\n%s" % error)
        print("\n#####################################################")

if __name__ == '__main__':
    print('#### BEM-VINDO(A) - ESCOLHA UMA DAS OPÇÕES ABAIXO: ####\n')
    
    optionSelected = -1

    while optionSelected != 0:
        print('[1] - Criar/Atualizar launch.json (VS Code)/config.json (Environments)')
        print('[2] - Executar aplicativo emulador/device')
        print('[3] - Build Android (APK)')
        print('[4] - Build Android (Bundle)')
        print('[5] - Build iOS (IPA)')
        print('[0] - Sair')
        print("\n")
        
        optionSelected = int(input('Digite o número que deseja: '))

        if optionSelected == 1:
            print('\n#### ESCOLHA O AMBIENTE: ####\n')
            subOptionSelected = -1
            while subOptionSelected != 0:
                for idx, item in enumerate(environments, start=1):
                    print("[%s] - %s" % (idx, item.upper()))
                print('[0] - Sair')
                print("\n")
                subOptionSelected = int(input('Digite o número do ambiente: '))
                print("\n")
                
                if subOptionSelected > 0:
                    environmentSelected =  environments[subOptionSelected-1] if subOptionSelected > 0 and subOptionSelected <= len(environments) else ""
                    if environmentSelected != "":
                        createUpdateConfigFiles(environmentSelected, environments, variables)
                    else: 
                        print('Opção digitada inválida\n')
        elif optionSelected == 2:
            if checkFilesExists():
                cmd = "flutter run --dart-define-from-file=%s/%s" % (folderEnvironments, fileEnvironments)
                os.system(cmd)
            else:
                print("\n%s\n" % (msgNotFoundFileEnvironment))
        elif optionSelected == 3 or optionSelected == 4: 
            if checkFilesExists():
                if optionSelected == 3:
                    print('\n#### GERAR APK (ANDROID): ####\n')
                elif optionSelected == 4:
                    print('\n#### GERAR BUNDLE (ANDROID): ####\n')

                subOptionSelected = -1

                while subOptionSelected != 0:
                    print('[1] - Debug')
                    print('[2] - Relase')
                    print('[0] - Sair')
                    print("\n")
                    subOptionSelected = int(input('Digite o número da versão de desenvolvimento: '))
                    print("\n")

                    if subOptionSelected > 0:
                        withOutDebug = ""
                        if subOptionSelected == 1: 
                            withOutDebug = "--debug"

                        typeBuild = "apk"
                        if optionSelected == 4:
                            typeBuild = "appbundle"
                            
                        cmd = """flutter build %s %s --dart-define-from-file=%s/%s --obfuscate --split-debug-info=build/app/outputs/symbols""" % (typeBuild, withOutDebug, folderEnvironments, fileEnvironments)
                        os.system(cmd)
            else:
                print("\n%s\n" % (msgNotFoundFileEnvironment))
        elif optionSelected == 5:
            if checkFilesExists():
                print('\n#### GERAR IPA (IOS): ####\n')

                cmd = """flutter build ipa --dart-define-from-file=%s/%s --obfuscate --split-debug-info=build/app/outputs/symbols""" % (folderEnvironments, fileEnvironments)
                os.system(cmd)
            else:
                print("\n%s\n" % (msgNotFoundFileEnvironment))
        else: 
            print('\n Você saiu ;)\n')