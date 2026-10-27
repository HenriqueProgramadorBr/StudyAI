# StudyAI --- Planejamento Completo do Projeto

**Versão:** 1.0\
**Data:** 26/10/2026\
**Objetivo:** desenvolver um aplicativo de estudos com recursos de IA,
priorizando custo zero, privacidade e execução local sempre que
possível.

------------------------------------------------------------------------

## 1. Visão geral

O **StudyAI** será um aplicativo para transformar materiais de estudo em
recursos úteis para aprender e revisar. O usuário poderá adicionar
vídeos ou canais do YouTube, PDFs, fotos de anotações, textos e outros
materiais compatíveis. A partir deles, o sistema poderá organizar
conteúdos, criar resumos, perguntas, flashcards e recomendações de
estudo.

### Princípios do projeto

1.  **Custo recorrente de R\$ 0:** não depender de APIs comerciais pagas
    nem de serviços pagos obrigatórios.
2.  **Desenvolvimento incremental:** criar uma parte por vez e testar
    antes de avançar.
3.  **Privacidade:** manter arquivos e dados localmente sempre que
    possível.
4.  **Transparência:** indicar quando um recurso ainda não está
    implementado, quando a IA não tiver certeza e quando um material não
    puder ser processado.
5.  **Compatibilidade realista:** priorizar funções que funcionem no PC
    de desenvolvimento e no celular disponível.
6.  **Código compreensível:** manter uma estrutura organizada,
    documentação e instruções reproduzíveis.
7.  **Sem promessas impossíveis:** IA local pode ser mais lenta e menos
    capaz do que modelos grandes hospedados. A qualidade dependerá do
    modelo, do tamanho do contexto e do conteúdo fornecido.

------------------------------------------------------------------------

## 2. Escopo do produto

### 2.1 Funcionalidades previstas

-   Cadastro de usuário com nome de exibição, e-mail e senha.

-   Login e logout.

-   Recuperação de acesso por um fluxo seguro, quando houver
    infraestrutura adequada para envio de e-mail; no MVP local, informar
    claramente se essa função ainda não estiver disponível.

-   Perfil básico e opção de excluir a própria conta.

-   Separação dos materiais, resumos, quizzes e flashcards por usuário,
    para que uma conta não acesse os dados de outra.

-   Adicionar texto digitado ou colado.

-   Importar PDFs.

-   Importar fotos de páginas e anotações.

-   Adicionar links de vídeos do YouTube.

-   Organizar materiais por disciplina, tema e coleção.

-   Gerar resumos estruturados.

-   Criar perguntas de revisão e quizzes.

-   Criar flashcards com frente e verso.

-   Permitir consultar um material por meio de perguntas e respostas.

-   Recomendar materiais relacionados, usando regras locais e fontes
    verificáveis.

-   Guardar histórico de materiais processados.

-   Acompanhar o progresso de revisão.

-   Oferecer uma interface móvel simples e acessível.

-   Funcionar sem conta e sem serviço externo obrigatório na primeira
    versão.

### 2.2 O que não deve ser prometido na primeira versão

-   Processar automaticamente qualquer canal inteiro do YouTube.
-   Extrair transcrições de todo vídeo sem limitações.
-   Entender perfeitamente caligrafia ou fotos desfocadas.
-   Responder sempre corretamente.
-   Treinar um modelo de linguagem do zero.
-   Sincronizar entre dispositivos sem implementar um mecanismo de
    sincronização.
-   Funcionar com o PC desligado se o backend estiver rodando apenas
    nele.
-   Oferecer pesquisa ilimitada na internet sem acesso à rede e sem
    fontes.
-   Executar modelos grandes rapidamente em um celular intermediário.

### 2.3 MVP --- primeira versão utilizável

O MVP deve conter apenas o necessário para validar o conceito:

1.  Criar e listar materiais.
2.  Inserir texto.
3.  Importar PDF textual.
4.  Extrair o conteúdo.
5.  Gerar resumo local.
6.  Gerar perguntas e flashcards.
7.  Salvar os resultados em banco de dados.
8.  Mostrar erros de maneira clara.
9.  Permitir consultar o histórico.

A integração com YouTube, OCR de imagens, recomendações avançadas e chat
com contexto maior entra depois que o fluxo básico estiver estável.

------------------------------------------------------------------------

## 3. Arquitetura proposta

### 3.1 Componentes

  -----------------------------------------------------------------------
  Componente              Tecnologia inicial      Responsabilidade
  ----------------------- ----------------------- -----------------------
  Aplicativo móvel        React Native + Expo +   Telas, navegação,
                          TypeScript              entrada de materiais e
                                                  exibição de resultados

  Backend                 Python + FastAPI        API, validação,
                                                  processamento e
                                                  coordenação das tarefas

  Banco de dados          SQLite                  Materiais, resumos,
                                                  flashcards, quizzes e
                                                  configurações

  IA local                `llama.cpp` com modelo  Geração de texto,
                          GGUF quantizado         resumos e perguntas

  Extração de PDF         PyMuPDF ou biblioteca   Extrair texto de PDFs
                          equivalente             

  OCR                     Tesseract ou            Ler texto de imagens,
                          alternativa compatível  quando necessário

  Testes                  pytest e testes manuais Verificar rotas,
                                                  processamento e fluxos
                                                  principais

  Controle de versão      Git                     Histórico de mudanças e
                                                  recuperação de versões
  -----------------------------------------------------------------------

### 3.2 Onde cada parte será executada

**Durante o desenvolvimento:**

