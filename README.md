# TCC-MBA-USP
* Trabalho de Conclusão de Curso - USP/Esalq
* Título - Utilização de Crawlers para mineração de dados e sua importância no processo de tomada de decisão
* MBA DSA (Data Science e Analytics) / Turma 231
* Utilização das ferramentas *docker*, *Python 3.11* e *WSL 2*

### Executando os crawlers

1. Instale as dependências do python utilizando o comando (dentro da pasta do projeto - recommend to use a virtual env to create this environment):
```
pip install -f requirements.txt
```
2. Instalando o docker ([Instalar o Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)), executar o container com a imagem do *Selenium Standalone Browser - Firefox* através do comando:
```
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:latest
```
3. Para executar os crawlers (pastas *youtube_channels* e *youtube_trending*), acessar cada uma das pastas via terminal e executar o seguinte comando:
    Obs.: Executar primeiramente o projeto *youtube_trending* e gerar o json **trendings.json** utilizando o notebook *notebooks/create_trending_table.ipynb*, e após isso executar o crawlers de *youtube_channels* e obter o json de resultados.
    a. Para o projeto scrapy **youtube_channels**:
    ```
    scrapy crawl google [-o outputfile.json]
    ```
    b. Para o projeto scrapy **youtube_trending**:
    ```
    scrapy crawl trendings [-o outputfile.json]
    ```

Obs.: Os notebooks com os caminhos de arquivos devem ser adaptados conforme sua estruturação inserida.

---

# TCC-MBA-USP
* Final Course Work - USP/Esalq
* Title - Using Crawlers for data mining and their importance in decision making
* MBA DSA (Data Science e Analytics) / Class 231
* Working with *docker*, *Python 3.11* and *WSL 2* tools.

### Running the web crawlers

1. Install the python dependencies from command (on the project folder - recomendo utilizar um virtual env para criar o ambiente):
```
pip install -f requirements.txt
```
2. Installing the docker tool ([Install Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)), to run the container with the *Selenium Standalone Browser - Firefox* image with:
```
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:latest
```
3. To run the crawlers (folders *youtube_channels* and *youtube_trending*), access the folders by terminal and execute these commands:
    Ps.: Running first the project *youtube_trending* and create the json file **trendings.json** by jupyter notebook file *notebooks/create_trending_table.ipynb*, and after run the crawler *youtube_channels* and get the final json file with results.
    a. To scrapy project **youtube_channels**:
    ```
    scrapy crawl google [-o outputfile.json]
    ```
    b. To scrapy project **youtube_trending**:
    ```
    scrapy crawl trendings [-o outputfile.json]
    ```

Ps.: The jupyter notebook scripts with the file paths needed adapts as your structure.

