# CogniMesh: Autonomous Multi-Agent Content Engine

> An advanced multi-agent system built with Python and LangGraph designed to autonomously research, draft, and iteratively review technical articles.

## System Architecture
```
cogni-mesh-agents-app/
│
├── app/                  # Código-fonte principal da aplicação
│   ├── core/             # Configurações globais (variáveis de ambiente, logger, etc.)
│   ├── agents/           # Definição dos agentes (Prompts, modelos e parsers)
│   ├── graph/            # A orquestração do LangGraph (o grafo de estados e transições)
│   ├── tools/            # Ferramentas externas (ex: busca na web, geradores)
│   └── api/              # Camada de entrada (endpoints FastAPI)
│
├── .env.example          # Exemplo de variáveis de ambiente necessárias (chaves de API)
├── .gitignore            # Arquivos ignorados pelo Git
├── Dockerfile            # Configuração para empacotar a aplicação em container
├── docker-compose.yml    # Orquestração de containers para rodar localmente
├── requirements.txt      # Dependências do projeto em Python
└── README.md             # O cartão de visitas do seu projeto no GitHub
```

## Agent Workflow Architecture
![alt text](public/agents-workflow.png)

The system utilizes a finite state machine to coordinate multiple LLMs with specialized roles:
1. **Researcher Agent:** Gathers up-to-date data from the web.
2. **Technical Writer Agent:** Produces a technical draft based on the research and incorporates feedback iteratively.
3. **Reviewer Agent:** Critically analyzes the text, either approving it or requesting cyclic revisions.
4. **Formatter Agent** Processes the approved draft into a clean, final Markdown output.

## 🚀 Technologies Used
- **Python 3.10+**
- **LangGraph** (Graph-based orchestration)
- **FastAPI** (Endpoint exposure)
- **Docker & Docker Compose** (Containerization)

## 🛠️ How to Run Locally
(Step-by-step instructions to be defined soon...)