-   O Windows 10 será usado para programar, testar o backend e manter o
    repositório.
-   O Redmi Note 8 Pro será usado para experimentar a execução local do
    modelo de IA pelo Termux.
-   Os dois dispositivos poderão se comunicar pela mesma rede Wi-Fi,
    quando necessário.

**Limitação importante:** se o backend FastAPI estiver rodando no PC,
ele não ficará disponível quando o PC estiver desligado. Para um
aplicativo independente, será necessário futuramente executar o backend
no próprio celular, incorporar o processamento ao app ou escolher uma
hospedagem gratuita que atenda aos limites do projeto. Serviços
gratuitos podem mudar suas condições.

### 3.3 Fluxo de processamento

1.  O usuário seleciona um material.
2.  O aplicativo envia o material ao backend ou o processa localmente,
    conforme o tipo e a arquitetura final.
3.  O backend valida o arquivo e extrai o texto.
4.  O texto é dividido em partes quando for muito longo.
5.  O sistema solicita ao modelo uma saída estruturada.
6.  O backend valida e normaliza a resposta.
7.  O resultado é salvo no SQLite.
8.  O aplicativo exibe o resumo, quiz ou flashcards.
9.  O usuário pode corrigir, editar, apagar ou gerar novamente o
    resultado.

### 3.4 Diagrama simplificado

``` text
Aplicativo React Native
          |
          | HTTP na rede local
          v
     API FastAPI
          |
          +------> Extração de PDF / OCR
          |
          +------> Preparação e divisão do texto
          |
          +------> IA local (llama.cpp + GGUF)
          |
          +------> SQLite
          |
          v
 Resumo / Quiz / Flashcards
          |
          v
 Aplicativo móvel
```

------------------------------------------------------------------------

## 4. Estratégia para IA local

### 4.1 Objetivo

Executar um modelo de linguagem já treinado, em formato quantizado, no
Redmi Note 8 Pro com 6 GB de RAM, sem root e sem API paga.

### 4.2 Caminho recomendado

1.  Verificar arquitetura do Android/Termux, memória e armazenamento
    disponível.
2.  Atualizar o Termux.
3.  Instalar as ferramentas de compilação necessárias.
4.  Verificar se existe pacote compatível ou compilar o `llama.cpp`.
5.  Baixar um modelo GGUF pequeno de fonte confiável.
6.  Conferir licença, tamanho e requisitos do modelo antes de baixar.
7.  Executar um prompt simples no terminal.
8.  Medir tempo de resposta, consumo de memória e estabilidade.
9.  Testar um resumo curto e um conjunto de perguntas.
10. Só então integrar o mecanismo ao backend.

### 4.3 Seleção do modelo

Um modelo pequeno da classe de aproximadamente **1B a 2B parâmetros**,
quantizado, pode ser um ponto de partida. Um modelo como Qwen2.5 1.5B
Instruct em quantização Q4 pode ser avaliado, desde que a versão
escolhida esteja disponível em GGUF e sua licença seja adequada ao uso
pretendido.

A escolha definitiva deve ser feita após testar o aparelho. O tamanho do
arquivo não representa toda a memória necessária: o modelo também usa
memória de execução e contexto. Modelos maiores podem ficar lentos,
fechar por falta de memória ou aquecer o aparelho.

### 4.4 Regras para o teste inicial

-   Não baixar vários modelos de uma vez.
-   Conferir espaço livre antes do download.
-   Usar primeiro prompts curtos.
-   Não manter muitos aplicativos pesados abertos durante o teste.
-   Monitorar temperatura e consumo de bateria.
-   Interromper se o aparelho ficar excessivamente quente ou instável.
-   Não presumir que todo modelo suporta português com a mesma
    qualidade.
-   Guardar o nome, versão, quantização e licença do modelo utilizado.

### 4.5 Limitações de uma IA local

-   Pode responder mais lentamente.
-   Pode cometer erros ou inventar informações.
-   Pode perder o contexto de documentos longos.
-   A qualidade varia de acordo com o modelo e o prompt.
-   O processamento pode consumir bateria e gerar calor.
-   O modelo ocupa armazenamento.
-   A execução offline não oferece automaticamente acesso a vídeos,
    sites ou materiais da internet.

### 4.6 Como melhorar a confiabilidade

-   Enviar o texto de origem junto da tarefa.
-   Solicitar respostas baseadas somente no material fornecido quando
    aplicável.
-   Pedir que a IA sinalize quando não houver informação suficiente.
-   Manter referências a páginas ou trechos do PDF quando possível.
-   Validar JSON e campos obrigatórios.
-   Exibir o material original para conferência.
-   Não tratar respostas geradas como gabarito infalível.

------------------------------------------------------------------------

## 5. Backend FastAPI

### 5.1 Estado inicial

O projeto já possui um backend básico em:

``` text
C:\StudyAI\backend\main.py
```

O arquivo inicial contém a aplicação FastAPI e rotas de teste:

-   `GET /` --- informa que a API está online.
-   `GET /health` --- informa o estado básico da API.
-   `/docs` --- documentação interativa automática do FastAPI.

O servidor foi iniciado com `uvicorn main:app --reload` a partir da
pasta `C:\StudyAI\backend`.

### 5.2 Estrutura-alvo

