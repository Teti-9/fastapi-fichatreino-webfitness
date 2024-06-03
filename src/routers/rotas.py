from src.infra.sqlalchemy.repositorios.repositorio import RepositorioTreino
from src.infra.sqlalchemy.config.database import db_dependency
from src.schemas.schemas import Treino
from fastapi import APIRouter, status
from dotenv import load_dotenv
from jinja2 import Template
from xhtml2pdf import pisa
from io import BytesIO
import os

router = APIRouter()
load_dotenv()

@router.post('/treino', status_code=status.HTTP_201_CREATED)
def popular_db(treino: Treino, db: db_dependency):
    treino_criado = RepositorioTreino(db).popular_db(treino)
    return treino_criado

@router.get('/treino/')
def gerar_ficha_geral(dias: str, db: db_dependency):
    ficha_treino_geral = {}
    exerc_selecionados = set()
    ordem = {}

    arquivo = 'src/infra/template/treino.pdf'
    html_path = "src/infra/template/template.html"
    new_html_path = "src/infra/template/treino.html"

    dias = dias.split(',')

    for dia in dias:
        ficha_treino = []

        modelo = os.environ.get(f'{dia}').split(', ')
        ordem[dia.strip().capitalize()] = list(dict.fromkeys(modelo))

        exercs_por_dia = len(modelo)
        exerc_count = {ex: 0 for ex in modelo}

        while len(ficha_treino) < exercs_por_dia:
            for exerc_name in modelo:
                if exerc_count[exerc_name] < modelo.count(exerc_name):
                    exerc = RepositorioTreino(db).procurar_exerc(exerc_name.capitalize())
                    ids_in_ficha_treino = [ex.id for ex in ficha_treino]
                    if exerc.id == 9 and 16 in ids_in_ficha_treino:
                        continue
                    if exerc.id == 16 and 9 in ids_in_ficha_treino:
                        continue
                    if exerc and (exerc.id,) not in exerc_selecionados and exerc not in ficha_treino:
                            exerc_selecionados.add((exerc.id,))
                            ficha_treino.append(exerc)
                            exerc_count[exerc_name] += 1

        muscle_grouped_exercises = {}
        for exerc in ficha_treino:
            muscle = exerc.musculo.capitalize()
            if muscle not in muscle_grouped_exercises:
                muscle_grouped_exercises[muscle] = []
            muscle_grouped_exercises[muscle].append(exerc)

        ficha_treino_geral[dia.strip().capitalize()] = muscle_grouped_exercises

    with open(html_path, 'r+', encoding='utf-8') as file:
        html_template = file.read()
        template = Template(html_template)
        new_html_template = template.render(data=ficha_treino_geral, ordem=ordem)

    with open(new_html_path, 'w', encoding='utf-8') as file:
        file.write(new_html_template)

    pdf = BytesIO()
    pisa.CreatePDF(new_html_template, dest=pdf)

    with open(arquivo, 'wb') as pdf_file:
        pdf_file.write(pdf.getvalue())
    
    # return ficha_treino_geral
    return {"mensagem": "PDF gerado com sucesso."}