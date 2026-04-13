# Alura Certificate Manager #

Inspired and forked from https://github.com/juliogazoli/certificados-alura

## Usage ##

Follow the [README.md from https://github.com/juliogazoli/certificados-alura](https://github.com/juliogazoli/certificados-alura)

You also need setup the the .env file (use .env.sample) with your credentials (alura and gcef).

```python3 src/main.py --action [alura|gcef]```

Options:
- **alura** -> Download all certificates from alura's site and generate a resume in certificates/jecampos/resume.csv (DOWNLOAD_DIR)
- **gcef** -> upload certificates to gcef and load data from certificate into forms. GCEF works only with 15 records per time (youn should split your csv into various chuncks of 15 records)
