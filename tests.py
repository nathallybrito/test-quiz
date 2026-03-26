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

