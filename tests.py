import pytest
from model import Question

@pytest.fixture
def empty_question():
    return Question(title="Qual a capital de Minas Gerais?", points=10, max_selections=2)

@pytest.fixture
def question_with_choices(empty_question):
    empty_question.add_choice("São Paulo", is_correct=False)      # ID gerado: 1
    empty_question.add_choice("Belo Horizonte", is_correct=True)  # ID gerado: 2
    empty_question.add_choice("Rio de Janeiro", is_correct=False) # ID gerado: 3
    return empty_question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# --- NOVOS 10 TESTES ADICIONADOS ---

def test_nao_deve_permitir_alternativa_com_mais_de_100_caracteres():
    # 1. Comportamento: Validação do limite máximo de caracteres de uma Choice
    pergunta = Question(title="Qual a cor do cavalo branco de Napoleão?")
    texto_longo = "A" * 101  # String com 101 caracteres
    
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        pergunta.add_choice(text=texto_longo)

def test_nao_deve_permitir_pergunta_com_titulo_maior_que_200_caracteres():
    # 2. Comportamento: Validação do limite máximo de caracteres do título da Question
    titulo_longo = "Q" * 201
    
    with pytest.raises(Exception, match="Title cannot be longer than 200 characters"):
        Question(title=titulo_longo)

def test_deve_permitir_criar_pergunta_com_pontuacao_maxima_permitida():
    # 3. Comportamento: Teste de limite (boundary test) para o valor máximo aceito (100)
    pergunta = Question(title="Pergunta Bônus", points=100)
    assert pergunta.points == 100

def test_deve_gerar_ids_sequenciais_para_novas_alternativas():
    # 4. Comportamento: O sistema de geração de IDs das alternativas deve ser previsível e sequencial
    pergunta = Question(title="Matemática")
    c1 = pergunta.add_choice("Opção A")
    c2 = pergunta.add_choice("Opção B")
    c3 = pergunta.add_choice("Opção C")
    
    assert c1.id == 1
    assert c2.id == 2
    assert c3.id == 3

def test_nova_alternativa_deve_ser_incorreta_por_padrao():
    # 5. Comportamento: Se não especificarmos, a alternativa nasce como 'is_correct=False'
    pergunta = Question(title="Geografia")
    escolha = pergunta.add_choice("Brasil")
    
    assert escolha.is_correct is False

def test_deve_lancar_erro_ao_definir_gabarito_com_id_inexistente():
    # 6. Comportamento: set_correct_choices deve falhar se passarmos um ID que não foi criado
    pergunta = Question(title="História")
    pergunta.add_choice("Opção 1") # ID 1
    
    with pytest.raises(Exception, match="Invalid choice id 99"):
        pergunta.set_correct_choices([99])

def test_deve_retornar_lista_vazia_se_usuario_errar_tudo():
    # 7. Comportamento: correct_selected_choices não deve retornar nada se nenhuma escolha selecionada for a certa
    pergunta = Question(title="Química")
    pergunta.add_choice("Água", is_correct=True)  # ID 1
    pergunta.add_choice("Fogo", is_correct=False) # ID 2
    
    acertos = pergunta.correct_selected_choices([2])
    assert acertos == [] # Lista vazia, pois ele selecionou a errada

def test_deve_retornar_apenas_ids_corretos_em_multipla_escolha():
    # 8. Comportamento: correct_selected_choices deve filtrar e devolver só o que o usuário acertou
    pergunta = Question(title="Cores", max_selections=3)
    pergunta.add_choice("Azul", is_correct=True)     # ID 1
    pergunta.add_choice("Laranja", is_correct=False) # ID 2
    pergunta.add_choice("Verde", is_correct=True)    # ID 3
    
    # O usuário selecionou as 3, mas só a 1 e a 3 estão certas
    acertos = pergunta.correct_selected_choices([1, 2, 3])
    assert acertos == [1, 3]

def test_remover_alternativa_deve_manter_as_outras_intactas():
    # 9. Comportamento: Remover uma alternativa do meio não deve afetar a existência das outras
    pergunta = Question(title="Física")
    pergunta.add_choice("A") # ID 1
    pergunta.add_choice("B") # ID 2
    pergunta.add_choice("C") # ID 3
    
    pergunta.remove_choice_by_id(2)
    ids_restantes = [c.id for c in pergunta.choices]
    
    assert ids_restantes == [1, 3]
    assert len(pergunta.choices) == 2

def test_nova_pergunta_deve_ter_uuid_unico_gerado_automaticamente():
    # 10. Comportamento: Toda Question criada ganha um hash único de identificação
    p1 = Question(title="Primeira Pergunta")
    p2 = Question(title="Segunda Pergunta")
    
    assert p1.id != p2.id
    assert isinstance(p1.id, str) # O uuid.uuid4().hex retorna uma string

    # --- NOVOS TESTES COM FIXTURES (Commit 3) ---

@pytest.fixture
def pergunta_com_alternativas():
    """
    Fixture que cria e retorna uma Question pré-populada com 3 escolhas.
    Essa mesma instância (limpa) será injetada em cada teste que a solicitar.
    """
    questao = Question(title="Qual é a complexidade de tempo da busca binária?", points=10, max_selections=1)
    questao.add_choice("O(n)", is_correct=False)       # ID gerado: 1
    questao.add_choice("O(log n)", is_correct=True)    # ID gerado: 2
    questao.add_choice("O(n^2)", is_correct=False)     # ID gerado: 3
    return questao


def test_deve_identificar_resposta_correta_usando_fixture(pergunta_com_alternativas):
    # O teste já recebe a 'pergunta_com_alternativas' pronta para uso
    acertos = pergunta_com_alternativas.correct_selected_choices([2])
    
    assert acertos == [2]
    assert len(acertos) == 1

def test_deve_limpar_todas_as_alternativas_usando_fixture(pergunta_com_alternativas):
    # Verificamos se a fixture realmente trouxe as 3 alternativas iniciais
    assert len(pergunta_com_alternativas.choices) == 3
    
    # Executamos a ação e testamos o resultado
    pergunta_com_alternativas.remove_all_choices()
    assert len(pergunta_com_alternativas.choices) == 0

def test_deve_bloquear_respostas_acima_do_limite_usando_fixture(pergunta_com_alternativas):
    # A nossa fixture definiu max_selections=1. Tentar enviar 2 IDs deve gerar um erro.
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        pergunta_com_alternativas.correct_selected_choices([1, 2])