``` text
C:\StudyAI\
├── backend\
│   ├── main.py
│   ├── api\
│   │   ├── materials.py
│   │   ├── summaries.py
│   │   ├── quizzes.py
│   │   └── flashcards.py
│   ├── services\
│   │   ├── document_extractor.py
│   │   ├── ai_service.py
│   │   └── text_chunker.py
│   ├── database\
│   │   ├── connection.py
│   │   └── models.py
│   ├── schemas\
│   │   ├── materials.py
│   │   └── study_outputs.py
│   ├── tests\
│   ├── requirements.txt
│   └── README.md
├── mobile\
│   └── (aplicativo Expo, quando iniciado)
├── docs\
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
├── .gitignore
└── README.md
```

Essa estrutura é um objetivo, não uma instrução para criar todas as
pastas agora. Elas devem ser adicionadas conforme cada etapa for
implementada.

### 5.3 Rotas planejadas

#### Autenticação e conta

  -----------------------------------------------------------------------
  Método                Rota                      Função
  --------------------- ------------------------- -----------------------
  `POST`                `/auth/register`          Criar uma conta

  `POST`                `/auth/login`             Validar credenciais e
                                                  iniciar sessão

  `POST`                `/auth/logout`            Encerrar sessão ou
                                                  revogar o token

  `GET`                 `/auth/me`                Retornar os dados
                                                  básicos do usuário
                                                  autenticado

  `POST`                `/auth/forgot-password`   Iniciar recuperação de
                                                  senha, somente quando o
                                                  envio seguro de e-mail
                                                  estiver configurado

  `POST`                `/auth/reset-password`    Definir nova senha com
                                                  token de recuperação
                                                  válido
  -----------------------------------------------------------------------

A recuperação de senha por e-mail não deve ser simulada como funcional
se não existir um mecanismo real de envio. Na primeira versão local,
pode ficar explicitamente marcada como "a implementar".

  Método     Rota                           Função
  ---------- ------------------------------ -----------------------------------------
  `GET`      `/`                            Informações básicas da API
  `GET`      `/health`                      Verificar disponibilidade e componentes
  `POST`     `/materials`                   Criar material de texto
  `GET`      `/materials`                   Listar materiais
  `GET`      `/materials/{id}`              Obter um material
  `DELETE`   `/materials/{id}`              Excluir um material
  `POST`     `/materials/upload`            Importar arquivo permitido
  `POST`     `/materials/{id}/summary`      Gerar resumo
  `POST`     `/materials/{id}/quiz`         Gerar quiz
  `POST`     `/materials/{id}/flashcards`   Gerar flashcards
  `GET`      `/materials/{id}/outputs`      Consultar resultados gerados

As rotas são propostas; não devem ser consideradas implementadas até que
existam e sejam testadas.

### 5.4 Autenticação: regras de implementação

-   Nunca guardar senhas em texto puro.
-   Armazenar somente hashes de senha produzidos por uma biblioteca
    reconhecida, preferencialmente com Argon2id ou outra opção moderna
    recomendada pela biblioteca escolhida.
-   Validar e normalizar e-mails e impedir duplicatas.
-   Usar mensagens de login genéricas para não revelar se um e-mail está
    cadastrado.
-   Aplicar limites de tentativas nos endpoints de login e recuperação.
-   Criar sessões ou tokens com expiração; definir como logout e
    revogação serão tratados.
-   Não colocar segredos de assinatura dentro do código nem no
    repositório.
-   Não armazenar tokens de sessão em locais inseguros no aplicativo
    móvel. Escolher armazenamento seguro compatível com a plataforma.
-   Exigir autenticação em rotas privadas.
-   Verificar no backend a propriedade de cada material: o usuário só
    pode ler, alterar ou excluir os próprios dados.
-   Criar testes para acesso não autenticado, token expirado e tentativa
    de acessar material de outro usuário.
-   Não considerar um identificador enviado pelo app como prova de
    propriedade.
-   Em desenvolvimento local, manter a API restrita à rede privada e
    usar HTTPS em qualquer implantação acessível pela internet.

### 5.5 Validação geral e segurança

-   Definir limite de tamanho para uploads.
-   Aceitar somente formatos explicitamente suportados.
-   Não confiar apenas na extensão do arquivo.
-   Gerar nomes internos para arquivos e evitar caminhos fornecidos pelo
    usuário.
-   Tratar PDFs corrompidos e arquivos vazios.
-   Validar o conteúdo recebido com Pydantic.
-   Evitar registrar conteúdo pessoal de materiais em logs.
-   Não expor o backend à internet por padrão.
-   Se a API ficar acessível na rede local, limitar o acesso e
    considerar autenticação.
-   Nunca colocar senhas ou chaves privadas diretamente no código.
-   Não executar comandos do sistema derivados de texto enviado pelo
    usuário.

------------------------------------------------------------------------

## 6. Banco de dados

### 6.1 Entidades iniciais

**User**

-   `id`
-   `display_name`
-   `email` --- único, normalizado
-   `password_hash`
-   `created_at`
-   `updated_at`
-   `is_active`

**Material**

-   `id`

-   `user_id` --- chave estrangeira para `User`

-   `title`

-   `source_type` --- text, pdf, image ou youtube

-   `source_reference` --- caminho local ou link, se aplicável

-   `extracted_text`

-   `created_at`

-   `updated_at`

-   `processing_status`

**StudyOutput**

-   `id`

-   `user_id` --- dono do resultado, validado no backend

-   `material_id`

-   `output_type` --- summary, quiz ou flashcards

-   `content`

-   `model_name`

-   `created_at`

**Flashcard**

-   `id`
-   `material_id`
-   `front`
-   `back`
-   `review_status`
-   `created_at`

**QuizQuestion**

-   `id`
-   `material_id`
-   `question`
-   `options`
-   `correct_answer`
-   `explanation`

### 6.2 Regras

