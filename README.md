# DATA SCRAPING CHALLENGES
---
This repository contains various data scraping projects developed in Python. Each project is isolated and configured to run in a Docker container, making it easier to execute and replicate the scrapers across different environments.

### Repository Structure
---
- **challenge1/:** This project involves creating a Python script that automates data extraction from the [Compra Agora](https://www.compra-agora.com/). website. The goal is to interact with the site to collect specific information and save it in a JSON file.
- **challenge2/:** This project consists of a Python script using the Scrapy library to automate the process of retrieving billing returns for orders placed by users.
- **challenge4:** This file contains the requested data from Challenge 4's investigation.
- **challenge7:** This file contains the response for challenge 7.

### Requirements
---
- **Docker:** Make sure Docker is installed. You can download Docker at docker.com.


### How to Use
---

**1. Clone the Repository**
```bash
git clone https://github.com/seuusuario/data-scraping-projects.git
cd data-scraping-challenges
```

**2. Configure Environment Variables**
Each project may have specific environment variables. Create a ```.secrets``` file based on the ```.secrets.example``` file in the root of each project to define the necessary variables.

**3. Build the Image for a Specific Project**
To build the image for a specific project, navigate to the project directory and use the following command:
```bash
docker build -t nome_da_imagem .
```

**4. Run a Specific Project**
After building the image, to run the project, use the following command:
```bash
docker run nome_da_imagem
```
