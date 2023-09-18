from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# Templates for Subjective Questioning

subjective_question_template = """
You are an examiner for the pharmacy license exam.
Generate 1 subjective question based on the users request.
All questions should be based on the concepts here: {context}

%TEXT
{question}
"""

subjective_answer_template = """
You are a teacher grading a quiz. 
You are given a {question} and the student's answer, 
Respond with the true answer based on the {context} and score the student answer out of a score of 10.

Example Format:
QUESTION: question here
STUDENT ANSWER: student's answer here
TRUE ANSWER: your correct answer here
GRADE: score out of 10

Grade the student answers based ONLY on their factual accuracy. 
Ignore differences in punctuation and phrasing between the student answer and true answer.
It is OK if the student answer contains more information than the true answer, 
as long as it does not contain any conflicting statements. Begin! 

QUESTION: {question}
STUDENT ANSWER: {student_answer}
TRUE ANSWER: 
GRADE: 

And explain why the STUDENT ANSWER is correct or incorrect based on your correct answer
"""


# Create a LangChain prompt template that we can insert values to later
subjective_question_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=subjective_question_template,
)

subject_answer_prompt = PromptTemplate(
    input_variables=["context", "question", "student_answer"],
    template=subjective_answer_template,
)


response_schemas = [
    ResponseSchema(
        name="Questions",
        description="""a list of all questions generated with each question having a list of the multiple choices.
        Questions should not be numbered.""",
    ),
    ResponseSchema(
        name="Options",
        description="all options generated for each question as a list of options",
    ),
    ResponseSchema(
        name="Answers",
        description="all answers generated for each question as a list of answers",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# Templates for Objective Questioning
objective_question_template = """
%INSTRUCTIONS:
You are an examiner for the pharmacy license exam.
Create {option_type} type questions
All questions should be based on the concepts here: {context}
Let's think step by step
{format_instructions}
The format for each quiz should be as such:
- Multiple-choice: 
    - Questions
        <Question 1>: <a. Option 1>, <b. Option 2>, <c. Option 3>, <d. Option 4>
        <Question 2>: <a. Option 1>, <b. Option 2>, <c. Option 3>, <d. Option 4>
    .....
    -Answers:
        <Answer 1>: <a Option 1|b Option 2|c Option 3|d Option 4>
        <Answer 2>: <a Option 1|b Option 2|c Option 3|d Option 4>

    Example:
        - Questions
            -1. What is the name of the drug that is used to treat the diabetes?
                a. Paracetamol
                b. Ibuprofen
                c. Zinc
                d. Metformin
                
            -2 What is the name of the drug that is used to treat the hypertension?
                a. Vitamin C
                b. Senna
                c. Magnesium
                d. Amlodipine
                
        - Answers:
            1. d. Metformin
            2. d. Amlodipine

- True/False:
    - Questions
        <Question 1>: <True|False>
        <Question 2>: <True|False>

    - Answers
        <Answer 1>: <True|False>
        <Answer 2>: <True|False>

    Example:
        - Questions
            -1. Is Metformin used to treat diabetes? True/False
            
            -2 Is Amlodipine used to treat polio? True/False
        - Answers: 
            1. True
            2. False

{question}
"""


objective_question_prompt = PromptTemplate(
    input_variables=[
        "context",
        "question",
        "option_type",
    ],
    partial_variables={"format_instructions": format_instructions},
    template=objective_question_template,
)