-   Todo material, resultado, quiz e flashcard deve estar associado ao
    usuário proprietário, diretamente ou por uma relação validada.

-   As consultas devem filtrar por `user_id` no servidor, não apenas no
    aplicativo.

-   Não devolver hashes de senha ou tokens nas respostas da API.

-   Criar índices para e-mail e chaves estrangeiras relevantes.

-   Definir um procedimento seguro para exclusão de conta e dos dados
    associados, informando claramente o que será apagado.

-   Usar IDs estáveis.

-   Relacionar cada resultado ao material de origem.

-   Tratar exclusões de forma consistente.

-   Fazer cópias de segurança durante o desenvolvimento.

-   Definir como o app excluirá arquivos e dados associados.

-   Evitar guardar cópias desnecessárias de documentos.

-   Não armazenar informações sensíveis sem necessidade.

------------------------------------------------------------------------

## 7. Processamento por tipo de material

### 7.1 Texto

**Prioridade: alta.**

1.  Receber o texto.
2.  Validar tamanho e título.
3.  Salvar no SQLite.
4.  Permitir gerar resumo, quiz e flashcards.
5.  Exibir erros se o texto estiver vazio ou for longo demais.

Esse é o melhor primeiro fluxo porque não depende de OCR nem de serviços
externos.

### 7.2 PDF

**Prioridade: alta, após o texto.**

1.  Aceitar PDF dentro de um limite de tamanho.
2.  Extrair texto.
3.  Detectar documento sem texto selecionável.
4.  Exibir uma prévia do texto extraído.
5.  Guardar o arquivo apenas se necessário.
6.  Processar documentos longos em blocos.
7.  Preservar números de página quando a biblioteca permitir.

PDF escaneado pode precisar de OCR; essa parte deve ser implementada
separadamente.

### 7.3 Fotos e imagens

**Prioridade: média.**

1.  Importar imagem.
2.  Validar formato, tamanho e orientação.
3.  Aplicar OCR local, se o desempenho for aceitável.
4.  Permitir corrigir o texto extraído.
5.  Enviar o texto corrigido ao fluxo de estudo.

OCR pode errar fórmulas, letras manuscritas e imagens desfocadas. A
correção manual precisa ser possível.

### 7.4 YouTube

**Prioridade: posterior.**

-   Começar por links individuais, não canais inteiros.
-   Verificar se há transcrição ou legendas acessíveis.
-   Respeitar termos de uso, direitos autorais e restrições da
    plataforma.
-   Não contornar mecanismos de acesso nem prometer transcrição de todos
    os vídeos.
-   Se não houver transcrição disponível, explicar a limitação e
    permitir colar uma transcrição obtida legitimamente.
-   Guardar o link de origem e evitar baixar ou redistribuir o vídeo sem
    necessidade.

### 7.5 Recomendações de estudo

**Prioridade: posterior.**

Começar com recomendações baseadas em regras simples:

-   mesmo assunto;
-   palavras-chave em comum;
-   disciplina selecionada;
-   temas que o usuário marcou como difíceis;
-   conteúdos relacionados a um material atual.

Recomendações geradas pela IA devem ser distinguidas de links externos
verificados. Não inventar fontes, vídeos ou URLs.

------------------------------------------------------------------------

## 8. Aplicativo móvel

### 8.1 Tecnologia

**React Native + Expo + TypeScript** é a proposta inicial para a
interface móvel. Isso mantém a UI separada do backend Python e permite
evoluir para Android sem construir toda a interface com Python.

### 8.2 Telas previstas

1.  **Início:** continuar estudando, materiais recentes e atalhos.
2.  **Adicionar material:** texto, PDF, imagem ou link.
3.  **Biblioteca:** pesquisa, filtros e coleções.
4.  **Detalhes do material:** conteúdo original e resultados.
5.  **Resumo:** texto organizado em tópicos.
6.  **Quiz:** perguntas, alternativas, resultado e explicações.
7.  **Flashcards:** frente, verso e revisão.
8.  **Chat do material:** perguntas sobre o conteúdo fornecido.
9.  **Recomendações:** próximos temas e materiais relacionados.
10. **Configurações:** armazenamento, privacidade e modelo selecionado.
11. **Cadastro:** nome de exibição, e-mail, senha e confirmação da
    senha.
12. **Login:** e-mail e senha, com validação e mensagens de erro claras.
13. **Perfil/conta:** visualizar dados básicos, sair da conta e
    solicitar exclusão.
14. **Recuperação de acesso:** somente quando houver um fluxo real e
    seguro implementado.

### 8.3 Diretrizes de interface

-   Navegação simples.
-   Texto legível e bom contraste.
-   Estados de carregamento, sucesso e erro.
-   Mensagens claras quando uma tarefa demora.
-   Não bloquear a interface durante processamento longo.
-   Permitir cancelar tarefas quando possível.
-   Exibir de onde veio um resumo ou resposta.
-   Não apresentar recursos fictícios como se já funcionassem.

### 8.4 Conexão com o backend

Durante o desenvolvimento, o celular e o PC podem se comunicar pela
mesma rede Wi-Fi. O app não deve usar `127.0.0.1` para acessar o backend
do PC, porque esse endereço no celular aponta para o próprio celular.
Será necessário usar o IP local do PC e configurar o firewall de forma
restrita à rede privada.

Não encaminhar portas do roteador nem expor a API à internet para esse
teste.

------------------------------------------------------------------------

## 9. Plano de implementação por fases

### Fase 0 --- Confirmar o ambiente

**Objetivo:** evitar instalar ferramentas desnecessárias.

