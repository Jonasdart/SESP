SELECT * FROM glpi_ipaddresses WHERE 

`mainitems_id` = '003' AND 
`mainitemtype` = 'Computer'

Sistema de Eficácia na Solução de Problemas, tem o intúito de ser uma plataforma que auxiliará os demais colaboradores da empresa a resolverem pequenos problemas que podem acontecer e interromper na rotina de trabalho.

- O sistema

    - O sistema contará com um servidor dedicado e banco de dados próprio. Utilizará do sistema de TAGS, já presente no GLPI, para buscar informações como IP da máquina e impressoras conectadas à mesma.

- O servidor

    - O servidor rodará em uma máquina virtual que todos os dias as meia noite solicitará ao servidor do SPDATA a data e hora.

- Os problemas
    
    - SPDATA lento devido operações no servidor
    - Tempo para ligar em cada setor informando que o sistema está disponível
    - SPDATA não abre por falta de mapeamento da pasta
    - SPDATA e internet não funcionam por data e hora desconfiguradas
    - Máquina lenta e/ou sistema travando/sem funcionar
    - Internet desconfigurada e/ou proxy desconfigurado
    - Internet sem conexão do cabo de rede (FISICO)
    - Impressora padrão não selecionada
    - Impressora aguardando cópia (FISICO)
    - Impressora dando erro de tonner (FISICO)
    - Mouse e/ou teclado não funcionam (FISICO)
    - Pasta compartilhada sem acesso
    - Impressora compartilhada sem acesso

- As soluções
    
    - Aguardar o término do procedimento, porém os colaboradores ficam desinformados quanto a isso e acabam ligando várias vezes para o setor. O SESP irá verificar se está acontecendo algo na rede do SPDATA assim que ele for aberto. Caso esteja, aparecerá um aviso na tela da pessoa.
    - Buscar informação, durante um loop prederteminado, se o sistema já está disponível para uso. 
    - Fazer o mapeamento da pasta SPDATA
    - Atualizar data e hora com base no horário de brasília
    - Reiniciar a máquina
    - Atualizar configuração de ip com base no banco de dados do GLPI
    - Solicitar que o colaborador verifique a conexão do cabo de rede
    - Com base no banco do GLPI padronizar a impressora e reiniciar a máquina
    - Solicitar que o colaborador desligue a impressora e retire o cabo de força e ligue novamente após um pequeno tempo
    - Solicitar que o colaborador faça o reset de configuração da impressora
    - Solicitar que o colaborador conecte a USB em outra porta
    - Solicitar que o colaborador faça novo mapeamento / ou mapear novamente a pasta e criar atalho na area de trabalho
    - Fazer o mapeamento da impressora com base no banco de dados do GLPI

- Formas de soluções

    - Script Automático/ de máquina
    - Script Manual/ de passo-a-passo

- Script Automático

    // São scripts que serão seguidos pela máquina, ou seja, que não precisarão de grande esforço do usuário final. São eles:
    
    - Verificação status manutenção SPDATA
    - Mapeamento de pastas
    - Mapeamento de impressoras
    - Selecionar impressora padrão
    - Criar atalhos na área de trabalho
    - Atualizar data e hora
    - Reiniciar máquina
    - Atualizar IP
    

- Script Manual

    // São scripts que serão seguidos pelo usuário final. Vão ser da forma de tutoriais rápidos organizados em forma de etapas. Cada etapa terá informação ÚNICA e um gif demonstrativo para o tutorial ser totalmente intuitivo. 
    Seguem quais são os scripts:

    - Verificar cabo de rede
    - Desligar e ligar a impressora
    - Fazer o reset de configuração da impressora 
    - Conectar o cabo USB do mouse/teclado em outra porta na máquina
    - Fazer o mapeamento de pastas manualmente
    - Fazer o mapeamento de impressoras manualmente

- SCRIPTS DE INICIO AUTOMATICO
    - Verificação status manutenção SPDATA
    - Data e hora
    - Configuração IP
    - Configuração Proxy 
    - Mapeamento SPDATA

