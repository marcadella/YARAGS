# YARAGS

Yet another RAG system

Fetch relevant annotations in zotero and use an LLM to generate some text based on this context.

Heavily inspired from https://medium.com/@emcf1/diy-ground-a-language-model-on-your-papers-from-zotero-with-finesse-a5c4ca7c187a

### Setup

#### First time setup

- Install [Ollama](https://ollama.com/) and [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main)
- Create environment: `conda env create -f environment.yml`
- Export Zotero API id and key in envirs `ZOTERO_USER_ID` and `ZOTERO_API_KEY`.
- Export Pushover API id and token in envirs `PUSHOVER_USER_KEY` and `PUSHOVER_API_TOKEN`.
- Restart terminal

#### Run notebook

- Activate environment: `conda activate YARAGS`
- Start jupyter lab: `jupyter lab`