-   [ ] Confirmar que `C:\StudyAI\backend\main.py` existe.
-   [ ] Ativar o ambiente virtual Python correto.
-   [ ] Iniciar o FastAPI e testar `/`, `/health` e `/docs`.
-   [ ] No Termux, verificar arquitetura, armazenamento livre e memória.
-   [ ] Atualizar pacotes do Termux.
-   [ ] Anotar erros e versões instaladas.

**Critério para avançar:** backend funcional e informações do celular
verificadas.

### Fase 1 --- API, autenticação e materiais de texto

-   [ ] Criar estrutura mínima de módulos.
-   [ ] Definir esquemas Pydantic.
-   [ ] Criar banco SQLite.
-   [ ] Criar tabela de usuários com e-mail único.
-   [ ] Implementar cadastro e login com hash seguro de senha.
-   [ ] Implementar sessão/token com expiração e logout.
-   [ ] Proteger rotas privadas e validar a propriedade dos dados.
-   [ ] Implementar criação, listagem, leitura e exclusão de materiais
    vinculados ao usuário.
-   [ ] Adicionar testes automatizados das rotas.
-   [ ] Tratar entradas vazias e inválidas.

**Critério para avançar:** cadastro/login funcionam, dados de contas
diferentes ficam isolados, e os materiais sobrevivem a reinícios.

### Fase 2 --- Testar a IA no celular isoladamente

-   [ ] Escolher o mecanismo de inferência.
-   [ ] Instalar ou compilar uma versão compatível.
-   [ ] Conferir licença e tamanho do modelo.
-   [ ] Baixar apenas um modelo pequeno.
-   [ ] Executar uma geração curta.
-   [ ] Medir velocidade, memória, temperatura e estabilidade.
-   [ ] Testar um resumo curto em português.

**Critério para avançar:** o modelo executa de forma estável e produz
uma saída útil. Se não funcionar bem, avaliar outra quantização ou outro
modelo antes de integrar.

### Fase 3 --- Integração backend--IA

-   [ ] Definir um contrato claro entre API e mecanismo de IA.
-   [ ] Criar `ai_service.py`.
-   [ ] Definir tempo máximo de execução e tratamento de falhas.
-   [ ] Validar a saída do modelo.
-   [ ] Implementar o primeiro endpoint de resumo.
-   [ ] Testar com materiais curtos.
-   [ ] Guardar modelo e metadados do resultado.

**Critério para avançar:** um texto de teste percorre o fluxo completo e
retorna um resumo validado.

### Fase 4 --- Resumos e divisão de textos longos

-   [ ] Criar divisão de texto em blocos.
-   [ ] Evitar cortar frases sem necessidade.
-   [ ] Resumir blocos individualmente quando apropriado.
-   [ ] Combinar os resumos sem perder o assunto central.
-   [ ] Preservar títulos e referências de páginas quando disponíveis.
-   [ ] Testar com textos de tamanhos diferentes.

**Critério para avançar:** textos curtos e médios são processados sem
exceder o contexto do modelo.

### Fase 5 --- Quizzes e flashcards

-   [ ] Definir formatos de saída.
-   [ ] Gerar perguntas baseadas no material.
-   [ ] Incluir resposta correta e explicação.
-   [ ] Validar se a resposta indicada existe nas alternativas.
-   [ ] Permitir revisar e editar os flashcards.
-   [ ] Testar questões ambíguas e respostas inválidas.

**Critério para avançar:** o resultado tem formato consistente e pode
ser usado pela interface.

### Fase 6 --- Importação de PDFs

-   [ ] Adicionar limite de tamanho.
-   [ ] Extrair texto.
-   [ ] Tratar PDFs sem texto selecionável.
-   [ ] Manter número de página quando possível.
-   [ ] Criar prévia para revisão do usuário.
-   [ ] Testar arquivos válidos, vazios, corrompidos e extensos.

**Critério para avançar:** o usuário consegue importar um PDF textual e
gerar um resumo.

### Fase 7 --- Interface móvel

-   [ ] Criar projeto Expo.
-   [ ] Implementar navegação.
-   [ ] Construir tela inicial e biblioteca.
-   [ ] Criar fluxo para adicionar texto.
-   [ ] Conectar ao backend local.
-   [ ] Mostrar estados de carregamento e erros.
-   [ ] Testar em um dispositivo Android.

**Critério para avançar:** um usuário consegue inserir texto no app e
ver o resultado gerado.

### Fase 8 --- Imagens e OCR

-   [ ] Escolher ferramenta de OCR local.
-   [ ] Testar em fotos nítidas e desfocadas.
-   [ ] Exibir texto extraído para correção.
-   [ ] Tratar rotação e baixa qualidade.
-   [ ] Encaminhar o texto corrigido ao fluxo normal.

**Critério para avançar:** o texto pode ser corrigido antes da geração
dos recursos de estudo.

### Fase 9 --- YouTube e recomendações

-   [ ] Aceitar links individuais.
-   [ ] Verificar disponibilidade de transcrição.
-   [ ] Tratar vídeos sem legenda acessível.
-   [ ] Preservar link e origem.
-   [ ] Implementar recomendações simples por tema e palavras-chave.
-   [ ] Exibir links externos apenas quando verificados.

**Critério para avançar:** o sistema comunica claramente o que conseguiu
ou não conseguiu processar.

### Fase 10 --- Qualidade e versão inicial

-   [ ] Testar instalação limpa.
-   [ ] Testar falha do modelo.
-   [ ] Testar pouco espaço em disco.
-   [ ] Testar reinício do backend.
-   [ ] Testar perda da conexão Wi-Fi.
-   [ ] Revisar mensagens de erro.
-   [ ] Documentar configuração e execução.
-   [ ] Criar backup do banco de dados.
-   [ ] Verificar licenças de bibliotecas e modelo.
-   [ ] Corrigir falhas antes de adicionar novas funcionalidades.

**Critério para lançamento inicial:** os fluxos principais funcionam,
falhas são compreensíveis e não há dependência de uma API paga.

------------------------------------------------------------------------

## 10. Testes e critérios de qualidade

### Testes de autenticação e isolamento de dados

-   Cadastro válido e rejeição de e-mail duplicado.
-   Rejeição de senha inválida e campos ausentes.
-   Login válido e inválido.
-   Acesso negado sem autenticação.
-   Sessão/token expirado ou revogado.
-   Usuário A não consegue abrir, alterar ou excluir material do usuário
    B.  
-   Logout encerra ou revoga a sessão conforme a estratégia escolhida.
-   Senhas nunca aparecem em logs nem nas respostas da API.
-   Exclusão de conta segue a política de remoção de dados documentada.

### Testes funcionais

-   Criar material de texto.
-   Listar e abrir material.
-   Excluir material e resultados relacionados.
-   Gerar resumo.
-   Gerar quiz.
-   Gerar flashcards.
-   Importar PDF textual.
-   Repetir processamento após reiniciar a API.

### Testes de falha

-   Texto vazio.
-   Arquivo inválido.
-   PDF corrompido.
-   Modelo indisponível.
-   Saída de IA em formato incorreto.
-   Falha de conexão.
-   Armazenamento insuficiente.
-   Texto maior do que o limite.
-   Pedido repetido durante processamento.

### Indicadores práticos

-   Percentual de tarefas concluídas sem erro.
-   Tempo de resposta para textos curtos.
-   Uso de memória durante inferência.
-   Quantidade de respostas que precisam ser corrigidas.
-   Número de falhas de extração por tipo de arquivo.
-   Facilidade para reinstalar e recuperar os dados.

Não definir metas de desempenho definitivas antes dos primeiros testes
no dispositivo real.

------------------------------------------------------------------------

## 11. Custo e recursos

### Meta de custo

  Item               Estratégia
  ------------------ ---------------------------------------------------------
  Editor             VS Code ou outro editor já disponível
  Backend            Python e FastAPI locais
  Banco              SQLite
  Modelo             Modelo aberto compatível com a licença e execução local
  Inferência         `llama.cpp` ou mecanismo compatível
  Aplicativo         Expo/React Native e ferramentas gratuitas
  Versionamento      Git
  APIs de IA pagas   Não usar como dependência
  Hospedagem paga    Não necessária para o protótipo local

**Atenção:** "sem API paga" não significa custo absolutamente zero em
qualquer cenário. Downloads usam internet, o processamento consome
bateria e armazenamento, e publicar ou hospedar serviços pode ter
custos. A meta é evitar cobranças recorrentes obrigatórias para o
funcionamento do MVP.

------------------------------------------------------------------------

## 12. Segurança e privacidade

-   Não enviar documentos pessoais para serviços externos sem
    consentimento.
-   Não incluir senhas ou tokens no Git.
-   Adicionar arquivos de banco, modelos e uploads ao `.gitignore`
    quando apropriado.
-   Limitar tamanho e formato dos arquivos.
-   Restringir o backend à rede local durante o desenvolvimento.
-   Não expor SSH ou FastAPI à internet sem necessidade.
-   Manter dependências atualizadas.
-   Informar ao usuário onde os materiais são armazenados.
-   Implementar exclusão de materiais e resultados.
-   Não registrar textos completos em logs por padrão.
-   Verificar licenças dos modelos e bibliotecas antes de distribuir o
    app.

------------------------------------------------------------------------

## 13. Git e organização do trabalho

Usar Git desde cedo para conseguir recuperar versões estáveis.

Exemplo de marcos:

-   `chore: criar backend FastAPI`
-   `feat: adicionar materiais de texto`
-   `feat: persistir materiais no SQLite`
-   `feat: integrar IA local`
-   `feat: gerar resumos`
-   `feat: gerar quizzes`
-   `feat: gerar flashcards`
-   `feat: importar PDFs`
-   `feat: criar interface móvel`

Não adicionar ao repositório:

-   ambientes virtuais;
-   arquivos GGUF grandes;
-   senhas;
-   arquivos pessoais;
-   banco de dados de uso real, salvo decisão explícita;
-   arquivos temporários e caches.

Criar um `README.md` com requisitos, instalação, comandos de execução,
testes, limitações e solução de problemas.

------------------------------------------------------------------------

## 14. Riscos e planos alternativos

  ---------------------------------------------------------------------
  Risco                              Mitigação
  ---------------------------------- ----------------------------------
  Compilação do mecanismo de IA      Verificar arquitetura e
  falha no Termux                    dependências; considerar binário
                                     ou pacote compatível

  Modelo consome muita RAM           Usar modelo menor, quantização
                                     menor ou contexto reduzido

  Celular fica lento ou aquece       Reduzir carga, limitar duração e
                                     interromper testes excessivos

  Qualidade da IA é baixa            Ajustar prompts, testar outro
                                     modelo e manter revisão humana

  PC desligado interrompe o backend  Planejar execução integrada no
                                     celular ou outra opção de
                                     hospedagem

  Wi-Fi desconectado                 Mostrar erro claro e permitir
                                     tentar novamente

  PDF não contém texto               Adicionar OCR numa fase posterior

  YouTube não oferece transcrição    Permitir entrada manual de texto
                                     ou informar a limitação

  Serviço gratuito muda suas regras  Manter o MVP funcional localmente

  Resposta da IA contém dados        Exibir origem, validar estrutura e
  incorretos                         permitir revisão
  ---------------------------------------------------------------------

------------------------------------------------------------------------

## 15. Próximas ações imediatas

A ordem recomendada para continuar a partir do estado atual:

1.  **Confirmar o backend existente** em `C:\StudyAI\backend\main.py`.
2.  Testar `http://127.0.0.1:8000/`, `http://127.0.0.1:8000/health` e
    `http://127.0.0.1:8000/docs`.
3.  Abrir o Termux diretamente no Redmi, sem depender da conexão SSH com
    o VS Code.
4.  Executar `uname -m`, `free -h` e `df -h "$HOME"`.
5.  Anotar a arquitetura e o armazenamento livre.
6.  Instalar ferramentas de compilação somente depois de confirmar o
    ambiente.
7.  Testar um único mecanismo de inferência e um único modelo pequeno.
8.  Integrar a IA ao backend apenas depois de uma geração local
    bem-sucedida.
9.  Implementar primeiro a entrada de texto, depois resumos, quizzes e
    flashcards.
10. Criar a interface móvel após a API básica estar estável.

### Comandos de diagnóstico no Termux

``` bash
uname -m
free -h
df -h "$HOME"
```

Esses comandos são somente de leitura: não apagam nem modificam
arquivos.

### Comandos de teste do backend no Windows

Execute no terminal em que o ambiente virtual está ativado e a partir da
pasta do backend:

``` powershell
uvicorn main:app --reload
```

Depois abra no navegador:

``` text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

Se a porta 8000 já estiver em uso, verifique se o backend já está
rodando antes de iniciar outra instância.

------------------------------------------------------------------------

## 16. Definição de pronto para o MVP

O StudyAI pode ser considerado pronto para uma primeira demonstração
quando:

-   [ ] O usuário consegue criar uma conta e entrar com login.
-   [ ] As rotas privadas exigem autenticação.
-   [ ] Os dados de usuários diferentes ficam isolados.
-   [ ] O usuário consegue sair da conta.
-   [ ] O usuário consegue inserir um texto.
-   [ ] O texto é salvo e pode ser reaberto.
-   [ ] A IA local gera um resumo.
-   [ ] O sistema gera perguntas e flashcards utilizáveis.
-   [ ] Os resultados ficam associados ao material correto.
-   [ ] Erros de modelo e de entrada são tratados.
-   [ ] O app consegue mostrar os resultados.
-   [ ] O projeto pode ser executado seguindo apenas o README.
-   [ ] A versão básica não exige uma API de IA paga.
-   [ ] As limitações conhecidas estão documentadas.

------------------------------------------------------------------------

## 17. Decisões que ainda precisam ser confirmadas

Estas decisões devem ser tomadas conforme os testes, não por suposição:

-   O mecanismo de IA que funciona melhor no Termux do aparelho.
-   O modelo GGUF e sua quantização.
-   O tamanho máximo de PDF.
-   Se o backend continuará no PC ou será movido para o celular.
-   Como o app será empacotado e instalado no Android.
-   Quais funções de YouTube são tecnicamente viáveis e compatíveis com
    os termos aplicáveis.
-   Se o OCR será executado no celular ou no backend.
-   Estratégia final de sessão (cookie seguro ou token) e armazenamento
    seguro no app.
-   Quando será implementada a recuperação de senha por e-mail.

**Regra de execução:** avançar uma fase por vez, registrar o resultado
dos testes e não começar a fase seguinte enquanto o critério da fase
atual não for atendido.


---

# 16. Atualização do progresso — 26/10/2026

Esta seção registra o estado atual do projeto para continuar em outra sessão sem repetir etapas concluídas.

## 16.1 Ambiente de desenvolvimento

- Sistema: Windows 10.
- Pasta principal: `C:\StudyAI`.
- Backend: `C:\StudyAI\backend`.
- Frontend: `C:\StudyAI\frontend`.
- Node.js: `v24.14.0`.
- npm: `11.9.0`.
- O frontend Next.js foi criado e a página padrão abriu em `http://localhost:3000`.
- As telas personalizadas de login, cadastro e recuperação ainda não foram criadas.

## 16.2 Backend de autenticação

O backend FastAPI, com SQLAlchemy e SQLite, tem estas rotas implementadas e testadas:

- `GET /` — rota inicial.
- `GET /health` — verificação de saúde.
- `POST /auth/register` — cadastro.
- `POST /auth/login` — login e emissão de JWT.
- `GET /auth/me` — consulta do usuário autenticado.
- `POST /auth/change-password` — alteração de senha.
- `POST /auth/forgot-password` — solicitação de recuperação.
- `POST /auth/reset-password` — redefinição de senha por token.

A documentação interativa está disponível durante a execução do backend em:
`http://127.0.0.1:8000/docs`

Comando usual para iniciar:

```powershell
cd C:\StudyAI\backend
python -m uvicorn main:app --reload
```

O usuário já testou cadastro, login, consulta do usuário, alteração de senha e recuperação de senha pelo Swagger.

## 16.3 Segurança e recuperação

- As senhas são armazenadas como hash usando `pwdlib` com o algoritmo recomendado (Argon2).
- O login usa JWT.
- A variável `STUDYAI_SECRET_KEY` está no arquivo `C:\StudyAI\backend\.env`. Não pedir nem compartilhar essa chave, senhas ou tokens reais.
- O modelo `PasswordResetToken` foi adicionado em `models.py`.
- O banco guarda o hash SHA-256 do token, não o token original.
- O token de recuperação expira em 15 minutos e só pode ser usado uma vez.
- Pedidos anteriores pendentes são invalidados quando uma nova recuperação é solicitada.
- A resposta pública de solicitação é genérica para não revelar se um e-mail está cadastrado.
- A página web de redefinição ainda não existe. O link de teste aponta para `http://localhost:3000/reset-password?token=...`.
- Antes de disponibilizar publicamente, revisar segurança adicional: limitação de tentativas, tratamento de erros, política de expiração/revogação dos JWTs e configurações de produção.

## 16.4 smtp4dev — teste de e-mail

O smtp4dev foi instalado no Windows usando:

```powershell
winget install Rnwood.Smtp4dev
```

O comando instalado é `Rnwood.Smtp4dev`. Se não for reconhecido no terminal atual, abrir um novo PowerShell.

- A interface web do smtp4dev abriu com sucesso.
- Porta SMTP confirmada: `25`.
- Autenticação SMTP desativada para o teste local.
- O envio de e-mail do backend para o smtp4dev foi testado com sucesso.
- smtp4dev captura e-mails localmente; não entrega mensagens reais para destinatários externos.

Configuração local esperada em `C:\StudyAI\backend\.env` (preservar a `STUDYAI_SECRET_KEY` já existente):

```dotenv
SMTP_HOST=127.0.0.1
SMTP_PORT=25
SMTP_USER=
SMTP_PASSWORD=
SMTP_USE_TLS=false
STUDYAI_FROM_EMAIL=studyai@localhost
STUDYAI_APP_URL=http://localhost:3000
```

O arquivo `email_service.py` foi adaptado para SMTP sem autenticação e TLS opcional. O arquivo temporário `C:\StudyAI\backend\test_email.py` foi usado para validar o envio e pode ser removido depois.

## 16.5 Frontend — estado atual

O projeto Next.js foi criado a partir de `C:\StudyAI` com:

```powershell
cd C:\StudyAI
npx create-next-app@latest frontend --typescript --eslint --app --src-dir --use-npm
```

Para executar:

```powershell
cd C:\StudyAI\frontend
npm run dev
```

A página inicial padrão foi aberta em `http://localhost:3000`.

Tecnologias escolhidas para as telas de autenticação:

- Next.js
- React
- TypeScript
- App Router
- CSS próprio (sem Tailwind nesta primeira versão)
- FastAPI como backend existente

O projeto foi criado com a pasta `src/`. Confirmar os arquivos reais antes de editar; espera-se uma estrutura semelhante a `src/app/page.tsx`, `src/app/layout.tsx` e `src/app/globals.css`.

## 16.6 Próximas etapas

### Etapa A — conferir estrutura

No PowerShell:

```powershell
cd C:\StudyAI\frontend
Get-ChildItem
Get-ChildItem .\src\app
```

Não sobrescrever arquivos até conferir a estrutura criada.

### Etapa B — criar as telas

Construir e testar uma tela de cada vez, com design consistente e responsivo:

1. Login: e-mail, senha, mostrar/ocultar senha, mensagens de erro e links para cadastro/recuperação.
2. Cadastro: nome de exibição, e-mail, senha e confirmação da senha no frontend.
3. Recuperação: formulário para solicitar o e-mail de recuperação.
4. Redefinição: ler `token` da query string e enviar `token` e `new_password` para `POST /auth/reset-password`.

Usar CSS próprio e componentes reutilizáveis quando fizer sentido. Não construir todas as telas de uma vez.

### Etapa C — integrar ao FastAPI

- `POST /auth/register`: enviar `display_name`, `email` e `password`.
- `POST /auth/login`: enviar `email` e `password`, depois tratar o JWT retornado.
- `POST /auth/forgot-password`: enviar `email`.
- `POST /auth/reset-password`: enviar `token` e `new_password`.

Antes de implementar as chamadas, conferir os modelos e respostas reais em `C:\StudyAI\backend\main.py` e no Swagger. Não inventar nomes de campos nem alterar contratos sem necessidade.

Como `http://localhost:3000` e `http://localhost:8000` são origens diferentes, configurar CORS no FastAPI permitindo explicitamente `http://localhost:3000` e, se necessário, `http://127.0.0.1:3000`. Testar chamadas reais pelo navegador.

### Etapa D — testes completos

1. Abrir o frontend.
2. Cadastrar uma conta de teste.
3. Fazer login com essa conta.
4. Solicitar recuperação e confirmar o e-mail no smtp4dev.
5. Abrir `/reset-password?token=...` e definir uma nova senha.
6. Confirmar login com a nova senha.
7. Testar e-mail inválido, senha incorreta, token inválido/expirado e falhas de rede.
8. Não expor tokens, hashes, senhas ou chaves secretas em logs ou na interface.

## 16.7 Como retomar amanhã

Use esta mensagem para continuar:

> Vamos continuar o StudyAI pelo arquivo `StudyAI_Planejamento_Atualizado_2026-10-26.md`. O backend FastAPI e a recuperação de senha já foram testados; o smtp4dev funciona na porta 25; o frontend Next.js já foi criado em `C:\StudyAI\frontend` e abre em `http://localhost:3000`. Vamos conferir a estrutura de `src/app` e criar a primeira tela de login, passo a passo, com caminhos exatos e testes antes de avançar.
